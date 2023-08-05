#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import kast
from kast.interface.overlay.MediaOverlay import MediaOverlay
from kast.media.casting.CastController import CastController
from kast.media.casting.CastEventObserver import CastEventObserver
from kast.media.processing.MediaProcessingService import MediaProcessingService
from kast.media.streaming.MediaServer import MediaServer
from kast.settings.Settings import Settings
from kast.settings.SettingsEventObserver import SettingsEventObserver
from kast.utils.ResourceProvider import ResourceProvider
from kast.utils.SingletonApplication import SingletonApplication


class Services:

    def __init__(self) -> None:
        self._appLock = SingletonApplication(appName=kast.__package_name__)
        self.resourceProvider = ResourceProvider(kast)
        self.settingsEventObserver = SettingsEventObserver()
        self.settings = Settings(resourceProvider=self.resourceProvider, settingsEventObserver=self.settingsEventObserver)

        self.castEventObserver = CastEventObserver()
        self.castController = CastController(settings=self.settings, castEventObserver=self.castEventObserver)
        self.mediaServer = MediaServer()
        self.mediaProcessingService = MediaProcessingService(self.settings.temporaryStoragePath)

        self.osMediaOverlay = MediaOverlay(settings=self.settings, castController=self.castController)
        self.settingsEventObserver.register(self.osMediaOverlay, self.osMediaOverlay.onSettingsEvent)
        self.castEventObserver.register(self.osMediaOverlay, self.osMediaOverlay.onCastEvent)
