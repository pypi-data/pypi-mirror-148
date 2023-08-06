#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

import json
from pathlib import Path
from typing import List

import typer
from mpbroker.config.config import user_cfg


def get_sources_paths(sources: List):
    """
    Get sources paths.
    NOTE: source paths are validated (checked), if a path is invalid (does not exist)
          it will not be returned.
    @return: list of source paths.
    """

    # typer.echo(f">> sources: {sources}")
    _ret = []
    for source in sources:
        if source in user_cfg.source_mappings:
            _path = user_cfg.source_mappings[source]
            # check if path exists.
            if Path(_path).is_dir() and any(Path(_path).iterdir()):
                typer.echo(f"- found {_path} and it has data...")
                _ret.append({"source": source, "path": _path})
            # typer.echo(f"- found {source} in source_mappings: {user_cfg.source_mappings[source]}")

    # typer.echo(f"_ret is: {_ret}")
    return _ret


def generate_sid(instr: str = None):
    """
    Generate a sid given an input string.
    Example: 'Duck_Dynasty_S1_D1.mkv' ─⏵ 'DCKDNSTS1D1.MKV'
    """

    return instr.translate(str.maketrans("", "", "AaEeIiOoUuYy_-()[]")).upper()


def make_doc(doc=None, rename_doc_id: bool = False):
    """
    Create a couchdb doc by deserializing the class to json, loading it back to
    json and finally renaming the doc_id field to _id.

    NOTE: the double deserialization is needed to get dates deserialized (easily)
    NOTE: we need to rename doc_id to _id as we can name it _id in the model or alias
          it as python treats it as a local and does not export it on deserialization.
    """

    j = json.loads(doc.json())
    if "doc_id" in j and rename_doc_id:
        j["_id"] = j.pop("doc_id")
    # ~ typer.echo(f"j={j}")

    return j
