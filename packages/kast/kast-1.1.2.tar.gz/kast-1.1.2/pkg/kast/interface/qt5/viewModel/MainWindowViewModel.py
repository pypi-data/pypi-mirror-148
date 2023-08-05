#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtWidgets import QMainWindow

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.view.MainWindowView import Ui_MainWindowView
from kast.interface.qt5.viewModel.AboutViewModel import AboutViewModel
from kast.interface.qt5.viewModel.MediaControlViewModel import MediaControlViewModel
from kast.interface.qt5.viewModel.StatusBarViewModel import StatusBarViewModel
from kast.interface.qt5.viewModel.VideoPreviewViewModel import VideoPreviewViewModel
from kast.interface.qt5.viewModel.VideoSettingsViewModel import VideoSettingsViewModel
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase
from kast.interface.qt5.viewModel.taskbar.TaskbarViewModel import TaskbarViewModel


class View(ViewBase, QMainWindow, Ui_MainWindowView):
    pass


class MainWindowViewModel(ViewModelBase):

    def __init__(self, uiServices: UiServices) -> None:
        self._view = View(parent=None)
        super().__init__(uiServices=uiServices, view=self._view)
        self._view.setWindowTitle(self.services.settings.appName)

        self._taskbarViewModel = TaskbarViewModel(parent=self._view, uiServices=uiServices)

        self._aboutViewModel = AboutViewModel(parent=self._view, uiServices=self.uiServices)
        self._videoPreviewViewModel = VideoPreviewViewModel(parent=self.view, uiServices=self.uiServices)
        self._mediaControlViewModel = MediaControlViewModel(parent=self.view, uiServices=self.uiServices, videoPreviewViewModel=self._videoPreviewViewModel)
        self._videoSettingsViewModel = VideoSettingsViewModel(parent=self.view, uiServices=self.uiServices)
        self._statusBarViewModel = StatusBarViewModel(parent=self.view, uiServices=self.uiServices)

        self._view.layoutForPreview.addWidget(self._videoPreviewViewModel.view)
        self._addControlsViewModel(self._mediaControlViewModel)
        self._addControlsViewModel(self._videoSettingsViewModel)
        self._addControlsViewModel(self._statusBarViewModel)

        self._view.actionExit.triggered.connect(self._view.close)
        self._view.actionAbout.triggered.connect(self._aboutViewModel.view.show)

    def _addControlsViewModel(self, viewModel: ViewModelBase) -> None:
        self._view.layoutForControls.addWidget(viewModel.view)
