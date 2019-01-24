# PyQT5 project
# Created by Mikhail Skoptsov
# This file creates a window for entering parameters
# and generating a fire image GIF

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow,\
    QSpinBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from fire import Fire
from Result import generate


class MyFunWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "FUN"
        self.InitUI()
        # Count of images in a GIF image
        self.count_pic = 0
        # Parameter responsible
        # for the presence of drops of fire
        # over the fire itself
        self.drop_par = 0
        # The parameter is responsible
        # for how many drops will be.
        # Than parameter higher the less drops
        self.drops_count_par = -1
        # GIF image name parameter
        self.name_par = 'movie'
        # GIF image width parameter
        self.width_par = 100
        # GIF image height parameter
        self.height_par = 100
        # error presence parameter
        self.stat = 1

    def InitUI(self):
        uic.loadUi('ui_forms\\fire_gen.ui', self)
        # Starts the function of collecting
        # information on the count
        self.count.valueChanged.connect(self.value_change)
        # Starts the generating function
        self.generate.clicked.connect(self.main_funk)
        # Starts the function of collecting
        # information on the drops
        self.drop.stateChanged.connect(self.changeTitle)
        self.show()

    def main_funk(self):
        self.stat = 0
        # Collecting information
        try:
            self.width_par = int(self.width.text())

            self.height_par = int(self.height.text())

            if self.drop_par == 1:
                self.drops_count_par = \
                    int(self.drops_count.text())
            else:
                self.drops_count_par = -1

        except ValueError:
            self.stat = 1

        if self.name.text() != "" and self.count_pic != 0:
            self.name_par = self.name.text()
        else:
            self.stat = 1

        # Start generate function
        if self.stat == 0:
            fire_obj = Fire(self.name_par, self.count_pic,
                            self.height_par,
                            self.width_par, self.drop_par,
                            self.drops_count_par)
            stat_gen = fire_obj.generate_images()
            # print("have_fun", self.name_par)
            if stat_gen == "success":
                self.label.setText("SUCCESS")
                generate(self.name_par, self.width_par,
                         self.height_par)
                # self.generator()
                self.label.setText("Enter the parameters"
                                   " and they will generate"
                                   " a gif image of the fire")
            else:
                self.label.setText("ERROR in the my code")
        else:
            self.label.setText("ERROR in your parameters")

    # change of count
    def value_change(self):
        self.count_pic = self.count.value()

    # change of drop state
    def changeTitle(self, state):
        if state == Qt.Checked:
            self.drop_par = 1
        else:
            self.drop_par = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyFunWidget()
    sys.exit(app.exec_())
