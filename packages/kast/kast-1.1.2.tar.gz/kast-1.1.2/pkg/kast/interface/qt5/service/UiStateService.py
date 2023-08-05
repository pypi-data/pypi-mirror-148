#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import copy

from kast.interface.qt5.service.InterfaceScheduler import InterfaceScheduler
from kast.interface.qt5.service.UiEvent import UiEvent, UiState
from kast.interface.qt5.service.UiEventObserver import UiEventObserver
from kast.media.casting.CastEventObserver import CastEventObserver
from kast.media.casting.CastState import CastState
from kast.utils.Loggable import Loggable


class UiStateService(Loggable):

    def __init__(
        self,
        interfaceScheduler: InterfaceScheduler,
        uiEventObserver: UiEventObserver,
        castEventObserver: CastEventObserver
    ) -> None:
        self._interfaceScheduler = interfaceScheduler
        self._uiEventObserver = uiEventObserver
        self._castEventObserver = castEventObserver

        self._uiEvent = UiEvent()
        self._castState = CastState()

        self._castEventObserver.register(listener=self, callback=self._onCastEvent)

    @property
    def uiEvent(self):
        return self._uiEvent

    @property
    def castState(self) -> CastState:
        return self._castState

    def dispatch(self, uiEvent: UiEvent, synchronous: bool = False) -> None:
        def interfaceCallback() -> None:
            self._uiEvent = uiEvent
            self._dispatch()

        if synchronous:
            interfaceCallback()
            return

        self._interfaceScheduler.schedule(interfaceCallback)

    def _onCastEvent(self, event: CastState) -> None:
        def interfaceCallback() -> None:
            self._castState = copy.deepcopy(event)
            self._updateUiState()
            self._dispatch()
        self._interfaceScheduler.schedule(interfaceCallback)

    def _updateUiState(self) -> None:
        if (self._uiEvent.state == UiState.Streaming) and (not self._castState.isConnectedOrRecoverable()):
            self._uiEvent = UiEvent(UiState.Idle)
            return

        if (self._uiEvent.state == UiState.Idle) and self._castState.isConnectedOrRecoverable():
            self._uiEvent = UiEvent(UiState.Streaming)
            return

    def _dispatch(self) -> None:
        self.log.info(
            f"UiState={self.uiEvent.state.name}, "
            f"DeviceState={self.castState.connection.value.lower().capitalize()}, "
            f"MediaState={self.castState.mediaState.playerState.value.lower().capitalize()}"
        )

        self._uiEventObserver.notify(self._uiEvent)
