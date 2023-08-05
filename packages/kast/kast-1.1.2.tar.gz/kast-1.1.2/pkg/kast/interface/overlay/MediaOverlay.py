#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import os
from typing import Type

from kast.interface.overlay.MediaOverlayBase import MediaOverlayBase


def _getImpl() -> Type[MediaOverlayBase]:
    if os.name == 'posix':
        from ._mpris.MediaOverlayMpris import MediaOverlayMpris
        return MediaOverlayMpris

    if os.name == 'nt':
        from ._winrt.MediaOverlayWinrt import MediaOverlayWinrt
        return MediaOverlayWinrt

    return MediaOverlayBase


MediaOverlay = _getImpl()
