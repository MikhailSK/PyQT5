# PyQT5 project
# Created by Mikhail Skoptsov
# This is a music player file


import sys
from os.path import expanduser
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, \
    QHBoxLayout, QSlider, QLabel, QAction, QFileDialog, \
    QMainWindow, QMessageBox, QApplication, qApp
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, \
    QMediaMetaData, QMediaContent
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDirIterator, QUrl


class MainWindowMusicPlayer(QMainWindow):
    stopState: bool

    def __init__(self):
        super().__init__()
        self.currentPlaylist = QMediaPlaylist()
        self.player = QMediaPlayer()
        self.userAction = -1  # 0 - stopped, 1 - playing 2 - paused
        self.player.mediaStatusChanged.connect(self.qmp_media_status_changed)
        self.player.stateChanged.connect(self.qmp_state_changed)
        self.player.positionChanged.connect(self.qmp_position_changed)
        self.player.volumeChanged.connect(self.qmp_volume_changed)
        self.player.setVolume(60)
        # Status bar
        self.statusBar().showMessage('No Media :: %d' % self.player.volume())
        self.home_screen()

    def home_screen(self):
        self.setWindowTitle('Music Player')

        self.create_menubar()

        self.create_toolbar()

        controlBar = self.add_controls()

        # need to add both information screen and control bar to the central widget.
        centralWidget = QWidget()
        centralWidget.setLayout(controlBar)
        self.setCentralWidget(centralWidget)

        # Set size of the MainWindow
        self.resize(200, 100)

        self.show()

    def create_menubar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(self.file_open())
        file_menu.addAction(self.song_info())
        file_menu.addAction(self.folder_open())
        file_menu.addAction(self.exit_action())

    def create_toolbar(self):
        pass

    def add_controls(self):
        controlArea = QVBoxLayout()
        seekSliderLayout = QHBoxLayout()
        controls = QHBoxLayout()
        playlistCtrlLayout = QHBoxLayout()

        # creating buttons
        playBtn = QPushButton('Play')  # play button
        pauseBtn = QPushButton('Pause')  # pause button
        stopBtn = QPushButton('Stop')  # stop button
        volumeDescBtn = QPushButton('V (-)')  # Decrease Volume
        volumeIncBtn = QPushButton('V (+)')  # Increase Volume

        # creating playlist controls
        prevBtn = QPushButton('Prev Song')
        nextBtn = QPushButton('Next Song')

        # creating seek slider
        seekSlider = QSlider()
        seekSlider.setMinimum(0)
        seekSlider.setMaximum(100)
        seekSlider.setOrientation(Qt.Horizontal)
        seekSlider.setTracking(False)
        seekSlider.sliderMoved.connect(self.seek_position)
        # seekSlider.valueChanged.connect(self.seekPosition)

        seekSliderLabel1 = QLabel('0.00')
        seekSliderLabel2 = QLabel('0.00')
        seekSliderLayout.addWidget(seekSliderLabel1)
        seekSliderLayout.addWidget(seekSlider)
        seekSliderLayout.addWidget(seekSliderLabel2)

        # Add handler for each button. Not using the default slots.
        playBtn.clicked.connect(self.play_handler)
        pauseBtn.clicked.connect(self.pause_handler)
        stopBtn.clicked.connect(self.stop_handler)
        volumeDescBtn.clicked.connect(self.decrease_volume)
        volumeIncBtn.clicked.connect(self.increase_volume)

        # Adding to the horizontal layout
        controls.addWidget(volumeDescBtn)
        controls.addWidget(playBtn)
        controls.addWidget(pauseBtn)
        controls.addWidget(stopBtn)
        controls.addWidget(volumeIncBtn)

        # playlist control button handlers
        prevBtn.clicked.connect(self.prev_item_playlist)
        nextBtn.clicked.connect(self.next_item_playlist)
        playlistCtrlLayout.addWidget(prevBtn)
        playlistCtrlLayout.addWidget(nextBtn)

        # Adding to the vertical layout
        controlArea.addLayout(seekSliderLayout)
        controlArea.addLayout(controls)
        controlArea.addLayout(playlistCtrlLayout)
        return controlArea

    # Music playback function
    def play_handler(self):
        self.userAction = 1
        self.statusBar().showMessage('Playing at Volume %d' % self.player.volume())
        if self.player.state() == QMediaPlayer.StoppedState:
            if self.player.mediaStatus() == QMediaPlayer.NoMedia:
                print(self.currentPlaylist.mediaCount())
                if self.currentPlaylist.mediaCount() == 0:
                    self.open_file()
                if self.currentPlaylist.mediaCount() != 0:
                    self.player.setPlaylist(self.currentPlaylist)
            elif self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
                self.player.play()
            elif self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
                self.player.play()
        elif self.player.state() == QMediaPlayer.PlayingState:
            pass
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()

    # Music pause function
    def pause_handler(self):
        self.userAction = 2
        self.statusBar().showMessage('Paused %s at position %s at Volume %d' %
                                     (self.player.metaData(QMediaMetaData.Title),
                                      self.centralWidget().layout().itemAt(0).layout().
                                      itemAt(0).widget().text(),
                                      self.player.volume()))
        self.player.pause()

    # Music stop function
    def stop_handler(self):
        self.userAction = 0
        self.statusBar().showMessage('Stopped at Volume %d'
                                     % (self.player.volume()))
        if self.player.state() == QMediaPlayer.PlayingState:
            self.stopState = True
            self.player.stop()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.stop()
        elif self.player.state() == QMediaPlayer.StoppedState:
            pass

    # Music status change function
    def qmp_media_status_changed(self):
        if self.player.mediaStatus() == QMediaPlayer.LoadedMedia \
                and self.userAction == 1:
            durationT = self.player.duration()
            self.centralWidget().layout().itemAt(0).layout() \
                .itemAt(1).widget().setRange(0, durationT)
            self.centralWidget().layout().itemAt(0).layout() \
                .itemAt(2).widget().setText(
                '%d:%02d' % (int(durationT / 60000),
                             int((durationT / 1000) % 60)))
            self.player.play()

    # Music playing change function
    def qmp_state_changed(self):
        if self.player.state() == QMediaPlayer.StoppedState:
            self.player.stop()

    # Music time change function
    def qmp_position_changed(self, position, senderType=False):
        sliderLayout = self.centralWidget().layout().itemAt(0).layout()
        if not senderType:
            sliderLayout.itemAt(1).widget().setValue(position)
        # update the text label
        sliderLayout.itemAt(0).widget().setText('%d:%02d' % (int(position / 60000),
                                                             int((position / 1000) % 60)))

    def seek_position(self, position):
        sender = self.sender()
        if isinstance(sender, QSlider):
            if self.player.isSeekable():
                self.player.setPosition(position)

    # Music volume change function
    def qmp_volume_changed(self):
        msg = self.statusBar().currentMessage()
        msg = msg[:-2] + str(self.player.volume())
        self.statusBar().showMessage(msg)

    # Music volume + change function
    def increase_volume(self):
        vol = self.player.volume()
        vol = min(vol + 5, 100)
        self.player.setVolume(vol)

    # Music volume - change function
    def decrease_volume(self):
        vol = self.player.volume()
        vol = max(vol - 5, 0)
        self.player.setVolume(vol)

    # File open function
    def file_open(self):
        fileAc = QAction(QIcon('icons\\open.png'), 'Open File', self)
        fileAc.setShortcut('Ctrl+O')
        fileAc.setStatusTip('Open File')
        fileAc.triggered.connect(self.open_file)
        return fileAc

    # File opening function
    def open_file(self):
        file_Chosen = QFileDialog.getOpenFileUrl(self, 'Open Music File',
                                                 expanduser('~'), 'Audio (*.mp3 *.ogg *.wav)',
                                                 '*.mp3 *.ogg *.wav')
        if file_Chosen is not None:
            self.currentPlaylist.addMedia(QMediaContent(file_Chosen[0]))

    # Folder open function
    def folder_open(self):
        folderAc = QAction(QIcon('icons\\open_fld.png'), 'Open Folder', self)
        folderAc.setShortcut('Ctrl+D')
        folderAc.setStatusTip('Open Folder (Will add all the files in the folder) ')
        folderAc.triggered.connect(self.add_files)
        return folderAc

    # Folder opening function
    def add_files(self):
        folder_Chosen = QFileDialog.getExistingDirectory(self,
                                                         'Open Music Folder', expanduser('~'))
        if folder_Chosen is not None:
            it = QDirIterator(folder_Chosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() == False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    print(it.filePath(), fInfo.suffix())
                    if fInfo.suffix() in ('mp3', 'ogg', 'wav'):
                        print('added file ', fInfo.fileName())
                        self.currentPlaylist. \
                            addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))
                it.next()

    # Song information function
    def song_info(self):
        infoAc = QAction(QIcon('icons\\info.png'), 'Info', self)
        infoAc.setShortcut('Ctrl+I')
        infoAc.setStatusTip('Displays Current Song Information')
        infoAc.triggered.connect(self.display_song_info)
        return infoAc

    # Show song information
    def display_song_info(self):
        metaDataKeyList = self.player.availableMetaData()
        fullText = '<table class="tftable" border="0">'
        for key in metaDataKeyList:
            value = self.player.metaData(key)
            fullText = \
                fullText + '<tr><td>' + key + '</td><td>' + \
                str(value) + '</td></tr>'
        fullText = fullText + '</table>'
        infoBox = QMessageBox(self)
        infoBox.setWindowTitle('Detailed Song Information')
        infoBox.setTextFormat(Qt.RichText)
        infoBox.setText(fullText)
        infoBox.addButton('OK', QMessageBox.AcceptRole)
        infoBox.show()

    # Switch to previous song
    def prev_item_playlist(self):
        self.player.playlist().previous()

    # Switch to next song
    def next_item_playlist(self):
        self.player.playlist().next()

    # exit function
    def exit_action(self):
        exitAc = QAction(QIcon('icons\\exit.png'), '&Exit', self)
        exitAc.setShortcut('Ctrl+Q')
        exitAc.setStatusTip('Exit App')
        exitAc.triggered.connect(self.close)
        return exitAc

    # exiting function
    @staticmethod
    def exit():
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindowMusicPlayer()
    sys.exit(app.exec_())
