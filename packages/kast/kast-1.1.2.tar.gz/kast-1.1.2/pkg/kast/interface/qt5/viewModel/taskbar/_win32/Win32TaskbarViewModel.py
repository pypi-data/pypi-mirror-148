#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton, QWinTaskbarButton

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.service.UiEvent import UiEvent, UiState
from kast.interface.qt5.viewModel.taskbar.TaskbarViewModelBase import TaskbarViewModelBase
from kast.media.casting.CastState import CastMediaState


class Win32TaskbarViewModel(TaskbarViewModelBase):

    def __init__(
        self,
        parent: QWindow,
        uiServices: UiServices
    ) -> None:
        super().__init__(parent, uiServices)
        self.uiServices.uiEventObserver.register(self, self._onUiEvent)

        self._mediaControls = mediaControls = []

        self._taskbarToolbar = taskbarToolbar = QWinThumbnailToolBar(parent)
        taskbarToolbar.setWindow(parent.windowHandle())

        self._taskbarButtonPlayOrPause = buttonPlayOrPause = QWinThumbnailToolButton(taskbarToolbar)
        buttonPlayOrPause.setToolTip('Play/Pause')
        buttonPlayOrPause.setIcon(parent.style().standardIcon(QStyle.SP_MediaPlay))
        mediaControls.append(buttonPlayOrPause)

        self._taskbarButtonStop = buttonStop = QWinThumbnailToolButton(taskbarToolbar)
        buttonStop.setToolTip('Stop')
        buttonStop.setIcon(parent.style().standardIcon(QStyle.SP_MediaStop))
        mediaControls.append(buttonStop)

        self._taskbarButtonSeekForward = buttonSeekForward = QWinThumbnailToolButton(taskbarToolbar)
        buttonSeekForward.setToolTip('Seek forward')
        buttonSeekForward.setIcon(parent.style().standardIcon(QStyle.SP_MediaSeekForward))
        mediaControls.append(buttonSeekForward)

        self._taskbarButtonSeekBackward = buttonSeekBackward = QWinThumbnailToolButton(taskbarToolbar)
        buttonSeekBackward.setToolTip('Seek backward')
        buttonSeekBackward.setIcon(parent.style().standardIcon(QStyle.SP_MediaSeekBackward))
        mediaControls.append(buttonSeekBackward)

        self._taskbarIcon = taskbarIcon = QWinTaskbarButton(parent)
        taskbarIcon.setWindow(parent.windowHandle())
        self._taskbarProgress = taskbarIcon.progress()

        taskbarToolbar.addButton(buttonSeekBackward)
        taskbarToolbar.addButton(buttonPlayOrPause)
        taskbarToolbar.addButton(buttonStop)
        taskbarToolbar.addButton(buttonSeekForward)

        self._enableControls(False)

        buttonPlayOrPause.clicked.connect(self._signalButtonPlayOrPause)
        buttonStop.clicked.connect(self._signalButtonStop)
        buttonSeekForward.clicked.connect(self._signalButtonSeekForward)
        buttonSeekBackward.clicked.connect(self._signalButtonSeekBackward)

    @property
    def _mediaState(self) -> CastMediaState:
        return self.uiServices.uiStateService.castState.mediaState

    def _onUiEvent(self, uiEvent: UiEvent) -> None:
        isStreaming = uiEvent.state == UiState.Streaming
        self._enableControls(isStreaming)

        iconPlayPause = QStyle.SP_MediaPause if self._mediaState.isPlaying() else QStyle.SP_MediaPlay
        self._taskbarButtonPlayOrPause.setIcon(self._parent.style().standardIcon(iconPlayPause))

        self._updateProgress(uiEvent)

    def _signalButtonPlayOrPause(self) -> None:
        self.uiServices.mediaControlService.playOrPause()

    def _signalButtonStop(self) -> None:
        self.uiServices.mediaControlService.stop()

    def _signalButtonSeekForward(self) -> None:
        self.uiServices.mediaControlService.seekForward()

    def _signalButtonSeekBackward(self) -> None:
        self.uiServices.mediaControlService.seekBackward()

    def _enableControls(self, enable: bool = True) -> None:
        for control in self._mediaControls:
            control.setEnabled(enable)

    def _updateProgress(self, uiEvent: UiEvent) -> None:
        if not uiEvent.progress.complete:
            percentage = uiEvent.progress.percentage
            vMax, vCur = (100, percentage) if percentage is not None else (0, 0)
            self._displayProgress(maximum=vMax, value=vCur)
            return

        duration = int(self._mediaState.duration)
        if (uiEvent.state == UiState.Streaming) and (duration > 0):
            self._displayProgress(maximum=duration, value=int(self._mediaState.currentTime))
            return

        self._taskbarProgress.setVisible(False)

    def _displayProgress(self, maximum: int, value: int) -> None:
        self._taskbarProgress.setRange(0, maximum)
        self._taskbarProgress.setValue(value)
        self._taskbarProgress.setVisible(True)
