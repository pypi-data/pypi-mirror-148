#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from pathlib import Path

StreamId = int
CodecName = str


def containerExtension(filePath: Path) -> str:
    return filePath.suffix.split('.')[-1]
