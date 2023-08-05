#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

from kast.interface.qt5.service.BackgroundRunner import BackgroundRunner
from kast.interface.qt5.service.InterfaceScheduler import InterfaceScheduler

Callback = Callable[[], None]


@dataclass
class Schedulers:
    interfaceScheduler: InterfaceScheduler
    backgroundRunner: BackgroundRunner


class ISchedulable(ABC):
    @property
    @abstractmethod
    def schedulers(self) -> Schedulers:
        """Should return schedulers object."""

    @abstractmethod
    def backgroundTaskMiddleware(self, callback: Callback) -> None:
        """Should directly call callback. Can be used to wrap with try clause to handle errors."""


class SchedulableBase(ISchedulable, ABC):
    def backgroundTaskMiddleware(self, callback: Callback) -> None:
        callback()


class Schedulable(SchedulableBase):

    def __init__(
        self,
        interfaceScheduler: InterfaceScheduler,
        backgroundRunner: BackgroundRunner
    ) -> None:
        self.__schedulers = Schedulers(
            interfaceScheduler,
            backgroundRunner
        )

    @property
    def schedulers(self) -> Schedulers:
        return self.__schedulers
