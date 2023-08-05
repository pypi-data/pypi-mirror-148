#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import logging


class Loggable:

    @property
    def log(self) -> logging.Logger:
        return logging.getLogger(f"{self.__class__.__name__}:({hex(id(self))})")
