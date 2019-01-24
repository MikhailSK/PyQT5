# PyQT5 project
# Created by Mikhail Skoptsov
# This file is the main menu of my application


import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

# Music Player
from music_player import MainWindowMusicPlayer
# Video Player
from video_player import MainWindowVideoPlayer
# Have Fun
from have_fun import MyFunWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Main menu"
        self.InitUI()
        self.cams = -1

    def InitUI(self):
        uic.loadUi('ui_forms\\main_form.ui', self)
        self.buttonWindow1.clicked.connect(
            self.buttonWindow2_onClick)
        self.buttonWindow2.clicked.connect(
            self.buttonWindow1_onClick)
        self.buttonWindow3.clicked.connect(
            self.buttonWindow3_onClick)
        self.show()

    # Function that closes the main menu and
    # opens the music player
    @pyqtSlot()
    def buttonWindow1_onClick(self):
        self.cams = MainWindowMusicPlayer()
        self.cams.show()
        self.close()

    # Function that closes the main menu and
    # opens the video player
    @pyqtSlot()
    def buttonWindow2_onClick(self):
        self.cams = MainWindowVideoPlayer()
        self.cams.show()
        self.close()

    # Function that closes the main menu and
    # opens Have Fun
    @pyqtSlot()
    def buttonWindow3_onClick(self):
        self.cams = MyFunWidget()
        self.cams.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
