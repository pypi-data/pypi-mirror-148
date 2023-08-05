#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import logging
import logging.handlers
import os
import platform
import signal
import sys
import threading
import types
from typing import Callable

import setproctitle

from kast.utils.Loggable import Loggable

if os.name == 'posix':
    from kast.interface.qt5.KastQtApp import KastQtApp  # Must be imported before services (to avoid media player problem)!
    from kast.Services import Services

if os.name == 'nt':
    from kast.Services import Services  # Must be imported before Qt (to avoid WinRT problem)!
    from kast.interface.qt5.KastQtApp import KastQtApp


class KastApp(Loggable):

    def __init__(self, debug: bool = False) -> None:
        self._debug = debug
        self._services = Services()
        self._desktopApp = KastQtApp(services=self._services)

    def run(self) -> int:
        setproctitle.setproctitle(self._services.settings.appName)

        self._initLogger()

        signal.signal(signal.SIGTERM, self._onSignal)
        signal.signal(signal.SIGINT, self._onSignal)

        try:
            self.log.info(f"Platform: {platform.platform()}")
            self.log.info(f"Python: {sys.version}")
            self.log.info(f"Interpreter path: '{sys.executable}'")
            self.log.info(f"Application: {self._services.settings.appName} ({self._services.settings.appVersion})")
            self.log.info(f"Persistent storage path: '{self._services.settings.persistentStoragePath}'")
            self.log.info(f"Temporary storage path: '{self._services.settings.temporaryStoragePath}'")

            self._services.mediaServer.mediaContent.thumbnailFile = self._services.settings.appIconPath
            self._services.mediaServer.start()
            self._runAsThread(self._services.osMediaOverlay.run)
            return self._desktopApp.run()

        except Exception as ex:
            self.log.exception(ex)
            return 1

        finally:
            self._onExit()

    def _onSignal(self, signum: int, frame: types.FrameType) -> None:
        self.log.info(f"Caught signal: {signal.Signals(signum).name}")
        self._desktopApp.exit(1)

    def _onExit(self) -> None:
        self._services.castController.quit()
        self._services.mediaServer.stop()

    def _runAsThread(self, callback: Callable[[], None]) -> None:
        thr = threading.Thread(target=callback)
        thr.daemon = True
        thr.start()

    def _initLogger(self) -> None:
        logFormatter = logging.Formatter(
            fmt='[%(asctime)s][%(threadName)s][%(levelname)-8.8s][%(name)s]: %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.INFO)

        fileHandler = logging.handlers.RotatingFileHandler(
            filename=self._services.settings.logFilePath,
            maxBytes=(5 * 1_000_000),
            backupCount=3
        )
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        if self._debug:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)
            rootLogger.addHandler(consoleHandler)
