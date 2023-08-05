#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_server.events import EventAdapter
from mpris_server.server import Server as MprisServer

from kast.interface.overlay._mpris.MprisCastController import MprisCastController
from kast.media.casting.CastState import CastState
from kast.settings.SettingsState import SettingsState


class MprisEventListener(EventAdapter):

    def __init__(
        self,
        mprisServer: MprisServer,
        mprisCastController: MprisCastController
    ) -> None:
        super().__init__(
            player=mprisServer.player,
            root=mprisServer.root
        )
        self._mprisCastController = mprisCastController

    def onSettingsEvent(self, event: SettingsState) -> None:
        self._mprisCastController.onSettingsEvent(event=event)
        self._reload()

    def onCastEvent(self, event: CastState) -> None:
        self._reload()

    def _reload(self) -> None:
        self.on_volume()
        self.on_playback()
        self.on_title()
        self.on_options()
        self.on_playpause()
