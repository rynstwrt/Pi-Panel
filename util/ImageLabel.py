from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.parent = parent
        self.setCursor(Qt.BlankCursor)

    
    def mousePressEvent(self, event):
        self.parent.close()