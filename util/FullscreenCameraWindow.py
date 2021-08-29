from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QImage
import numpy as np
import cv2
from time import sleep
from util.VideoCapture import VideoCapture
from util.ImageLabel import ImageLabel


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, device_index, use_default_video_capture, manipulation_function):
        super(VideoThread, self).__init__()
        self.device_index = device_index
        self.use_default_video_capture = use_default_video_capture
        self.manipulation_function = manipulation_function
        self._should_run = True


    def run(self):
        if self.use_default_video_capture:
            cap = cv2.VideoCapture(self.device_index)

            try:
                while self._should_run:
                    ret, frame = cap.read()

                    if ret:
                        self.change_pixmap_signal.emit(frame)

                    sleep(1.0 / cap.get(cv2.CAP_PROP_FPS))
            finally:
                cap.release()
        else:
            cap = VideoCapture(self.device_index)

            try:
                while self._should_run:
                    frame = cap.read()
                    frame = frame if self.manipulation_function is None else self.manipulation_function(frame)
                    self.change_pixmap_signal.emit(frame)
            finally:
                cap.release()


    def stop(self):
        self._should_run = False
        self.wait()



class FullscreenCameraWindow(QWidget):
    def __init__(self, device_index=0, use_default_video_capture=True, manipulation_function=None):
        super(FullscreenCameraWindow, self).__init__()
        
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = ImageLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(1024, 600)
        pixmap.fill(QColor("darkGray"))
        self.label.setPixmap(pixmap)
        
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.thread = VideoThread(device_index, use_default_video_capture, manipulation_function)
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