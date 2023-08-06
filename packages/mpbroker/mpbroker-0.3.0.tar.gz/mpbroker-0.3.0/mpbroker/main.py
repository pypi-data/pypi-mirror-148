#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>
#
# LOGGING: designed to run at INFO loglevel.

import json
import subprocess  # nosec
import time
from pathlib import Path
from typing import Optional

import click
import pycouchdb
import requests
import typer
import urllib3
from mpbroker.config.config import DATABASES, user_cfg, prj_file
from mpbroker.models.injest import InjestResultType
from mpbroker.models.media import (
    Media,
    MediaPlay,
    MediaPlayHistory,
    MediaPlayRating,
    MediaPlayStatus,
)
from mpbroker.utils import get_sources_paths, make_doc

# disable InsecureRequestWarnings which come up if you are proxying couchdb through haproxy with ssl termination.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server = pycouchdb.Server(user_cfg.database.db_uri)
app = typer.Typer()


@app.command()
def db_init():
    """
    Perform db setup tasks such as creating all databases, views, etc.
    """

    typer.echo("Created needed databases...")
    for db in DATABASES:
        try:
            server.create(db)
            typer.secho(f" ✓ database: {db} - created", fg=typer.colors.GREEN)
        except pycouchdb.exceptions.Conflict:
            typer.secho(
                f" ✗ database: {db} - skipped (already exists)", fg=typer.colors.WHITE
            )
        except requests.exceptions.ConnectionError:
            typer.echo("Database unavailable, is it up?")
            raise typer.Exit()

    typer.echo("Create Media Views...")
    try:
        db = server.database("media")
    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()

    _doc = {
        "_id": "_design/by-name",
        "views": {
            "names": {
                "map": "function(doc) { \n  emit(doc.name, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources]);\n}"
            },
            "stats_status": {
                "map": "function (doc) {\n  emit(doc.play.status, 1);\n}",
                "reduce": "_count",
            },
            "stats_total": {
                "map": "function (doc) {\n  emit(doc._id, 1);\n}",
                "reduce": "_count",
            },
            "stats_sources": {
                "reduce": "_count",
                "map": "function (doc) {\n  emit(doc.sources, 1);\n}",
            },
        },
    }
    db.save(_doc)
    typer.echo(" - by-name view created")


@app.command()
def play(name: str):
    """
    Play a media item.
    """

    _base = Path(name)
    media_item = _base.name
    # typer.echo(f"Playing item [{name}/{media_item}]")

    # lookup item to get source.
    try:
        db = server.database("media")
    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()

    _doc = db.get(media_item)
    # typer.echo(f"- play doc: {_doc}")

    # typer.echo(f">> source_mappings: {user_cfg.source_mappings}")
    source_paths = get_sources_paths(_doc["sources"])
    if len(source_paths) < 1:
        typer.echo(
            f"No viable sources found for {name} with sources: {_doc['sources']}"
        )
        raise typer.Exit()
    # typer.echo(f" source_paths: {source_paths}")

    # @TODO: currently we simply play the first source_path - should have something
    #  better here eventually like a ranking or some checking.
    _media_path = f"{source_paths[0]['path']}/{name}"

    # capture when we start playing.
    _start = time.time()

    # @TODO: check if file and player exist, then execute
    typer.echo(f"Playing item with: {user_cfg.player} from location: {_media_path}")
    subprocess.call([user_cfg.player, _media_path])  # nosec
    _end = time.time()
    typer.echo("Play completed, creating play history...")

    # create the play history.
    _new_history = MediaPlayHistory(
        base=source_paths[0]["path"],
        player=user_cfg.player,
        start=_start,
        end=_end,
        client=f"{user_cfg.client_id}:{user_cfg.player_id}",
    )
    _history = []
    if (
        "play" in _doc
        and "history" in _doc["play"]
        and _doc["play"]["history"]
        and len(_doc["play"]["history"]) > 0
    ):
        _history = _doc["play"]["history"]
    _history.append(json.loads(_new_history.json()))
    # ~ j = json.loads(doc.json())
    # ~ typer.echo(f"- _history of type={type(_history)} is: {_history}")
    _doc["play"]["history"] = _history
    _doc["play"]["status"] = typer.prompt(
        "update Play Status",
        default=MediaPlayStatus.played,
        type=click.Choice([str(i) for i in MediaPlayStatus._value2member_map_]),
    )
    _doc["play"]["rating"] = int(
        typer.prompt(
            "Rate item",
            default=MediaPlayRating.ok,
            type=click.Choice([str(i) for i in MediaPlayRating._value2member_map_]),
        )
    )

    rating_notes = typer.prompt(
        "Add Rating notes? (leave blank to not add a note)",
        default="",
        show_default=False,
    )
    if rating_notes:
        _doc["play"]["rating_notes"] = rating_notes

    notes = typer.prompt(
        "Add Notes for media item? (leave blank to not add a note update)\n  A note for the media item could be something specific like 'watched Ep 1, 2, and 4'",
        default="",
        show_default=False,
    )
    if notes:
        _doc["play"]["notes"] = notes

    db.save(_doc)


@app.command()
def list(name: str):
    """
    List media by name.
    """

    from rich.console import Console
    from rich.table import Table

    try:
        db = server.database("media")
    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()

    results = db.query(
        "by-name/names",
        # ~ group='true',
        # ~ keys=[name],
        startkey=name,
        endkey=f"{name}\ufff0",
        as_list=True,
        # ~ flat="key"
    )

    if results:
        typer.echo("\n\n")
        # ~ typer.echo(f"- results: {results}")
        table = Table(title=f"Listing Results for: '{name}'", title_justify="center")
        table.add_column("Item", style="cyan", no_wrap=True)
        table.add_column("Status", justify="center", style="magenta")
        table.add_column("Rating")
        table.add_column("Notes")
        table.add_column("Sources", justify="right", style="yellow")

        for item in results:
            _status = item["value"][1]
            _rating = f"{item['value'][2]}" if item["value"][2] else ""
            _rating = f"{_rating} {item['value'][3]}" if item["value"][3] else _rating
            _notes = f"{item['value'][4]}" if item["value"][4] else ""
            # ~ typer.echo(f" - {item['value'][0]}/{item['key']} | {_status} {_rating}")
            table.add_row(
                f"{item['value'][0]}/{item['key']}",
                _status,
                _rating,
                _notes,
                f"{', '.join(item['value'][5])}",
            )

        console = Console()
        console.print(table)
    else:
        typer.echo("No results found")


@app.command()
def injest(
    base: str = typer.Option(
        ..., "--base", help="the base path to search for media items to injest"
    ),
    source_label: str = typer.Option(
        user_cfg.defaults.source_label,
        "--source-label",
        help="the label to use for this source",
    ),
):
    """
    Injest media from a given base location.
    """

    typer.echo("Scanning base ({base}) for media...")

    _base = Path(base)
    if not _base.exists() or not _base.is_dir():
        typer.echo(f"Directory [{_base}] not found or not a directory, cannot proceed!")
        raise typer.Exit()

    all_files = []
    injested_files = []
    updated_files = []
    already_exists_files = []
    for ext in user_cfg.injest.file_types:
        all_files.extend(_base.rglob(ext))

    typer.echo(
        f"""
---------- Confirm Injest ----------
- base:            {_base.as_posix()}
- file types:      {user_cfg.injest.file_types}
- source label:    {source_label} (note: all items injested will have this source label)
- number of items: {len(all_files)}
"""
    )

    typer.confirm("Do you want to continue?", abort=True)
    _start = time.time()

    with typer.progressbar(all_files) as progress:
        for f in progress:
            # do injest here returning if it was injested or not.
            ret = injest_file(
                source_label=source_label, filepath=f, base=_base.as_posix()
            )
            if ret == InjestResultType.ok:
                injested_files.append(f)
            elif ret == InjestResultType.updated:
                updated_files.append(f)
            elif ret == InjestResultType.fail_exists:
                already_exists_files.append(f)

    _stop = time.time()

    typer.echo(
        f"""
---------- Injest Summary ----------
 - location:        {_base.as_posix()}
 - source label:    {source_label}
 - files to injest: {len(all_files)}
 - number injested: {len(injested_files)}
 - number updated:  {len(updated_files)}
 - number skipped:  {len(already_exists_files)} (already exists)
Injestion took {_stop - _start}s
"""
    )


def injest_file(source_label: str, filepath: str, base: str):
    """
    Injest a file.
    """

    # ensure base ends with /
    _base = base if base.endswith("/") else f"{base}/"
    # directory is filepath.parent - base
    directory = str(filepath.parent).replace(_base, "")
    m = Media(
        doc_id=filepath.name,
        # sid=make_sid(filepath.name),
        name=filepath.name,
        base=_base,
        directory=directory,
        sources=[source_label],
        media_type=filepath.suffix,
        # ~ notes="",
        play=MediaPlay(),
        creator=None,
        updator=None,
    )

    dts = make_doc(doc=m, rename_doc_id=True)

    try:
        db = server.database("media")
    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()

    try:
        db.save(
            dts
        )  # note: dont use .json() here as it serializes to a string which wont work!
        return InjestResultType.ok
    except pycouchdb.exceptions.Conflict:
        _doc = db.get(m.doc_id)
        # set source and check if current matches, if not add.
        if source_label not in _doc["sources"]:
            _doc["sources"].append(source_label)
            db.save(_doc)
            return InjestResultType.updated
        else:
            typer.echo(
                f"- duplicate item not injested - {m.directory}/{m.name}, sources: {_doc['sources']}"
            )

        return InjestResultType.fail_exists


@app.command()
def stats():
    """
    Get media stats.
    """

    try:
        db = server.database("media")
    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()

    _total = db.query(
        "by-name/stats_total",
        # ~ group='true',
        # ~ keys=[name],
        # ~ startkey=name,
        # ~ endkey=f"{name}\ufff0",
        as_list=True,
        # ~ flat="key"
    )

    _status = db.query(
        "by-name/stats_status",
        group="true",
        as_list=True,
    )

    _sources = db.query(
        "by-name/stats_sources",
        group="true",
        as_list=True,
    )

    _sources_list = [
        f"\n    • {source['key'][0]} ({source['value']})" for source in _sources
    ]
    _new = [item for item in _status if item["key"] == MediaPlayStatus.new]
    _played = [item for item in _status if item["key"] == MediaPlayStatus.played]
    _watched = [item for item in _status if item["key"] == MediaPlayStatus.watched]

    typer.echo(
        f"""
Media Item Stats
  - TOTAL:   {_total[0]['value']}
  - New:     {_new[0]['value'] if _new else 0}
  - Played:  {_played[0]['value'] if _played else 0}
  - Watched: {_watched[0]['value'] if _watched else 0}
  - Sources: {''.join(_sources_list)}
"""
    )


def version_callback(value: bool):
    if value:
        typer.echo(f"""{prj_file['tool']['poetry']['name']} - {prj_file['tool']['poetry']['description']}
  version {prj_file['tool']['poetry']['version']}
""")

        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        help="Show application version and exit",
    ),
):
    # ~ typer.echo(f"{cfg.core.name} - {cfg.core.description}")
    pass


if __name__ == "__main__":
    app()
