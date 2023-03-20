import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class MP3Music(QWidget):
    def __init__(self):
        super().__init__()

        self.state = "Play"
        self.playlist = []
        self.position = 0
        self.index = ""
        self.player = QMediaPlayer()

        p = self.palette()
        color = QColor("#87CEEB")
        color.setAlpha(200)
        p.setColor(QPalette.Window, QColor(color))
        self.setPalette(p)

        self.init_ui()

    def init_ui(self):
        vb = QVBoxLayout()
        self.setLayout(vb)
        vb.setAlignment(Qt.AlignCenter)

        self.label = QLabel("MP3 PLAYER")
        self.label.setFont(QFont("Italic", 20))
        self.label.setAlignment(Qt.AlignCenter)
        vb.addWidget(self.label)

        hb = QHBoxLayout()
        vb.addLayout(hb)

        font = QFont("Italic", 10)
        self.skipbackwardbtn = QPushButton()
        self.skipbackwardbtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        hb.addWidget(self.skipbackwardbtn)

        self.playbtn = QPushButton(self)
        self.playbtn.setEnabled(False)
        self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playbtn.setFont(font)
        hb.addWidget(self.playbtn)

        self.skipforwardbtn = QPushButton()
        self.skipforwardbtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipForward))
        hb.addWidget(self.skipforwardbtn)

        hb2 = QHBoxLayout()
        vb.addLayout(hb2)
        self.openfilebtn = QPushButton()
        self.openfilebtn.setIcon(
        self.style().standardIcon(QStyle.SP_DirOpenIcon))
        self.openfilebtn.setFont(font)
        hb2.addWidget(self.openfilebtn)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)
        hb2.addWidget(self.slider)

        self.songlist = QListWidget()
        vb.addWidget(self.songlist)

        self.toolbar = QToolBar()
        vb.addWidget(self.toolbar)
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()
        self.toolbar.addSeparator()

        self.player = QMediaPlayer()
        self.space = QWidget()
        self.space.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(self.space)
        self.speaker = QAction()
        self.speaker.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.toolbar.addAction(self.speaker)
        self.slider_vl = QSlider(Qt.Horizontal)
        self.toolbar.addWidget(self.slider_vl)
        self.label_vl = QLabel("50%")
        self.label_vl.setFont(QFont("Helvetica", 10))
        self.label_vl.setMinimumWidth(40)
        self.toolbar.addWidget(self.label_vl)
        self.slider.setRange(0, 100)
        volume = self.player.volume()
        self.slider_vl.setValue(int(volume / 2))

        # pembuatan fungsi tombol
        self.openfilebtn.clicked.connect(self.open_mp3_file)
        self.playbtn.clicked.connect(self.play_mp3)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.stateChanged.connect(self.state_changed)
        self.songlist.clicked.connect(self.set_state)
        self.songlist.doubleClicked.connect(self.play_mp3)
        self.skipbackwardbtn.clicked.connect(self.skip_backward)
        self.skipforwardbtn.clicked.connect(self.skip_forward)
        self.slider_vl.valueChanged.connect(self.set_volume)

        # fungsi control untuk mengambil musiklist
    def open_mp3_file(self):
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(
            self, "Open files", os.getenv("HOME"))
        self.song = names[0]
        self.songlist.addItems(self.song)

    def set_state(self):
        self.playbtn.setEnabled(True)
        self.state = "Play"
        self.playbtn.setText("")
        self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def play_mp3(self):
        if self.state == "Play":
            self.playbtn.setText("")
            self.state = "Pause"

            path = self.songlist.currentItem().text()
            url = QUrl.fromLocalFile(path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.index = self.songlist.currentRow().__index__()
            self.player.setPosition(self.position)
            self.playlist.append(path)
            if len(self.playlist) > 2:
                self.playlist.pop(0)
            if self.songlist.currentItem().text != self.playlist[0]:
                self.position = 0
                self.player.setPosition(self.position)
            self.player.play()
        else:
            self.playbtn.setText("")
            self.state = "Play"
            self.player.pause()
            paused = self.player.position()
            self.position = paused

    def skip_backward(self):
        self.state = "Play"
        try:
            self.songlist.setCurrentRow(self.index - 1)
            self.play_mp3()
        except:
            pass

    def skip_forward(self):
        self.state = "Play"
        try:
            self.songlist.setCurrentRow(self.index + 1)
            self.play_mp3()
        except:
            pass

    def set_position(self, position):
        self.player.setPosition(position)

    def position_changed(self, position):
        self.slider.setValue(position)
        duration = self.player.duration()
        value = self.slider.value()
        try:
            value == duration
            self.state = "Play"
        except:
            self.play_mp3()

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def state_changed(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playbtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
            self.player.play()
        else:
            self.playbtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            self.player.pause()

    def set_volume(self):
        volume = self.slider_vl.value()
        self.player.setVolume(volume)
        self.label_vl.setText(str(volume)+"%")

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Message', "Are You Want To Quit ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    gui = MP3Music()
    gui.show()
    gui.setWindowTitle("MP3 Player 0.1")
    gui.setWindowIcon(QIcon("musikplayer.ico"))
    gui.setGeometry(600,200,600,700)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
