#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_server.server import Server as MprisServer

from kast.interface.overlay.MediaOverlayBase import MediaOverlayBase
from kast.interface.overlay._mpris.MprisCastController import MprisCastController
from kast.interface.overlay._mpris.MprisEventListener import MprisEventListener
from kast.media.casting.CastController import CastController
from kast.media.casting.CastState import CastState
from kast.settings.Settings import Settings
from kast.settings.SettingsState import SettingsState


class MediaOverlayMpris(MediaOverlayBase):

    def __init__(
        self,
        settings: Settings,
        castController: CastController
    ) -> None:
        super().__init__(settings=settings, castController=castController)

        self._mprisCastController = MprisCastController(settings=settings, castController=castController)
        self._mprisServer = MprisServer(name=settings.appName, adapter=self._mprisCastController)
        self._mprisServer.publish()
        self._mprisEventListener = MprisEventListener(mprisServer=self._mprisServer, mprisCastController=self._mprisCastController)

    def run(self) -> None:
        self._mprisServer.loop()

    def onSettingsEvent(self, event: SettingsState) -> None:
        self._mprisEventListener.onSettingsEvent(event=event)

    def onCastEvent(self, event: CastState) -> None:
        self._mprisEventListener.onCastEvent(event=event)
