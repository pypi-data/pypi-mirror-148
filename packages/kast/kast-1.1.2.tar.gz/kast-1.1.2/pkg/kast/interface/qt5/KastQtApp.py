#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import os
import platform
import sys

from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from kast.Services import Services
from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.service.UiEvent import UiEvent, UiState, Progress
from kast.interface.qt5.viewModel.MainWindowViewModel import MainWindowViewModel
from kast.utils.Loggable import Loggable


class KastQtApp(Loggable):

    def __init__(self, services: Services) -> None:
        self._setupQt()
        self._app = QApplication(sys.argv)
        self._uiServices = UiServices(services)

        self._app.setWindowIcon(QIcon(str(services.settings.appIconPath)))
        self._setupPlatform()

        self._mainWindowViewModel = MainWindowViewModel(uiServices=self._uiServices)

        self._app.aboutToQuit.connect(self._onExit)

    def run(self) -> int:
        self.log.info(f"PyQt: {Qt.PYQT_VERSION_STR}, Qt: {Qt.QT_VERSION_STR}")
        return self._app.exec()

    def exit(self, returnCode: int = 0) -> None:
        self._app.closeAllWindows()
        self._app.exit(returnCode)

    def _onExit(self) -> None:
        self.log.info("Interface exit.")
        self._uiServices.uiEventObserver.notify(UiEvent(state=UiState.Closing, progress=Progress(complete=False)))

    def _setupPlatform(self) -> None:
        """Platform specific setup. Should be run after QApplication creation."""

        if platform.system() == 'Linux':
            self._app.setDesktopFileName(self._uiServices.services.settings.desktopFileName)

    @staticmethod
    def _setupQt() -> None:
        """Qt framework setup. Should be run before QApplication creation."""

        # On windows default backend for media support is 'directshow'.
        # Which does not provide support for proprietary codecs like 'h264'.
        # We could change to 'windowsmediafoundation' backend instead.
        # Unfortunately this setup will only work for Qt>=5.15.5.
        # Workaround for older versions is to install a codec pack.
        if os.name == 'nt':
            os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
