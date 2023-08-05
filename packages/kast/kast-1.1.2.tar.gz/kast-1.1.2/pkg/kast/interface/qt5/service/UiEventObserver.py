#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Any, Callable, Dict

from kast.interface.qt5.service.UiEvent import UiEvent
from kast.utils.Loggable import Loggable


class UiEventObserver(Loggable):

    Callback = Callable[[UiEvent], None]

    def __init__(self) -> None:
        self._listeners: Dict[Any, UiEventObserver.Callback] = {}

    def register(self, listener: Any, callback: Callback) -> None:
        self._listeners[listener] = callback

    def unregister(self, listener: Any) -> None:
        if listener in self._listeners.keys():
            self._listeners.pop(listener)

    def notify(self, uiEvent: UiEvent) -> None:
        for callback in self._listeners.values():
            callback(uiEvent)
