from PyQt5.QtWidgets import QLabel


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.parent = parent

    
    def mousePressEvent(self, event):
        self.parent.close()