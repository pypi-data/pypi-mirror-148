#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import List, Optional

from mpris_server.adapters import MprisAdapter
from mpris_server.base import DbusObj, Microseconds, PlayState, URI, VolumeDecimal
from mpris_server.compat import enforce_dbus_length, get_dbus_name
from mpris_server.metadata import Metadata

from kast.interface.overlay._mpris.common import castTimeToMprisTime, mprisTimeToCastTime
from kast.media.casting.CastController import CastController
from kast.media.casting.CastState import CastConnectionState, CastState
from kast.settings.Settings import Settings
from kast.settings.SettingsState import SettingsState


class MprisCastController(MprisAdapter):

    def __init__(
        self,
        settings: Settings,
        castController: CastController
    ) -> None:
        super().__init__(name=settings.appName)
        self._settings = settings
        self._castController = castController

        self._desktopFilePath = self._settings.persistentStoragePath.joinpath(f"{self._settings.package}.desktop")
        self._createDesktopFile()

    @property
    def _castState(self) -> CastState:
        return self._castController.castState

    def metadata(self) -> Metadata:

        @enforce_dbus_length
        def get_track_id(name: str) -> DbusObj:
            return f'/track/{get_dbus_name(name)}'

        title = self.get_stream_title()
        contentUrl = self._castState.mediaState.contentUrl
        contentUrl = contentUrl if contentUrl else None

        metadata = {
            'mpris:trackid': get_track_id(title),
            'mpris:length': castTimeToMprisTime(self._castState.mediaState.duration),
            'mpris:artUrl': self.get_art_url(),
            'xesam:url': contentUrl,
            'xesam:title': title,
            'xesam:artist': [self._castState.deviceName],
        }

        return metadata

    def get_art_url(self, track: Optional[int] = None) -> str:
        return self._castState.mediaState.imageUrl or \
            self._castState.mediaState.iconUrl or \
            str(self._settings.appIconPath)

    def get_desktop_entry(self) -> str:
        return str(self._desktopFilePath.with_suffix(suffix=''))

    def get_stream_title(self) -> str:
        title = self._castState.mediaState.title \
            if self._castState.mediaState.title is not None \
            else self._settings.appName

        if self._castState.connection == CastConnectionState.Lost:
            title = f'[Connection Lost] {title}'

        return title

    def get_uri_schemes(self) -> List[str]:
        return URI

    def get_mime_types(self) -> List[str]:
        return self._castController.supportedMimeTypes

    def can_quit(self) -> bool:
        return True

    def can_control(self) -> bool:
        return True

    def can_play(self) -> bool:
        return True

    def can_pause(self) -> bool:
        return self._castState.capabilities.canPause

    def can_seek(self) -> bool:
        return self._castState.capabilities.canSeek

    def can_go_next(self) -> bool:
        return False

    def can_go_previous(self) -> bool:
        return False

    def is_mute(self) -> bool:
        return self._castState.mediaState.volumeMuted

    def get_volume(self) -> VolumeDecimal:
        return self._castState.mediaState.volumeLevel

    def get_playstate(self) -> PlayState:
        if self._castState.mediaState.isPlaying():
            return PlayState.PLAYING
        if self._castState.mediaState.isPaused():
            return PlayState.PAUSED
        return PlayState.STOPPED

    def get_current_position(self) -> Microseconds:
        return castTimeToMprisTime(self._castState.mediaState.currentTime)

    def is_playlist(self) -> bool:
        return False

    def is_repeating(self) -> bool:
        return False

    def get_shuffle(self) -> bool:
        return False

    def quit(self) -> None:
        self._castController.quit()

    def set_mute(self, val: bool) -> None:
        self._castController.setMute(val)

    def set_volume(self, val: VolumeDecimal) -> None:
        self._castController.setVolume(val)

    def play(self) -> None:
        self._castController.play()

    def pause(self) -> None:
        self._castController.pause()

    def resume(self) -> None:
        self._castController.play()

    def stop(self) -> None:
        self._castController.stop()

    def seek(self, timePos: Microseconds) -> None:
        self._castController.seek(mprisTimeToCastTime(timePos))

    def next(self) -> None:
        pass

    def previous(self) -> None:
        pass

    def set_repeating(self, val: bool) -> None:
        pass

    def set_shuffle(self, val: bool) -> None:
        pass

    def set_loop_status(self, val: str) -> None:
        pass

    def onSettingsEvent(self, event: SettingsState) -> None:
        pass

    def _createDesktopFile(self) -> None:
        desktopFileContent = \
            "[Desktop Entry]\n" \
            "Encoding=UTF-8\n" \
            f"Name={self._settings.appName}\n" \
            f"Icon={self._settings.appIconPath}\n"

        with self._desktopFilePath.open(mode='w') as fOutput:
            fOutput.write(desktopFileContent)
