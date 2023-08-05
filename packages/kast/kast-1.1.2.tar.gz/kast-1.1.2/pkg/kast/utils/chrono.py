#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from __future__ import annotations  # TODO: Remove when support dropped for: Python < 3.10

from dataclasses import dataclass
from functools import total_ordering
from math import floor
from typing import Optional, Union


class TimeUnitTypeError(TypeError):
    pass


@total_ordering
class TimeUnit:

    ConvFactor = float
    NumericValue = int

    DEFAULT_VALUE = 0

    @staticmethod
    def Value() -> Union:
        return Union[int, float, TimeUnit]

    @dataclass(frozen=True)
    class Params:
        name: str
        convFactor: TimeUnit.ConvFactor

    class Type:

        def __init__(self, name: str, convFactor: TimeUnit.ConvFactor) -> None:
            self._timeUnit = TimeUnit(params=TimeUnit.Params(name=name, convFactor=convFactor))

        def __call__(self, value: Optional[TimeUnit.Value()] = None) -> TimeUnit:
            return self._timeUnit(value=value)

        @property
        def convFactor(self):
            return self._timeUnit.convFactor

    def __init__(
        self,
        params: Params,
        value: Optional[TimeUnit.Value()] = None
    ) -> None:
        value = value if value is not None else self.DEFAULT_VALUE

        self._params = params
        self._value = self._convertValue(value)

    def __call__(self, value: Optional[TimeUnit.Value()] = None) -> TimeUnit:
        return TimeUnit(params=self._params, value=value)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return f"{self.name}({self.value})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.name}={self.value}) at {hex(id(self))}>"

    def __add__(self, other: Value()) -> TimeUnit:
        if isinstance(other, int):
            return TimeUnit(params=self._params, value=(self.value + other))

        if isinstance(other, TimeUnit):
            return TimeUnit(params=self._params, value=(self.value + self._convertValue(other)))

        raise TimeUnitTypeError(f"Cannot increase '{self.name}' with '{type(other).__name__}'!")

    def __sub__(self, other: Value()) -> TimeUnit:
        return self.__add__(-other)

    def __neg__(self) -> TimeUnit:
        return TimeUnit(params=self._params, value=(-self.value))

    def __eq__(self, other: Value()) -> bool:
        return self.value == self._convertValue(other)

    def __gt__(self, other: Value()) -> bool:
        return self.value > self._convertValue(other)

    @property
    def name(self) -> str:
        return self._params.name

    @property
    def convFactor(self) -> ConvFactor:
        return self._params.convFactor

    @property
    def value(self) -> NumericValue:
        return self._value

    def _convertValue(self, value: Value()) -> NumericValue:
        if not isinstance(value, self.Value().__args__):
            raise TimeUnitTypeError(f"Cannot create '{self._params.name}' from '{type(value).__name__}'!")

        if isinstance(value, TimeUnit):
            return int(floor(value.value * value.convFactor / self.convFactor))

        return int(floor(value))


Seconds = TimeUnit.Type(name='Seconds', convFactor=1)

Milliseconds = TimeUnit.Type(name='Milliseconds', convFactor=(Seconds.convFactor / 1_000))
Microseconds = TimeUnit.Type(name='Microseconds', convFactor=(Milliseconds.convFactor / 1_000))
Nanoseconds = TimeUnit.Type(name='Nanoseconds', convFactor=(Microseconds.convFactor / 1_000))

Minutes = TimeUnit.Type(name='Minutes', convFactor=(60 * Seconds.convFactor))
Hours = TimeUnit.Type(name='Hours', convFactor=(60 * Minutes.convFactor))
Days = TimeUnit.Type(name='Days', convFactor=(24 * Hours.convFactor))
Weeks = TimeUnit.Type(name='Weeks', convFactor=(7 * Days.convFactor))
