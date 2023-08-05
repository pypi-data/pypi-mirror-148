#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import List

from kast.media.processing.SubtitlesSource import ISubtitlesSource


class SubtitlesSourceList:

    def __init__(self) -> None:
        self._sources: List[ISubtitlesSource] = []

    def __len__(self) -> int:
        return len(self._sources)

    def __getitem__(self, index: int) -> ISubtitlesSource:
        return self._sources[index]

    def clear(self) -> None:
        self._sources = []

    def append(self, source: ISubtitlesSource) -> None:
        self._sources.append(source)

    def pop(self, index: int) -> ISubtitlesSource:
        return self._sources.pop(index)
