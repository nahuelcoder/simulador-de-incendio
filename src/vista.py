#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Este módulo contiene la clase que crea la ventana"""

from PyQt5.QtWidgets import QMainWindow
from GUI import Ui_Simulador


class Vista(QMainWindow, Ui_Simulador):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setupUi(self)
