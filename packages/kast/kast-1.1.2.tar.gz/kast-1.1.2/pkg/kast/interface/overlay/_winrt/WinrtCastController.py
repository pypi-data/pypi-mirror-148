#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import asyncio
from pathlib import Path
from typing import Tuple

from winrt import _winrt
from winrt.windows.foundation import Uri, TimeSpan
from winrt.windows.media import SystemMediaTransportControls, SystemMediaTransportControlsButtonPressedEventArgs, \
    SystemMediaTransportControlsButton, PlaybackPositionChangeRequestedEventArgs, MediaPlaybackType, \
    SystemMediaTransportControlsTimelineProperties, MediaPlaybackStatus
from winrt.windows.media.playback import MediaPlayer
from winrt.windows.storage import StorageFile
from winrt.windows.storage.streams import RandomAccessStreamReference

from kast.media.casting.CastController import CastController
from kast.media.casting.CastState import CastPlayerState
from kast.settings.Settings import Settings
from kast.utils.Loggable import Loggable
from kast.utils.chrono import Seconds, Milliseconds

# Workaround for COM thread configuration interference with PyQt:
_winrt.uninit_apartment()


class WinrtCastController(Loggable):

    def __init__(
        self,
        settings: Settings,
        castController: CastController
    ) -> None:
        self._settings = settings
        self._castController = castController

        self._mediaControls = mediaControls = self._createMediaControls()
        mediaControls.is_enabled = True

        mediaControls.add_button_pressed(lambda sender, args: self._onButtonPressed(sender=sender, args=args))
        mediaControls.add_playback_position_change_requested(lambda sender, args: self._onPositionChanged(sender=sender, args=args))

    def reload(self) -> None:
        self._updateControls()
        self._updateMetaData()
        self._updateTimeline()
        self._updatePlayerState()

    def _updateControls(self) -> None:
        enable = (not self._castController.castState.mediaState.isStopped())
        self._mediaControls.is_play_enabled = enable
        self._mediaControls.is_pause_enabled = enable
        self._mediaControls.is_stop_enabled = enable

    def _updateMetaData(self) -> None:
        title, subtitle = self._getTitleAndSubtitle()

        displayUpdater = self._mediaControls.display_updater
        displayUpdater.type = MediaPlaybackType.VIDEO
        displayUpdater.video_properties.title = title
        displayUpdater.video_properties.subtitle = subtitle
        displayUpdater.thumbnail = self._createThumbnailStream()

        displayUpdater.update()

    def _updateTimeline(self) -> None:
        mediaState = self._castController.castState.mediaState

        timelineProperties = SystemMediaTransportControlsTimelineProperties()
        timelineProperties.start_time = self._createTimeSpan()
        timelineProperties.min_seek_time = self._createTimeSpan()
        timelineProperties.position = self._createTimeSpan(mediaState.currentTime)
        timelineProperties.max_seek_time = self._createTimeSpan(mediaState.duration)
        timelineProperties.end_time = self._createTimeSpan(mediaState.duration)

        self._mediaControls.update_timeline_properties(timelineProperties)

    def _updatePlayerState(self) -> None:
        states = {
            CastPlayerState.Playing: MediaPlaybackStatus.PLAYING,
            CastPlayerState.Paused: MediaPlaybackStatus.PAUSED,
            CastPlayerState.Buffering: MediaPlaybackStatus.CHANGING,
            CastPlayerState.Idle: MediaPlaybackStatus.STOPPED,
            CastPlayerState.Unknown: MediaPlaybackStatus.CLOSED,
        }

        state = self._castController.castState.mediaState.playerState
        if state not in states:
            self.log.warning(f"Unhandled media player state change (state={state.name})!")
            return

        self._mediaControls.playback_status = states[state]

    def _onButtonPressed(
        self,
        sender: SystemMediaTransportControls,
        args: SystemMediaTransportControlsButtonPressedEventArgs
    ) -> None:
        button = SystemMediaTransportControlsButton(args.button)

        actions = {
            SystemMediaTransportControlsButton.PLAY: self._castController.play,
            SystemMediaTransportControlsButton.PAUSE: self._castController.pause,
            SystemMediaTransportControlsButton.STOP: self._castController.stop
        }

        if button not in actions:
            self.log.warning(f"Unhandled button press (button='{button.name}')!")
            return

        actions[button]()

    def _onPositionChanged(
        self,
        sender: SystemMediaTransportControls,
        args: PlaybackPositionChangeRequestedEventArgs
    ) -> None:
        position = Seconds(Milliseconds(args.requested_playback_position.duration))
        self._castController.seek(position)

    def _getTitleAndSubtitle(self) -> Tuple[str, str]:
        castState = self._castController.castState

        titles = []
        castState.mediaState.title and titles.append(castState.mediaState.title)
        titles.append(self._settings.appName + (f" ({castState.deviceName})" if castState.deviceName else ''))
        titles.append('')

        return titles[0], titles[1]

    def _createThumbnailStream(self) -> RandomAccessStreamReference:
        thumbnailUrl = self._castController.castState.mediaState.imageUrl or self._castController.castState.mediaState.iconUrl
        if thumbnailUrl:
            return RandomAccessStreamReference.create_from_uri(Uri(thumbnailUrl))

        return RandomAccessStreamReference.create_from_file(asyncio.run(self.openFile(self._settings.appIconPath)))

    @staticmethod
    def _createTimeSpan(seconds: Seconds = Seconds(0)) -> TimeSpan:
        return TimeSpan(Milliseconds(seconds).value)

    @staticmethod
    async def openFile(file: Path) -> StorageFile:
        return await StorageFile.get_file_from_path_async(str(file))

    @staticmethod
    def _createMediaControls() -> SystemMediaTransportControls:
        mediaPlayer = MediaPlayer()
        mediaPlayer.command_manager.is_enabled = False
        return mediaPlayer.system_media_transport_controls
