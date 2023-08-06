#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2021 drad <drader@adercon.com>

import logging
import sys
import pkg_resources

_log_level = "INFO"   #[CRITICAL|ERROR|WARNING|INFO|DEBUG] (suggest INFO)
APP_VERSION = pkg_resources.get_distribution("cryptik").version
APP_NAME = pkg_resources.get_distribution("cryptik").project_name

logging.basicConfig(
    format="%(message)s",
    level=logging.getLevelName(_log_level),
    stream=sys.stdout,
)
