#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

from enum import Enum


class InjestResultType(str, Enum):
    """
    Injest Result types.
    """

    ok = "ok, processed successfully"
    updated = "document updated"
    fail_exists = "failure, document already exists"
