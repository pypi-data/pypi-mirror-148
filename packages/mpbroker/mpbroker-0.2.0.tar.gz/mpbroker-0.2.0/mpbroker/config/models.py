#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

from datetime import date
from typing import List

from pydantic import BaseModel


class ConfigCore(BaseModel):
    """
    Core specific config.
    """

    name: str = None
    description: str = None
    version: str = None
    created: date = None
    modified: date = None


class ConfigBase(BaseModel):
    """
    Config Base.
    """

    user_config_file_name: str = None
    core: ConfigCore = None


class UserConfigDefaults(BaseModel):
    """
    Defaults for UserConfig.
    """

    source_label: str = None


class UserConfigInjest(BaseModel):
    """
    User Config Injest.
    """

    file_types: List[str] = None


class UserConfigDatabase(BaseModel):
    """
    User Config database info.
    """

    db_uri: str = None


class UserConfigBase(BaseModel):
    """
    User config base.
    """

    client_id: str = None
    player_id: str = None
    player: str = None

    database: UserConfigDatabase = None
    defaults: UserConfigDefaults = None
    injest: UserConfigInjest = None
    source_mappings: dict = None
