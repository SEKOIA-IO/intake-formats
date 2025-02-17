#!/usr/bin/env python

import difflib
import json
import sys
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import requests
import structlog
import typer
import yaml
from rich.console import Console
from rich.markdown import Markdown

logger = structlog.get_logger()


def read_yaml(file: Path) -> Any:
    with file.open() as f:
        return yaml.safe_load(f)


def read_json(file: Path) -> Any:
    with file.open() as f:
        return json.load(f)


def clean_parser(obj: Any) -> Any:
    """Remove fields with null values and name property of actions in the parser"""
    if isinstance(obj, dict):
        return {
            key: clean_parser(value)
            for key, value in obj.items()
            if value is not None and (key != "name" or value not in ["set", "translate", "delete"])
        }
    if isinstance(obj, list):
        return [clean_parser(value) for value in obj]
    else:
        return obj


class Differ(ABC):
    @abstractmethod
    def validate(self, original: Any, replacement: Any, title: str) -> bool:
        raise NotImplementedError

    @abstractproperty
    def bypass(self) -> bool:
        raise NotImplementedError


class AskForDiff(Differ):
    def __init__(self, console: Console):
        self.__console = console

    @property
    def bypass(self) -> bool:
        return False

    def validate(self, original: Any, replacement: Any, title: str) -> bool:
        original_content = yaml.dump(clean_parser(original)).splitlines()
        replacement_content = yaml.dump(clean_parser(replacement)).splitlines()
        diff = list(
            difflib.unified_diff(
                original_content,
                replacement_content,
                fromfile=f"original {title}",
                tofile=f"replacement {title}",
            )
        )

        if len(diff) == 0:
            logger.info(f"No difference detected for {title}")
            return True

        diffy = "\n".join(list(diff))
        self.__console.print(
            Markdown(
                f"""
```diff
{diffy}
```
"""
            )
        )

        if typer.prompt("You are about to publish this modification. Continue? [y/n]").lower() == "n":
            return False
        else:
            return True


class AlwaysValidateDiff(Differ):
    def validate(self, original: Any, replacement: Any, title: str) -> bool:
        return True

    @property
    def bypass(self) -> bool:
        return True


@dataclass
class Item:
    uuid: str
    name: str
    slug: str
    description: str
    taxonomy: list
    logo: Path

    def as_payload(self, with_uuid=False) -> dict:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "taxonomy": self.taxonomy,
        }

    @property
    def type(self) -> str:
        raise NotImplementedError



@dataclass
class Format(Item):
    parser: dict
    datasources: list
    smartdescriptions: list | None = None
    automation_module_uuid: str | None = None
    automation_connector_uuid: str | None = None

    @property
    def type(self) -> str:
        return "format"

    @property
    def url_path(self) -> str:
        return "formats"

    @staticmethod
    def from_format_dir(format_dir: Path) -> "Format":
        if not format_dir.exists():
            raise OSError(f"Format '{format_dir.name}' doesn't exist")  # noqa: B028

        manifest_file = format_dir / "_meta/manifest.yml"
        if not manifest_file.exists():
            raise OSError(f"Missing manifest in the format '{format_dir.name}'")  # noqa: B028

        logo_file = format_dir / "_meta/logo.png"
        if not logo_file.exists():
            raise OSError(f"Missing logo in the format '{format_dir.name}'")  # noqa: B028
        elif logo_file.stat().st_size > 51200:
            raise OSError(
                f"Oversized format logo. expected lesser than 50KiB. got '{logo_file.stat().st_size}'"  # noqa: B028
            )

        parser = None
        parser_file = format_dir / "ingest/parser.yml"
        if parser_file.exists():
            parser = read_yaml(parser_file)
        else:
            logger.warning("No parser found for the format", format_name=format_dir.name)

        taxonomy: dict[str, str] = {}
        taxonomy_file = format_dir / "_meta/fields.yml"
        if taxonomy_file.exists():
            taxonomy = read_yaml(taxonomy_file)
        else:
            logger.warning("No taxonomy found for the format", format_name=format_dir.name)

        smartdescriptions = None
        smartdescriptions_file = format_dir / "_meta/smart-descriptions.json"
        if smartdescriptions_file.exists():
            smartdescriptions = read_json(smartdescriptions_file)
        else:
            logger.warning("No smartdescriptions found for the format", format_name=format_dir.name)

        manifest = read_yaml(manifest_file)
        datasources = list(manifest.get("data_sources", {}).keys())
        if len(datasources) == 0:
            logger.warning("No data sources found for the format", format_name=format_dir.name)

        return Format(
            uuid=manifest["uuid"],
            name=manifest["name"],
            slug=manifest["slug"],
            description=manifest["description"],
            parser=parser,
            datasources=datasources,
            taxonomy=list(taxonomy.values()),
            smartdescriptions=smartdescriptions,
            automation_connector_uuid=manifest.get("automation_connector_uuid"),
            automation_module_uuid=manifest.get("automation_module_uuid"),
            logo=logo_file,
        )

    def as_payload(self, with_uuid=False) -> dict:
        payload: dict[str, Any | dict] = {
            "format_uuid": self.uuid,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "datasources": self.datasources,
            "taxonomy": self.taxonomy,
            "automation_connector_uuid": self.automation_connector_uuid,
            "automation_module_uuid": self.automation_module_uuid,
        }

        if self.parser:
            payload["parser"] = self.parser

        return payload


class Client:
    def __init__(self, platform_url: str, api_key: str, ssl_verify: bool):
        self.platform_url = platform_url
        self.base_url = f"{platform_url}/v1/ingest"
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.verify = ssl_verify

    def get(self, item: Item) -> requests.Response:
        return requests.get(
            f"{self.base_url}/{item.url_path}/{item.uuid}",
            headers=self.headers,
            verify=self.verify,
        )

    def create(self, item: Item) -> requests.Response:
        return requests.post(
            f"{self.base_url}/{item.url_path}",
            json=item.as_payload(),
            headers=self.headers,
            verify=self.verify,
        )

    def update(self, item: Item) -> requests.Response:
        payload = item.as_payload()

        to_removed = {"uuid", "format_uuid"} & set(payload.keys())
        if len(to_removed) > 0:
            for key in to_removed:
                del payload[key]

        return requests.put(
            f"{self.base_url}/{item.url_path}/{item.uuid}",
            json=payload,
            headers=self.headers,
            verify=self.verify,
        )

    def update_image(self, item: Item) -> requests.Response:
        return requests.put(
            f"{self.base_url}/{item.url_path}/{item.uuid}/picture",
            files={"picture": (item.logo.name, item.logo.open("rb"), "image/png")},
            headers=self.headers,
            verify=self.verify,
        )

    def get_smartdescriptions(self, intake_format: Format) -> requests.Response:
        return requests.get(
            f"{self.base_url}/{intake_format.url_path}/{intake_format.uuid}/smart-descriptions",
            headers=self.headers,
            verify=self.verify,
        )

    def update_smartdescriptions(self, intake_format: Format) -> requests.Response:
        return requests.post(
            f"{self.base_url}/{intake_format.url_path}/{intake_format.uuid}/smart-descriptions",
            json={"content": intake_format.smartdescriptions},
            headers=self.headers,
            verify=self.verify,
        )


def update_format(client: Client, intake_format: Format, differ: Differ):
    if not differ.bypass:
        get_response = client.get(intake_format)
        if get_response.status_code > 399 and get_response.status_code != 404:
            logger.error(
                "Failed to get Format",
                format_uuid=intake_format.uuid,
                status_code=get_response.status_code,
                body=get_response.text,
            )
            sys.exit(22)

        content = get_response.json()
        if not differ.validate(
            {
                "uuid": content.get("uuid"),
                "name": content.get("name"),
                "slug": content.get("slug"),
                "description": content.get("description"),
                "datasources": content.get("datasources"),
                "automation_module_uuid": content.get("automation_module_uuid"),
                "automation_connector_uuid": content.get("automation_connector_uuid"),
            },
            {
                "uuid": intake_format.uuid,
                "name": intake_format.name,
                "slug": intake_format.slug,
                "description": intake_format.description,
                "datasources": intake_format.datasources,
                "automation_module_uuid": intake_format.automation_module_uuid,
                "automation_connector_uuid": intake_format.automation_connector_uuid,
            },
            "format",
        ):
            logger.info("Diff not validated. Format not published")
            return

        if not differ.validate(content.get("taxonomy"), intake_format.taxonomy, "taxomony"):
            logger.info("Diff not validated. Format not published")
            return

        if not differ.validate(content.get("parser"), intake_format.parser, "parser"):
            logger.info("Diff not validated. Format not published")
            return

    update_response = client.update(intake_format)
    if update_response.status_code == 200:
        logger.info(
            "Format updated",
            format_uuid=intake_format.uuid,
            status_code=update_response.status_code,
        )
    elif update_response.status_code == 404:
        update_response = client.create(intake_format)
        if update_response.status_code == 200:
            logger.info(
                "Format created",
                format_uuid=intake_format.uuid,
                status_code=update_response.status_code,
            )

    if update_response.status_code > 399:
        logger.error(
            "Failed to update Format",
            format_uuid=intake_format.uuid,
            status_code=update_response.status_code,
            body=update_response.text,
        )
        sys.exit(21)


def update_logo(client: Client, item: Item):
    update_response = client.update_image(item)
    if update_response.status_code == 200:
        logger.info(
            f"Image updated for {item.type.capitalize()}",
            item_type=item.type,
            item_uuid=item.uuid,
            status_code=update_response.status_code,
        )
    elif update_response.status_code > 399:
        logger.error(
            f"Failed to update image for {item.type.capitalize()}",
            item_type=item.type,
            item_uuid=item.uuid,
            status_code=update_response.status_code,
            body=update_response.text,
        )
        sys.exit(31)


def update_smartdescriptions(client: Client, intake_format: Format, differ: Differ):
    if not differ.bypass:
        get_response = client.get_smartdescriptions(intake_format)
        if get_response.status_code > 399 and get_response.status_code != 404:
            logger.error(
                "Failed to get smart-descriptions",
                format_uuid=intake_format.uuid,
                status_code=get_response.status_code,
                body=get_response.text,
            )
            sys.exit(42)

        if not differ.validate(
            get_response.json().get("content"),
            intake_format.smartdescriptions,
            "smart-descriptions",
        ):
            logger.info("Diff not validated. Smart-descriptions not published")
            return

    update_response = client.update_smartdescriptions(intake_format)
    if update_response.status_code == 200:
        logger.info(
            "Smart-descriptions updated",
            format_uuid=intake_format.uuid,
            status_code=update_response.status_code,
        )
    elif update_response.status_code > 399:
        logger.error(
            "Failed to update smart-descriptions",
            format_uuid=intake_format.uuid,
            status_code=update_response.status_code,
            body=update_response.text,
        )
        sys.exit(41)


def publish_format(format: Path, platform_url: str, apikey: str, ssl_verify: bool, differ: Differ):
    client = Client(platform_url, apikey, ssl_verify)

    try:
        intake_format = Format.from_format_dir(format)
    except OSError:
        logger.exception("Failed to publish format")
        sys.exit(10)

    update_format(client, intake_format, differ)
    update_logo(client, intake_format)
    if intake_format.smartdescriptions:
        update_smartdescriptions(client, intake_format, differ)
    sys.exit(0)


def main(
    format_path: Path,
    apikey: str,
    url: str = "https://app.sekoia.io",
    insecure: bool = False,
    host: Optional[str] = None, #noqa: UP007
    no_diff: bool = False,
):
    """
    Publish new format to ingestAPI.
    format_path: The location of the format to publish
    apikey: The APIKey to use
    url: The base URL to the Sekoia.io platform
    If --insecure is used, it disables SSL verification (develop/test purpose)
    If --host is used, it takes a custom host
    If --no-diff is used, the changes will be not be displayed
    """
    ssl_verify = True

    if insecure:
        ssl_verify = False

    if host:
        url = host

    differ: Differ = AskForDiff(Console())
    if no_diff:
        differ = AlwaysValidateDiff()

    publish_format(format_path, url, apikey, ssl_verify, differ)


if __name__ == "__main__":
    typer.run(main)
