#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

from kast.interface.qt5.utils.Schedulable import ISchedulable


class SchedulableException(Exception):
    pass


def foregroundTask(func):
    """Decorator used to make sure method runs in interface thread. Decorated methods must return None!"""
    def wrapper(self: ISchedulable, *args, **kwargs):
        _verifySchedulable(self)

        def callback() -> None:
            func(self, *args, **kwargs)

        if _isMainThread():
            callback()
            return

        self.schedulers.interfaceScheduler.schedule(callback)

    return wrapper


def backgroundTaskEx(forceSpawnThread: bool = False):
    """Decorator used to make sure method runs in background thread. Decorated methods must return None!"""
    def decorator(func):
        def wrapper(self: ISchedulable, *args, **kwargs):
            _verifySchedulable(self)

            def callback() -> None:
                func(self, *args, **kwargs)

            if not forceSpawnThread and not _isMainThread():
                callback()
                return

            self.schedulers.backgroundRunner.execute(lambda: self.backgroundTaskMiddleware(callback))

        return wrapper

    return decorator


backgroundTask = backgroundTaskEx()


def _isMainThread() -> bool:
    return QThread.currentThread() == QApplication.instance().thread()


def _verifySchedulable(obj):
    if not isinstance(obj, ISchedulable):
        raise SchedulableException("Non schedulable service cannot use schedulable decorators!")
