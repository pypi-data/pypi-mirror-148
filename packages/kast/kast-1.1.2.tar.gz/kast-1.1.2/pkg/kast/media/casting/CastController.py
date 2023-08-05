#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import List, Optional

import pychromecast
from pychromecast.controllers.media import MediaStatus, MediaStatusListener
from pychromecast.controllers.receiver import CastStatus, CastStatusListener
from pychromecast.socket_client import ConnectionStatus, ConnectionStatusListener

from kast.media.processing.common import CodecName
from kast.utils.Loggable import Loggable
from kast.media.casting.CastEventObserver import CastEventObserver
from kast.media.casting.CastException import CastException
from kast.media.casting.CastState import CastMediaState, CastState, Seconds, \
    VolumeLevel, DeviceName
from kast.settings.Settings import Settings


class CastController(
    Loggable,
    MediaStatusListener,
    CastStatusListener,
    ConnectionStatusListener
):
    TIMEOUT = Seconds(10)
    SEEK_DELTA = Seconds(10)

    def __init__(
        self,
        settings: Settings,
        castEventObserver: CastEventObserver
    ) -> None:
        self._settings = settings
        self._castEventObserver = castEventObserver

        self.__device: Optional[pychromecast.Chromecast] = None
        self._castState: CastState = CastState()

    def _clear(self, mediaOnly: bool = False) -> None:
        if mediaOnly:
            self._castState.mediaState = CastMediaState()
            return

        self._castState = CastState()

    @property
    def _device(self) -> Optional[pychromecast.Chromecast]:
        return self.__device if self.isConnected else None

    @property
    def _mediaController(self) -> Optional[pychromecast.controllers.media.MediaController]:
        device = self._device
        return device.media_controller if device else None

    @property
    def castState(self) -> CastState:
        return self._castState

    @property
    def isConnected(self):
        return self.__device and self.castState.isConnected()

    @property
    def supportedMimeTypes(self) -> List[str]:
        return ['video/mp4']  # Theoretically should also support: ['video/x-matroska', 'video/webm']

    @property
    def supportedContainerFormats(self) -> List[str]:
        return ['mp4']  # Theoretically should also support: ['mkv', 'webm']

    @property
    def supportedVideoCodecs(self) -> List[CodecName]:
        return ['h264']  # Since 'Chromecast Ultra' support for 'hevc' (h265)!

    @property
    def supportedAudioCodecs(self) -> List[CodecName]:
        return ['ac3']  # No evidence for wider support for 'aac'.

    @property
    def preferredContainerFormat(self) -> str:  # TODO:  Apply some logic if possible.
        return self.supportedContainerFormats[0]

    @property
    def preferredVideoCodec(self) -> CodecName:  # TODO:  Apply some logic if possible.
        return self.supportedVideoCodecs[0]

    @property
    def preferredAudioCodec(self) -> CodecName:  # TODO:  Apply some logic if possible.
        return self.supportedAudioCodecs[0]

    def searchDevices(self) -> List[DeviceName]:
        castInfoList, castBrowser = pychromecast.discovery.discover_chromecasts(timeout=self.TIMEOUT.value)
        castBrowser.stop_discovery()
        return [ci.friendly_name for ci in castInfoList]

    def connect(self, name: DeviceName) -> None:
        chromecasts, castBrowser = pychromecast.get_chromecasts(timeout=self.TIMEOUT.value)
        castBrowser.stop_discovery()
        for chromecast in chromecasts:
            if name == chromecast.name:
                self._setupDevice(chromecast)
                return
        raise CastException(f"Could not find device by name '{name}'!")

    def disconnect(self) -> None:
        device = self._device
        if device:
            device.quit_app()
            device.disconnect()
            self._clear()

    def stream(
        self,
        movieUrl: str,
        movieMime: str = 'video/mp4',
        subtitlesUrl: str = None,
        subtitlesMime: str = 'text/vtt',
        thumbnailUrl: str = None,
        play: bool = True,
        title: str = None
    ) -> None:
        title = title if title is not None else self._settings.appName
        mediaController = self._mediaController
        if mediaController:
            mediaController.play_media(
                url=movieUrl,
                content_type=movieMime,
                subtitles=subtitlesUrl,
                subtitles_mime=subtitlesMime,
                autoplay=play,
                title=title,
                thumb=thumbnailUrl
            )
            mediaController.block_until_active()

    def quit(self) -> None:
        device = self._device
        device and device.quit_app()

    def setMute(self, val: bool) -> None:
        device = self._device
        device and device.set_volume_muted(val)

    def setVolume(self, val: VolumeLevel) -> None:
        device = self._device
        device and device.set_volume(val)

    def play(self) -> None:
        mediaController = self._mediaController
        mediaController and mediaController.play()

    def pause(self) -> None:
        mediaController = self._mediaController
        mediaController and mediaController.pause()

    def resume(self) -> None:
        mediaController = self._mediaController
        mediaController and mediaController.play()

    def stop(self) -> None:
        mediaController = self._mediaController
        mediaController and mediaController.stop()

    def seek(self, timePos: Seconds) -> None:
        mediaController = self._mediaController
        mediaController and mediaController.seek(timePos.value)

    def seekForward(self) -> None:
        self.seek(self._castState.mediaState.currentTime + self.SEEK_DELTA)

    def seekBackward(self) -> None:
        self.seek(self._castState.mediaState.currentTime - self.SEEK_DELTA)

    def _setupDevice(self, device: pychromecast.Chromecast) -> None:
        if device.cast_type != pychromecast.CAST_TYPE_CHROMECAST:
            raise CastException(f"Device '{device.name}' does not support video casting!")

        device.register_status_listener(self)
        device.media_controller.register_status_listener(self)
        device.socket_client.register_connection_listener(self)

        device.wait()

        self.__device = device
        self._castState.deviceName = device.name

    def _notify(self) -> None:
        self._castEventObserver.notify(event=self._castState)

    def new_media_status(self, status: MediaStatus):
        self._castState.update(mediaStatus=status)

        if self._castState.mediaState.isStopped():
            self._clear(mediaOnly=True)

        self._notify()

    def new_cast_status(self, status: CastStatus):
        self._castState.update(castStatus=status)
        self._notify()

    def new_connection_status(self, status: ConnectionStatus):
        self._castState.update(connectionStatus=status)

        if not self._castState.isConnectedOrRecoverable():
            self._clear()

        self._notify()
