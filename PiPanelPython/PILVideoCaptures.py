import cv2
from VideoCapture import VideoCapture


class PILVideoCapture:
    def __init__(self, device_index):
        self.cap = VideoCapture(device_index)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        frame = self.cap.read()
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


class PILVideoCaptureEdgeDetection:
    def __init__(self, device_index):
        self.cap = VideoCapture(device_index)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        frame = self.cap.read()
        edges = cv2.Canny(frame, 100, 300)
        return cv2.cvtColor(edges, cv2.COLOR_BGR2RGB)


class PILVideoCaptureFile:
    def __init__(self, file_path):
        self.cap = VideoCapture(file_path)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1024 // 2, 600 // 2))
        return frame