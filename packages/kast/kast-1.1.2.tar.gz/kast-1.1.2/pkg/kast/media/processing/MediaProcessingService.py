#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import threading
from pathlib import Path
from typing import Optional

import av

from .MetaData import MetaData
from .SubtitleUtils import SubtitleUtils
from .Transcoder import Codecs, Streams, TranscodeParams, Transcoder


class MediaProcessingService:

    DEFAULT_CONTAINER_FORMAT = 'mp4'

    DEFAULT_CODEC_VIDEO = 'h264'
    DEFAULT_CODEC_AUDIO = 'ac3'

    def __init__(self, storageDir: Path) -> None:
        self._storageDir = storageDir
        self._subtitleUtils = SubtitleUtils(storageDir=self._storageDir)

    @staticmethod
    def extractMetaData(inputFile: Path) -> MetaData:
        def fixStreamName(index: int, name: str, defaultPrefix) -> str:
            return name if name else f'{defaultPrefix} {index}'
        with av.open(str(inputFile)) as f:
            return MetaData(
                title=inputFile.stem,
                audioStreamLangs=[fixStreamName(idx, stream.language, 'Audio') for idx, stream in enumerate(f.streams.audio)],
                subtitleStreamLangs=[fixStreamName(idx, stream.language, 'Subtitles') for idx, stream in enumerate(f.streams.subtitles)]
            )

    def convertSubtitles(self, inputFile: Path) -> Path:
        return self._subtitleUtils.convertToVtt(inputFile=inputFile)

    def extractSubtitles(self, inputFile: Path, streamId: int) -> Path:
        return self._subtitleUtils.extractAsVtt(inputFile=inputFile, streamId=streamId)

    def createTranscoder(
        self,
        inputFile: Path,
        inputStreamIds: Streams,
        outputCodecNames: Optional[Codecs] = None,
        containerFormat: Optional[str] = None,
        progressCallback: Optional[Transcoder.Callback] = None,
        cancelEvent: Optional[threading.Event] = None
    ) -> Transcoder:
        containerFormat = containerFormat if containerFormat else self.DEFAULT_CONTAINER_FORMAT
        outputCodecNames = Codecs(
            video=self.DEFAULT_CODEC_VIDEO,
            audio=self.DEFAULT_CODEC_AUDIO
        )
        return Transcoder(
            params=TranscodeParams(
                inputFile=inputFile,
                inputStreamIds=inputStreamIds,
                outputCodecNames=outputCodecNames
            ),
            outputFile=(self._storageDir / f'movie.{containerFormat}'),
            progressCallback=progressCallback,
            cancelEvent=cancelEvent
        )
