#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from kast.interface.overlay.MediaOverlayBase import MediaOverlayBase
from kast.interface.overlay._winrt.WinrtCastController import WinrtCastController
from kast.media.casting.CastController import CastController
from kast.media.casting.CastState import CastState
from kast.settings.Settings import Settings
from kast.settings.SettingsState import SettingsState


class MediaOverlayWinrt(MediaOverlayBase):

    def __init__(
        self,
        settings: Settings,
        castController: CastController
    ) -> None:
        super().__init__(settings=settings, castController=castController)

        self._winrtCastController = WinrtCastController(settings=settings, castController=castController)

    def run(self) -> None:
        self._winrtCastController.reload()

    def onSettingsEvent(self, event: SettingsState) -> None:
        self._winrtCastController.reload()

    def onCastEvent(self, event: CastState) -> None:
        self._winrtCastController.reload()
