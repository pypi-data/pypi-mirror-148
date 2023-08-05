#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtGui import QWindow

from kast.Services import Services
from kast.interface.qt5.UiServices import UiServices


class TaskbarViewModelBase:

    def __init__(
        self,
        parent: QWindow,
        uiServices: UiServices
    ) -> None:
        self._parent = parent
        self._uiServices = uiServices

    @property
    def services(self) -> Services:
        return self._uiServices.services

    @property
    def uiServices(self) -> UiServices:
        return self._uiServices
