#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_server.base import Microseconds

import kast.utils.chrono as chrono


def castTimeToMprisTime(value: chrono.Seconds) -> Microseconds:
    return chrono.Microseconds(value).value


def mprisTimeToCastTime(value: Microseconds) -> chrono.Seconds:
    return chrono.Seconds(chrono.Microseconds(value))
