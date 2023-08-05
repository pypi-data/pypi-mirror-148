#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from PyQt5.QtWidgets import QMessageBox

ButtonId = int


class DialogQuestion:

    def __init__(
        self,
        title: str,
        message: str,
        default: bool = False,
        icon: QMessageBox.Icon = QMessageBox.Question,
        positiveButton: ButtonId = QMessageBox.Ok,
        negativeButton: ButtonId = QMessageBox.Cancel
    ) -> None:
        self._positiveButton = positiveButton
        self._negativeButton = negativeButton
        self._msgBox = msgBox = QMessageBox()

        msgBox.setIcon(icon)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(positiveButton | negativeButton)
        msgBox.setDefaultButton(positiveButton if default else negativeButton)

    def display(self) -> bool:
        return self._msgBox.exec() == self._positiveButton

    def dismiss(self) -> None:
        self._msgBox.close()


def dialogCriticalError(message: str) -> None:
    _dialogInformation(title="CriticalError", message=message, icon=QMessageBox.Critical)


def dialogError(message: str) -> None:
    _dialogInformation(title="Error", message=message, icon=QMessageBox.Critical)


def dialogWarning(message: str) -> None:
    _dialogInformation(title="Warning", message=message, icon=QMessageBox.Warning)


def dialogQuestionOkCancel(title: str, message: str, default: bool = False) -> bool:
    return DialogQuestion(
        title=title,
        message=message,
        default=default
    ).display()


def dialogQuestionYesNo(title: str, message: str, default: bool = False) -> bool:
    return DialogQuestion(
        title=title,
        message=message,
        default=default,
        positiveButton=QMessageBox.Yes,
        negativeButton=QMessageBox.No
    ).display()


def _dialogInformation(title: str, message: str, icon: QMessageBox.Icon = QMessageBox.Information) -> None:
    msgBox = QMessageBox()
    msgBox.setIcon(icon)
    msgBox.setWindowTitle(title)
    msgBox.setText(message)
    msgBox.exec()
