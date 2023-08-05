#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import os
from dataclasses import dataclass, field
from pathlib import Path

from dataclasses_json import dataclass_json


def defaultBrowseMediaPath() -> str:
    return str(Path.home() if os.name == 'posix' else Path.home().anchor)


@dataclass_json
@dataclass
class SettingsState:
    previousTemporaryPath: str = ''
    browseMediaPath: str = field(default_factory=defaultBrowseMediaPath)  # Path is not serializable.
