#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QWidget

from kast.interface.qt5.UiServices import UiServices
from kast.interface.qt5.view.AboutViewModel import Ui_AboutViewModel
from kast.interface.qt5.viewModel.ViewModelBase import ViewBase, ViewModelBase


class View(ViewBase, QDialog, Ui_AboutViewModel):
    pass


class AboutViewModel(ViewModelBase):

    def __init__(self, parent: QWidget, uiServices: UiServices) -> None:
        self._view = View(parent=parent)
        super().__init__(uiServices=uiServices, view=self._view)
        self._view.hide()

        logo = QPixmap(str(self.services.settings.appIconPath)).scaled(128, 128)
        self._view.labelLogo.setPixmap(logo)

        self._view.labelAppName.setText(self.services.settings.appName)
        self._view.labelAppVersion.setText(self.services.settings.appVersion)
        self._view.labelAppDescription.setText("Cast movies (with subtitles) straight from your PC.")
        self._view.labelAuthorName.setText(self.services.settings.author)
        self._view.labelAuthorContact.setText(self.services.settings.email)

        self._view.layout().activate()
        self._view.setFixedSize(self._view.size().width(), self._view.size().height())
