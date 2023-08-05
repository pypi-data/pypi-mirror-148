#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Callable
from queue import Empty, Full, Queue
from typing import Optional

from PyQt5.QtCore import QTimer

from kast.utils.Loggable import Loggable


class InterfaceScheduler(Loggable):

    Callback = Callable[[], None]

    TIMEOUT_SECONDS = 0.1

    def __init__(self) -> None:
        self._queue = Queue()
        self._timer = QTimer()
        self._timer.setInterval(100)
        self._timer.timeout.connect(self._process)
        self._timer.start()

    def schedule(self, callback: Callback) -> None:
        try:
            self._queue.put(item=callback, block=True, timeout=self.TIMEOUT_SECONDS)
        except Full:
            raise RuntimeError(f"Could not schedule interface task! Queue size: {self._queue.qsize()}")

    def _process(self) -> None:
        callback = self._tryPopTask()
        if callback:
            callback()
            self._queue.task_done()

    def _tryPopTask(self) -> Optional[Callback]:
        try:
            return self._queue.get(block=True, timeout=self.TIMEOUT_SECONDS)
        except Empty:
            return None
