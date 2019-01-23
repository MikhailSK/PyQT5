# PyQT5 project
# Created by Mikhail Skoptsov
# This file is the main menu of my application
import os
import sys

import pyglet
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from fire import Fire
from Result import generate


class MyFunWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "FUN"
        self.InitUI()
        self.count_pic = 0
        self.drop_par = 0
        self.drops_count_par = -1
        self.name_par = 'movie'
        self.width_par = 100
        self.height_par = 100
        self.stat = 1

    def InitUI(self):
        uic.loadUi('ui_forms\\fire_gen.ui', self)
        self.count.valueChanged.connect(self.value_change)
        self.generate.clicked.connect(self.main_funk)
        self.drop.stateChanged.connect(self.changeTitle)
        self.show()

    def main_funk(self):
        self.stat = 0
        try:
            self.width_par = int(self.width.text())

            self.height_par = int(self.height.text())

            if self.drop_par == 1:
                self.drops_count_par = int(self.drops_count.text())
            else:
                self.drops_count_par = -1
        except ValueError:
            self.stat = 1
        if self.name.text() != "":
            self.name_par = self.name.text()
        else:
            self.stat = 1

        if self.stat == 0:
            fire_obj = Fire(self.name_par, self.count_pic, self.height_par,
                            self.width_par, self.drop_par, self.drops_count_par)
            stat_gen = fire_obj.generate_images()
            # print("have_fun", self.name_par)
            if stat_gen == "success":
                generate(self.name_par, self.width_par, self.height_par)
                # self.generator()

    def value_change(self):
        self.count_pic = self.count.value()

    def changeTitle(self, state):
        if state == Qt.Checked:
            self.drop_par = 1
        else:
            self.drop_par = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyFunWidget()
    sys.exit(app.exec_())
