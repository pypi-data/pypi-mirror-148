#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QStyle, QWidget

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.service.UiEvent import UiEvent, UiState
from kast.interface.qt5.view.MediaControlView import Ui_MediaControlView
from kast.interface.qt5.viewModel.VideoPreviewViewModel import VideoPreviewViewModel
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase
from kast.media.casting.CastState import CastMediaState, CastPlayerState, CastState, Seconds
from kast.utils.chrono import Milliseconds


class View(ViewBase, QWidget, Ui_MediaControlView):
    pass


class MediaControlViewModel(ViewModelBase):

    def __init__(
        self,
        parent: QWidget,
        uiServices: UiServices,
        videoPreviewViewModel: VideoPreviewViewModel
    ) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)
        self.uiServices.uiEventObserver.register(self, self._onUiEvent)

        self._videoPreviewViewModel = videoPreviewViewModel
        self._videoPreviewViewModel.setMuteCallback(self._onLocalMute)
        self._videoPreviewViewModel.setVolumeCallback(self._onLocalVolume)

        self._view.buttonPlayPause.setIcon(self._view.style().standardIcon(QStyle.SP_MediaPlay))
        self._view.buttonStop.setIcon(self._view.style().standardIcon(QStyle.SP_MediaStop))
        self._view.buttonSeekFront.setIcon(self._view.style().standardIcon(QStyle.SP_MediaSeekForward))
        self._view.buttonSeekBack.setIcon(self._view.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self._view.buttonMuteRemote.setIcon(self._view.style().standardIcon(QStyle.SP_MediaVolume))
        self._view.buttonMuteLocal.setIcon(self._view.style().standardIcon(QStyle.SP_MediaVolume))

        self._videoPositionUpdater = QTimer()
        self._videoPositionUpdater.setInterval(int(Milliseconds(Seconds(1))))
        self._videoPositionUpdater.timeout.connect(self._signalVideoPositionUpdate)
        self._videoPositionUpdater.start()

        self._view.buttonDisconnect.clicked.connect(self._signalClickedDisconnect)
        self._view.buttonPlayPause.clicked.connect(self._signalClickedPlayPause)
        self._view.buttonStop.clicked.connect(self._signalClickedStop)
        self._view.buttonSeekFront.clicked.connect(self._signalClickedSeekForward)
        self._view.buttonSeekBack.clicked.connect(self._signalClickedSeekBackward)
        self._view.buttonMuteRemote.clicked.connect(self._signalClickedMuteRemote)
        self._view.buttonMuteLocal.clicked.connect(self._signalClickedMuteLocal)

        self._view.sliderSeek.sliderReleased.connect(self._signalSeekPosition)
        self._view.sliderVolumeRemote.sliderReleased.connect(self._signalSetVolumeRemote)
        self._view.sliderVolumeLocal.sliderReleased.connect(self._signalSetVolumeLocal)

        self._view.setVisible(False)

    @property
    def _castState(self) -> CastState:
        return self.uiServices.uiStateService.castState

    @property
    def _mediaState(self) -> CastMediaState:
        return self._castState.mediaState

    def _onUiEvent(self, uiEvent: UiEvent) -> None:
        isStreaming = uiEvent.state == UiState.Streaming
        self._view.setVisible(isStreaming)
        self._videoPreviewViewModel.enable(state=isStreaming)
        self._videoPreviewViewModel.setPlayerState(state=self._mediaState.playerState)

        if uiEvent.state == UiState.Closing:
            self._videoPreviewViewModel.cleanup()

        iconPlayPause = QStyle.SP_MediaPause if self._mediaState.isPlaying() else QStyle.SP_MediaPlay
        self._view.buttonPlayPause.setIcon(self._view.style().standardIcon(iconPlayPause))

        self._updateVideoPosition(position=self._mediaState.currentTime, duration=self._mediaState.duration)

        volumeLevel = int(round(self._mediaState.volumeLevel * 100))
        self._view.sliderVolumeRemote.setSliderPosition(volumeLevel)

        iconMuted = QStyle.SP_MediaVolumeMuted if self._mediaState.volumeMuted or volumeLevel == 0 else QStyle.SP_MediaVolume
        self._view.buttonMuteRemote.setIcon(self._view.style().standardIcon(iconMuted))

    def _onLocalMute(self, muted: bool) -> None:
        iconMuted = QStyle.SP_MediaVolumeMuted if muted else QStyle.SP_MediaVolume
        self._view.buttonMuteLocal.setIcon(self._view.style().standardIcon(iconMuted))

    def _onLocalVolume(self, volume: int) -> None:
        self._view.sliderVolumeLocal.setValue(volume)

    def _updateVideoPosition(self, position: Seconds, duration: Seconds) -> None:
        def formatTime(seconds: Seconds) -> str:
            return time.strftime('%H:%M:%S', time.gmtime(seconds.value))

        self._view.labelTime.setText(f"{formatTime(position)} / {formatTime(duration)}")

        self._view.sliderSeek.setRange(0, duration.value)
        self._view.sliderSeek.setSliderPosition(position.value)

        self._videoPreviewViewModel.updateVideoPosition(position=position)

    def _signalVideoPositionUpdate(self) -> None:
        if self._mediaState.playerState == CastPlayerState.Playing:
            self._updateVideoPosition(
                position=self._mediaState.currentTime,
                duration=self._mediaState.duration
            )

    def _signalClickedDisconnect(self) -> None:
        self.services.castController.quit()
        self.services.castController.disconnect()

    def _signalClickedPlayPause(self) -> None:
        self.uiServices.mediaControlService.playOrPause()

    def _signalClickedStop(self) -> None:
        self.uiServices.mediaControlService.stop()

    def _signalClickedSeekForward(self) -> None:
        self.uiServices.mediaControlService.seekForward()

    def _signalClickedSeekBackward(self) -> None:
        self.uiServices.mediaControlService.seekBackward()

    def _signalSeekPosition(self) -> None:
        self.uiServices.mediaControlService.seek(Seconds(self._view.sliderSeek.value()))

    def _signalClickedMuteRemote(self) -> None:
        self.uiServices.mediaControlService.setMute(not self._mediaState.volumeMuted)

    def _signalSetVolumeRemote(self) -> None:
        self.uiServices.mediaControlService.setVolume(self._view.sliderVolumeRemote.value()/100)

    def _signalClickedMuteLocal(self) -> None:
        self._videoPreviewViewModel.muted = not self._videoPreviewViewModel.muted

    def _signalSetVolumeLocal(self) -> None:
        self._videoPreviewViewModel.volume = self._view.sliderVolumeLocal.value()
