#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from enum import Enum
from typing import Callable, Optional

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.view.VideoPreviewView import Ui_VideoPreviewView
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase
from kast.media.casting.CastState import CastPlayerState, Seconds
from kast.utils.Loggable import Loggable
from kast.utils.chrono import Milliseconds

MuteCallback = Callable[[bool], None]
VolumeCallback = Callable[[int], None]


class View(ViewBase, QWidget, Ui_VideoPreviewView):
    pass


class VideoPreviewViewModel(Loggable, ViewModelBase):

    POSITION_DELTA = 1

    def __init__(self, parent: QWidget, uiServices: UiServices) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)

        self._lastPlayerState = CastPlayerState.Unknown
        self._muteCallback: Optional[MuteCallback] = None
        self._volumeCallback: Optional[VolumeCallback] = None

        self._view.labelImageLogo.setPixmap(QPixmap(str(self.services.settings.appIconPath)))

        self._videoWidget = QVideoWidget(self._view)
        self._videoWidget.setVisible(False)

        self._view.layoutPreview.addWidget(self._videoWidget)

        self._mediaPlayer: Optional[QMediaPlayer] = None

        self._resetMediaPlayer()

    def _resetMediaPlayer(self, init: bool = True) -> None:
        if self._mediaPlayer is not None:
            self._mediaPlayer.setMedia(QMediaContent())
            self._mediaPlayer.setVideoOutput(None)
            self._mediaPlayer.deleteLater()

        if not init:
            return

        self._mediaPlayer = QMediaPlayer(self._view, QMediaPlayer.VideoSurface)
        self._mediaPlayer.setVideoOutput(self._videoWidget)

        self._mediaPlayer.error.connect(self._signalOnMediaPlayerError)
        self._mediaPlayer.mutedChanged.connect(self._signalOnMuted)
        self._mediaPlayer.volumeChanged.connect(self._signalOnVolume)

        self._mediaPlayer.setMuted(True)

    @property
    def muted(self) -> bool:
        return self._mediaPlayer.isMuted()

    @muted.setter
    def muted(self, value: bool) -> None:
        self._mediaPlayer.setMuted(value)

    @property
    def volume(self) -> int:
        return self._mediaPlayer.volume()

    @volume.setter
    def volume(self, value: int) -> None:
        self._mediaPlayer.setVolume(value)

    def setMuteCallback(self, callback: MuteCallback) -> None:
        self._muteCallback = callback

    def setVolumeCallback(self, callback: VolumeCallback) -> None:
        self._volumeCallback = callback

    def cleanup(self) -> None:
        self._resetMediaPlayer(init=False)

    def enable(self, state: bool) -> None:
        self._view.labelImageLogo.setVisible(not state)
        self._videoWidget.setVisible(state)

        self._reloadMedia(enabled=state)

    def setPlayerState(self, state: CastPlayerState) -> None:
        if not self._hasMedia() or state == self._lastPlayerState:
            return
        self._lastPlayerState = state

        if state == CastPlayerState.Playing:
            self._mediaPlayer.play()
            return

        if state in [CastPlayerState.Buffering, CastPlayerState.Paused]:
            self._mediaPlayer.pause()
            return

        self._mediaPlayer.stop()

    def updateVideoPosition(self, position: Seconds) -> None:
        if not self._hasMedia():
            return

        previewPosition = Seconds(Milliseconds(self._mediaPlayer.position()))
        if int(previewPosition) not in self._designateAcceptablePositionRange(position):
            self.log.info(f"Updating preview position: {previewPosition} -> {position}")
            self._mediaPlayer.setPosition(Milliseconds(position).value)

    def _designateAcceptablePositionRange(self, position: Seconds) -> range:
        return range(
            int(position) - self.POSITION_DELTA,
            int(position) + self.POSITION_DELTA + 1
        )

    def _reloadMedia(self, enabled: bool) -> None:
        if(
            (enabled and not self._hasMedia()) or
            (not enabled and self._hasMedia())
        ):
            self.log.info("Reloading a media content.")
            self._resetMediaPlayer()

            if enabled:
                mediaContent = QMediaContent(QUrl.fromLocalFile(str(self.services.mediaServer.mediaContent.movieFile)))
                self._mediaPlayer.setMedia(mediaContent)

    def _hasMedia(self) -> bool:
        return not self._mediaPlayer.media().isNull()

    def _signalOnMediaPlayerError(self) -> None:
        self.log.error(f"Media player error: {mediaPlayerErrorToStr(self._mediaPlayer.error())}")

    def _signalOnMuted(self, muted: bool) -> None:
        self._muteCallback and self._muteCallback(muted)

    def _signalOnVolume(self, volume: int) -> None:
        self._volumeCallback and self._volumeCallback(volume)


def mediaPlayerErrorToStr(errorCode: int) -> str:
    class Error(Enum):
        NoError = QMediaPlayer.NoError
        ResourceError = QMediaPlayer.ResourceError
        FormatError = QMediaPlayer.FormatError
        NetworkError = QMediaPlayer.NetworkError
        AccessDeniedError = QMediaPlayer.AccessDeniedError
        ServiceMissingError = QMediaPlayer.ServiceMissingError

    if errorCode not in set(er.value for er in Error):
        return f'Unknown({errorCode})'

    return Error(errorCode).name
