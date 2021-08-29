from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from util.ImageLabel import ImageLabel
from urllib.request import urlopen


class FullscreenImageWindow(QWidget):
    def __init__(self, path_or_url, is_url=False):
        super(FullscreenImageWindow, self).__init__()
        
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = ImageLabel(self)

        if is_url:
            data = urlopen(path_or_url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
        else:
            pixmap = QPixmap(path_or_url)
        
        pixmap = pixmap.scaled(1024, 600)
        label.setPixmap(pixmap)
        
        layout.addWidget(label)
        self.setLayout(layout)