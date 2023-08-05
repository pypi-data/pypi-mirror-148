#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import sys
from typing import Callable

from PyQt5.QtCore import QRunnable, QThreadPool

from kast.interface.qt5.service.InterfaceScheduler import InterfaceScheduler
from kast.interface.qt5.utils.dialogs import dialogCriticalError
from kast.utils.Loggable import Loggable

Callback = Callable[[], None]


class Worker(Loggable, QRunnable):

    def __init__(self, interfaceScheduler: InterfaceScheduler, callback: Callback) -> None:
        super().__init__()
        self._interfaceScheduler = interfaceScheduler
        self._callback = callback

    def run(self) -> None:
        try:
            self._callback()
        except Exception as ex:
            self.log.critical(f"Unhandled error in background task! Exception: {ex}", exc_info=True)

            def notifyCritical() -> None:
                try:
                    message = "Application encountered a CRITICAL error!" \
                          "\n(Shutting down due to high severity.)"
                    dialogCriticalError(message=message)
                finally:
                    sys.exit(1)

            self._interfaceScheduler.schedule(notifyCritical)


class BackgroundRunner:

    def __init__(self, interfaceScheduler: InterfaceScheduler) -> None:
        self._interfaceScheduler = interfaceScheduler
        self._threadPool = QThreadPool()

    def execute(self, callback: Callback) -> None:
        self._threadPool.start(Worker(interfaceScheduler=self._interfaceScheduler, callback=callback))
