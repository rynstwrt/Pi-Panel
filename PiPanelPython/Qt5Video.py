from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys



class Qt5Video(QMainWindow):
    def __init__(self, parent=None):
        super(Qt5Video, self).__init__(parent)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        video_widget = QVideoWidget()

        wid = QWidget(self)
        self.setCentralWidget(wid)

        layout = QVBoxLayout()
        layout.addWidget(video_widget)

        wid.setLayout(layout)

        self.media_player.setVideoOutput(video_widget)

    
    def setMedia(self, path):
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))


    def exitCall(self):
        sys.exit(app.exec_())


    def play(self):
        self.media_player.play()


if __name__ == "__main__":
    app = QApplication([])
    player = Qt5Video()
    player.show()
    player.setMedia("assets/trippy.mp4")
    player.play()
    sys.exit(app.exec_())