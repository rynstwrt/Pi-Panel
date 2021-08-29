from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QImage
import numpy as np
import cv2
from util.VideoCapture import VideoCapture
from util.ImageLabel import ImageLabel
from time import sleep


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, url):
        super(VideoThread, self).__init__()
        self.url = url
        self._should_run = True


    def run(self):
        cap = cv2.VideoCapture(self.url)

        try:
            while self._should_run:
                ret, frame = cap.read()

                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = cap.read()
                
                self.change_pixmap_signal.emit(frame)
                sleep(1.0 / cap.get(cv2.CAP_PROP_FPS))
        finally:
            cap.release()
   

    def stop(self):
        self._should_run = False
        self.wait()



class FullscreenVideoWindow(QWidget):
    def __init__(self, url):
        super(FullscreenVideoWindow, self).__init__()
        
        self.showFullScreen()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = ImageLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(1024, 600)
        pixmap.fill(QColor("darkGray"))
        self.label.setPixmap(pixmap)
        
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.thread = VideoThread(url)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()


    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


    @pyqtSlot(np.ndarray)
    def update_image(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = image_rgb.shape

        image_qt = QImage(image_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        image_qt = image_qt.scaled(1024, 600, Qt.KeepAspectRatioByExpanding)
        image_qt = QPixmap.fromImage(image_qt)

        self.label.setPixmap(image_qt)