#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import shutil
import tempfile
import threading
from pathlib import Path

from kast import __app_name__, __version__, __author__, __email__, __package_name__
from kast.settings.SettingsEventObserver import SettingsEventObserver
from kast.settings.SettingsState import SettingsState
from kast.utils.ResourceProvider import ResourceProvider


class Settings:

    def __init__(
        self,
        resourceProvider: ResourceProvider,
        settingsEventObserver: SettingsEventObserver
    ) -> None:
        self._resourceProvider = resourceProvider
        self._settingsEventObserver = settingsEventObserver

        self._persistentStoragePath = Path.home().joinpath(f".config/{__package_name__}")
        self._persistentStoragePath.mkdir(parents=True, exist_ok=True)
        self._settingsStateFilePath = self._persistentStoragePath.joinpath('settings.json')
        self._temporaryStorage = tempfile.TemporaryDirectory(prefix=f"{__package_name__}-")

        self._lock = threading.Lock()
        self._settingsState = SettingsState()

        self._load()
        self._cleanupArtifacts()

    @property
    def author(self) -> str:
        return __author__

    @property
    def email(self) -> str:
        return __email__

    @property
    def package(self) -> str:
        return __package_name__

    @property
    def appName(self) -> str:
        return __app_name__

    @property
    def appVersion(self) -> str:
        return __version__

    @property
    def desktopFileName(self) -> str:
        return f'{__package_name__}.desktop'

    @property
    def persistentStoragePath(self) -> Path:
        return self._persistentStoragePath

    @property
    def temporaryStoragePath(self) -> Path:
        return Path(self._temporaryStorage.name)

    @property
    def logFilePath(self) -> Path:
        return self.persistentStoragePath.joinpath(f"{self.package}.log")

    @property
    def appIconPath(self) -> Path:
        return self._resourceProvider.getResourcePath(Path('appicon.png'))

    @property
    def browseMediaDir(self) -> Path:
        with self._lock:
            return Path(self._settingsState.browseMediaPath)

    @browseMediaDir.setter
    def browseMediaDir(self, value: Path) -> None:
        with self._lock:
            self._settingsState.browseMediaPath = str(value)
        self._notify()

    def _notify(self) -> None:
        self._settingsEventObserver.notify(event=self._settingsState)
        self._save()

    def _cleanupArtifacts(self) -> None:
        if self._settingsState.previousTemporaryPath and Path(self._settingsState.previousTemporaryPath).exists():
            shutil.rmtree(self._settingsState.previousTemporaryPath)

        self._settingsState.previousTemporaryPath = str(self.temporaryStoragePath)

    def _load(self) -> None:
        with self._lock:
            if self._settingsStateFilePath.is_file() and self._settingsStateFilePath.stat().st_size:
                with self._settingsStateFilePath.open() as fInput:
                    self._settingsState = SettingsState.from_json(fInput.read())

    def _save(self) -> None:
        with self._lock:
            with self._settingsStateFilePath.open(mode='w') as fOutput:
                fOutput.write(self._settingsState.to_json())
