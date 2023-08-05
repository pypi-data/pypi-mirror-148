#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtDBus import QDBusConnection, QDBusMessage
from PyQt5.QtGui import QWindow

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.service.UiEvent import UiEvent, UiState
from kast.interface.qt5.viewModel.taskbar.TaskbarViewModelBase import TaskbarViewModelBase
from kast.media.casting.CastState import CastMediaState


class UnityTaskbarViewModel(TaskbarViewModelBase):

    def __init__(self, parent: QWindow, uiServices: UiServices) -> None:
        super().__init__(parent, uiServices)
        self.uiServices.uiEventObserver.register(self, self._onUiEvent)

        self._displayProgress(False)

    @property
    def _mediaState(self) -> CastMediaState:
        return self.uiServices.uiStateService.castState.mediaState

    def _onUiEvent(self, uiEvent: UiEvent) -> None:
        self._updateProgress(uiEvent)

    def _updateProgress(self, uiEvent: UiEvent) -> None:
        if not uiEvent.progress.complete:
            percentage = uiEvent.progress.percentage
            percentage = percentage/100 if percentage is not None else 1.0
            self._displayProgress(True, percentage)
            return

        duration = int(self._mediaState.duration)
        if (uiEvent.state == UiState.Streaming) and (duration > 0):
            self._displayProgress(True, int(self._mediaState.currentTime)/duration)
            return

        self._displayProgress(False)

    def _displayProgress(self, display: bool, percentage: float = 0.0) -> None:
        self._sendMessage({
            'progress': percentage,
            'progress-visible': display
        })

    def _sendMessage(self, parameters: dict) -> None:
        message = QDBusMessage.createSignal('/', 'com.canonical.Unity.LauncherEntry', 'Update')
        message << f'application://{self.services.settings.desktopFileName}'
        message << parameters
        QDBusConnection.sessionBus().send(message)
