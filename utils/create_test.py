#!/usr/bin/env python
# coding: utf-8

import sys
from pathlib import Path

import orjson
import typer
import yaml


def read_yaml(file: Path):
    with file.open() as f:
        return yaml.safe_load(f)


def get_module_manifest_file(format_path: Path):
    module_manifest_file = format_path.parent / "_meta/manifest.yml"
    if module_manifest_file.exists():
        return module_manifest_file

    module_manifest_file = format_path.parent / "_meta/manifest.yaml"
    if module_manifest_file.exists():
        return module_manifest_file

    typer.echo("error='Missing manifest in the module'")
    raise typer.Exit(code=10)


def get_format_manifest_file(format_path: Path):
    manifest_file = format_path / "_meta/manifest.yml"
    if manifest_file.exists():
        return manifest_file

    manifest_file = format_path / "_meta/manifest.yaml"
    if manifest_file.exists():
        return manifest_file

    typer.echo("error='Missing manifest in the format'")
    raise typer.Exit(code=11)


def create_test(
    output: Path = typer.Argument(
        ...,
        help="The destination file of the test",
        dir_okay=False,
        file_okay=True,
        writable=True,
        resolve_path=True,
    ),
    event: str = typer.Argument(..., help="The raw event to add in the test as the message"),
):

    get_module_manifest_file(output.parent.parent)
    manifest_file = get_format_manifest_file(output.parent.parent)
    manifest = read_yaml(manifest_file)

    if event == "-":
        event = sys.stdin.read()

    test = {
        "input": {
            "sekoiaio": {
                "intake": {
                    "dialect": manifest["name"],
                    "dialect_uuid": manifest["uuid"],
                },
            },
            "message": event,
        },
        "expected": {"message": event},
    }

    with output.open("wb+") as f:
        f.write(orjson.dumps(test, option=orjson.OPT_INDENT_2))


if __name__ == "__main__":
    typer.run(create_test)
