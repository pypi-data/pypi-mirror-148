#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from pathlib import Path

from kast.media.processing.MediaProcessingService import MediaProcessingService
from kast.media.processing.common import StreamId


class ISubtitlesSource(ABC):

    @abstractmethod
    def toVtt(self) -> Path:
        """Convert subtitles source to VTT format and provide result file path."""


class SubtitlesFromStream(ISubtitlesSource):

    def __init__(
        self,
        mediaProcessingService: MediaProcessingService,
        mediaFile: Path,
        streamId: StreamId
    ) -> None:
        self._mediaProcessingService = mediaProcessingService
        self._mediaFile = mediaFile
        self._streamId = streamId

    def toVtt(self) -> Path:
        return self._mediaProcessingService.extractSubtitles(
            inputFile=self._mediaFile,
            streamId=self._streamId
        )


class SubtitlesFromFile(ISubtitlesSource):

    def __init__(
        self,
        mediaProcessingService: MediaProcessingService,
        subtitlesFile: Path
    ) -> None:
        self._mediaProcessingService = mediaProcessingService
        self._subtitlesFile = subtitlesFile

    def toVtt(self) -> Path:
        return self._mediaProcessingService.convertSubtitles(inputFile=self._subtitlesFile)
