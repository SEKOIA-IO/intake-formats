import json
import os
from collections.abc import Generator, Sequence
from pathlib import Path
from time import sleep
from typing import Any

import requests as requests
import typer
from requests.adapters import HTTPAdapter, Retry

app = typer.Typer()
CHUNK_SIZE: int = 1000
TIME_BETWEEN_CHUNKS = 1  # seconds
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))


def read_input_messages(intake_path: Path) -> list:
    # iterate over files in
    # that directory
    events: list = list()
    intake_tests_path = f"{intake_path}/tests"
    for filename in os.listdir(intake_tests_path):
        f: str = os.path.join(intake_tests_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f) as json_file:
                testfile = json.load(json_file)
                events.append(testfile["input"]["message"])

    return events


def chunk_events(events: Sequence, chunk_size: int) -> Generator[list[Any], None, None]:
    """
    Group events by chunk
    :param sequence events: The events to group
    :param int chunk_size: The size of the chunk
    """
    chunk: list[Any] = []

    # iter over the events
    for event in events:

        # if the chunk is full
        if len(chunk) >= chunk_size:
            # yield the current chunk and create a new one
            yield chunk
            chunk = []

        # add the event to the current chunk
        chunk.append(event)

    # if the last chunk is not empty
    if len(chunk) > 0:
        # yield the last chunk
        yield chunk


def send_events(intake_key: str, url: str, events: list, chunk_size: int) -> None:
    intake_key_str = typer.style(f'sekoiaio.intake.key: "{intake_key}"', fg="green")

    params = {"return_response": "true"}
    events_ids: list = []

    chunks = chunk_events(events, chunk_size)
    for index, chunk in enumerate(chunks):
        typer.echo(f"Sending chunk #{index} with {len(chunk)} events to {intake_key_str}")
        content = {"intake_key": intake_key, "jsons": chunk}
        response = session.post(url=url, json=content, params=params)
        if response.ok:
            response_json = response.json()
            events_ids.extend(response_json.get("event_ids", []))
        else:
            typer.echo(typer.style(f"Error for chunk #{index}: {response.status_code} {response.json()}", fg="red"))
        sleep(TIME_BETWEEN_CHUNKS)

    if len(events_ids) > 0:
        response_text = typer.style('event.id: ("{}")'.format('" OR "'.join(events_ids)), fg="green")
        typer.echo(f"Response: {response_text}")


@app.command()
def from_intake_formats(intake_key: str, url: str, intake_path: Path, chunk_size: int = CHUNK_SIZE):
    events: list = read_input_messages(intake_path)
    send_events(intake_key=intake_key, events=events, url=url, chunk_size=chunk_size)


@app.command()
def from_text_file(intake_key: str, url: str, file: Path, chunk_size: int = CHUNK_SIZE):
    with open(file) as input_file:
        send_events(
            events=[line[:-1] for line in input_file.readlines()],  # remove the line-feed at the end of the line
            intake_key=intake_key,
            url=url,
            chunk_size=chunk_size,
        )


@app.command()
def from_cli(intake_key: str, url: str, event: str, chunk_size: int = CHUNK_SIZE):
    send_events(events=[event], intake_key=intake_key, url=url, chunk_size=chunk_size)


if __name__ == "__main__":
    app()
