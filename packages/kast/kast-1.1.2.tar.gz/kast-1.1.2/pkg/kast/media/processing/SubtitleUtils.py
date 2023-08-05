#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import itertools
from pathlib import Path
from typing import List, Tuple

import av
import pycaption
import pysubs2


class SubtitleException(Exception):
    pass


class SubtitleUtils:

    _EVENT_LINE_PREFIX = 'Dialogue: '

    def __init__(self, storageDir: Path) -> None:
        self._storageDir = storageDir

        outputFileBaseName = 'subtitles'

        self._intermediateFile = self._storageDir / f'{outputFileBaseName}.ass'
        self._outputFile = self._storageDir / f'{outputFileBaseName}.vtt'

    def extractAsVtt(self, inputFile: Path, streamId: int) -> Path:
        self._extractRawSsa(inputFile=inputFile, streamId=streamId)
        self._convertToVtt(self._convertRawSsaToSrtString())
        return self._outputFile

    def convertToVtt(self, inputFile: Path) -> Path:
        with open(inputFile, encoding='utf-8', errors='ignore') as fInput:
            self._convertToVtt(fInput.read())
        return self._outputFile

    def _convertToVtt(self, subtitles: str) -> None:
        converter = pycaption.CaptionConverter()

        subFormat = pycaption.detect_format(subtitles)
        if not subFormat:
            raise SubtitleException("Could not detect subtitle format or content malformed!")

        converter.read(subtitles, subFormat())
        with open(self._outputFile, 'w', encoding='utf-8', errors='ignore') as fOutput:
            fOutput.write(converter.write(pycaption.WebVTTWriter()))

    def _extractRawSsa(self, inputFile: Path, streamId: int) -> None:
        with av.open(str(inputFile)) as fInput:
            with av.open(str(self._intermediateFile), 'w') as fOutput:
                inStream = fInput.streams.subtitles[streamId]
                outStream = fOutput.add_stream('ass')
                for packet in fInput.demux(inStream):
                    if packet.dts is None:
                        continue
                    packet.stream = outStream
                    fOutput.mux(packet)

    def _convertRawSsaToSrtString(self) -> str:
        subGen = pysubs2.SSAFile()
        with open(self._intermediateFile, encoding='utf-8', errors='ignore') as fInput:
            lineBuffer = ''
            for line in fInput.readlines():
                line = line.rstrip('\n')

                if len(lineBuffer) > 0:
                    if not line.startswith(self._EVENT_LINE_PREFIX):
                        lineBuffer += '\\N'
                    else:
                        subGen.events.append(self._parseSsaEvent(lineBuffer))
                        lineBuffer = ''

                lineBuffer += line

            if len(lineBuffer) > 0:
                subGen.events.append(self._parseSsaEvent(lineBuffer))

        self._removeTextPrefix(subEvents=subGen.events)

        return subGen.to_string('srt')

    def _parseSsaEvent(self, eventStr: str) -> pysubs2.SSAEvent:
        layer, startStr, endStr, text = eventStr[len(self._EVENT_LINE_PREFIX):].split(',', maxsplit=3)

        def timestampStrToMs(timestampStr: str) -> int:
            return pysubs2.time.timestamp_to_ms(pysubs2.time.TIMESTAMP.match(timestampStr).groups())

        event = pysubs2.SSAEvent()
        event.layer = layer
        event.start = timestampStrToMs(startStr)
        event.end = timestampStrToMs(endStr)
        event.text = text

        return event

    def _removeTextPrefix(self, subEvents: List[pysubs2.SSAEvent]) -> None:
        prefix = self._findCommonTextPrefix(subEvents=subEvents)
        if not prefix:
            return

        for subEvent in subEvents:
            subEvent.text = self._removePrefix(subEvent.text, prefix)

    @staticmethod
    def _removePrefix(text: str, prefix: str) -> str:
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    @staticmethod
    def _findCommonTextPrefix(subEvents: List[pysubs2.SSAEvent]) -> str:
        def allCharacterInColumnAreTheSame(charColumn: Tuple[str]) -> bool:
            return all(charColumn[0] == character for character in charColumn)

        charColumns = zip(*[e.text for e in subEvents])
        prefixColumns = itertools.takewhile(allCharacterInColumnAreTheSame, charColumns)
        prefix = ''.join(prefixColumn[0] for prefixColumn in prefixColumns)

        separator = ','
        return prefix.rsplit(separator, maxsplit=1)[0] + separator
