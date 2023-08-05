#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import threading
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class UiState(Enum):
    Idle = 'Idle'
    DeviceSearch = 'Searching for cast devices'
    VideoProbe = 'Extracting video meta data'
    Preprocessing = 'Preprocessing'
    AvProcessing = 'Transcoding/Remuxing'
    Connecting = 'Connecting'
    Streaming = 'Streaming'
    Closing = 'Closing'


@dataclass
class Progress:
    complete: bool = True
    percentage: Optional[int] = None
    cancelEvent: Optional[threading.Event] = None


@dataclass
class UiEvent:
    state: UiState = UiState.Idle
    progress: Progress = Progress()
