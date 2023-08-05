#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import os
from typing import Type

from kast.interface.qt5.viewModel.taskbar.TaskbarViewModelBase import TaskbarViewModelBase


def _getImpl() -> Type[TaskbarViewModelBase]:
    if os.name == 'nt':
        from ._win32.Win32TaskbarViewModel import Win32TaskbarViewModel
        return Win32TaskbarViewModel

    if os.name == 'posix':
        from ._unity.UnityTaskbarViewModel import UnityTaskbarViewModel
        return UnityTaskbarViewModel

    return TaskbarViewModelBase


TaskbarViewModel = _getImpl()
