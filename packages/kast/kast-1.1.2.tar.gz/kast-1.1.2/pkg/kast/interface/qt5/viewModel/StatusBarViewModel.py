#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import threading
import time
from typing import Optional

from PyQt5.QtWidgets import QStyle, QWidget

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.utils.dialogs import DialogQuestion
from kast.interface.qt5.service.UiEvent import UiEvent, UiState
from kast.interface.qt5.view.StatusBarView import Ui_StatusBarView
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase


class View(ViewBase, QWidget, Ui_StatusBarView):
    pass


class StatusBarViewModel(ViewModelBase):

    def __init__(self, parent: QWidget, uiServices: UiServices) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)
        self.uiServices.uiEventObserver.register(self, self._onUiEvent)

        self._cancelEvent: Optional[threading.Event] = None
        self._cancelMsgBox: Optional[DialogQuestion] = None
        self._taskStartTime: Optional[float] = None

        self._view.buttonCancel.setIcon(self._view.style().standardIcon(QStyle.SP_BrowserStop))
        self._view.widgetProgress.setVisible(False)

        self._view.buttonCancel.clicked.connect(self._signalClickedCancel)

    def _onUiEvent(self, uiEvent: UiEvent) -> None:
        if uiEvent.state == UiState.Closing:
            self._cancelTask()

        self._view.labelStatusMessage.setText(self._createStatusMessage(uiEvent=uiEvent))
        self._updateProgressArea(uiEvent=uiEvent)

    def _updateProgressArea(self, uiEvent: UiEvent) -> None:
        self._view.widgetProgress.setVisible(not uiEvent.progress.complete)

        self._cancelEvent = uiEvent.progress.cancelEvent
        self._view.buttonCancel.setEnabled(self._cancelEvent is not None)

        if uiEvent.progress.complete:
            self._dismissCancelMessageBox()
            return

        vMin, vMax, vCur = (0, 100, uiEvent.progress.percentage) if uiEvent.progress.percentage is not None else (0, 0, 0)
        self._view.progressBar.setRange(vMin, vMax)
        self._view.progressBar.setValue(vCur)

    def _signalClickedCancel(self) -> None:
        try:
            self._cancelMsgBox = DialogQuestion(title="Abort", message="Do you really want to abort current background task?")
            if not self._cancelMsgBox.display():
                return

            self._cancelTask()

        finally:
            self._cancelMsgBox = None

    def _dismissCancelMessageBox(self) -> None:
        self._cancelMsgBox and self._cancelMsgBox.dismiss()

    def _cancelTask(self) -> None:
        self._cancelEvent is not None and self._cancelEvent.set()

    def _createStatusMessage(self, uiEvent: UiEvent) -> str:
        if uiEvent.state == UiState.Streaming:
            playerState = self.uiServices.uiStateService.castState.mediaState.playerState
            return f"{uiEvent.state.value} ({playerState.value.lower().capitalize()})"

        remainingEstimateMessage = self._createRemainingEstimateMessage(uiEvent=uiEvent)
        remainingEstimateMessage = f" (Remaining estimate: {remainingEstimateMessage})" if remainingEstimateMessage else ''

        return uiEvent.state.value + remainingEstimateMessage

    def _createRemainingEstimateMessage(self, uiEvent: UiEvent) -> Optional[str]:
        if uiEvent.progress.complete or not uiEvent.progress.percentage:
            self._taskStartTime = None
            return None

        if self._taskStartTime is None:
            self._taskStartTime = time.time()
            return None

        duration = time.time() - self._taskStartTime
        percentage = uiEvent.progress.percentage
        estimate = (duration / percentage) * (100 - percentage)
        return time.strftime('%H:%M:%S', time.gmtime(estimate))
