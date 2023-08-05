#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Any, Callable, Dict

from kast.media.casting.CastState import CastState
from kast.utils.Loggable import Loggable


class CastEventObserver(Loggable):

    Callback = Callable[[CastState], None]

    def __init__(self) -> None:
        self._listeners: Dict[Any, CastEventObserver.Callback] = {}

    def register(self, listener: Any, callback: Callback) -> None:
        self._listeners[listener] = callback

    def unregister(self, listener: Any) -> None:
        if listener in self._listeners.keys():
            self._listeners.pop(listener)

    def notify(self, event: CastState) -> None:
        for callback in self._listeners.values():
            callback(event)
