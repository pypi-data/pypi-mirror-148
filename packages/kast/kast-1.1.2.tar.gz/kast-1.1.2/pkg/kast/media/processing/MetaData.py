#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from dataclasses import dataclass, field
from typing import List


@dataclass
class MetaData:
    title: str = ''
    audioStreamLangs: List[str] = field(default_factory=lambda: [])
    subtitleStreamLangs: List[str] = field(default_factory=lambda: [])
