#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from kast.media.casting.CastController import CastController
from kast.media.casting.CastState import CastState
from kast.settings.Settings import Settings
from kast.settings.SettingsState import SettingsState
from kast.utils.Loggable import Loggable


class MediaOverlayBase(Loggable):

    def __init__(
        self,
        settings: Settings,
        castController: CastController
    ) -> None:
        self._settings = settings
        self._castController = castController

    def run(self) -> None:
        pass

    def onSettingsEvent(self, event: SettingsState) -> None:
        pass

    def onCastEvent(self, event: CastState) -> None:
        pass
