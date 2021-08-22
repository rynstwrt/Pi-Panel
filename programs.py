from util.VideoCapture import VideoCapture
from util.WaveForm import WaveForm
from util.SpectrumAnalyzer import SpectrumAnalyzer
from util.ModifiedSine import ModifiedSine
from util.FullscreenImageWindow import FullscreenImageWindow
from util.FullscreenVideoWindow import FullscreenVideoWindow
from util.FullscreenCameraWindow import FullscreenCameraWindow
import cv2


# Store image windows in this variable so they don't 
# get immediately garbage collected and disappear
last_image_window = False 


def pride_flag():
    global last_image_window
    last_image_window = FullscreenImageWindow("assets/progressprideflag.jpg", False)
    last_image_window.show()


def camera():
    FullscreenCameraWindow()


def edge_detection():
    FullscreenCameraWindow(0, False, lambda frame: cv2.Canny(frame, 100, 300))


def bunny_video():
    FullscreenVideoWindow("https://www.rmp-streaming.com/media/big-buck-bunny-360p.mp4")


def monitor():
    global last_image_window
    last_image_window = FullscreenImageWindow("assets/monitor.jpg", False)
    last_image_window.show()


def modified_sine():
    ModifiedSine()


def waveform():
    WaveForm()


def spectrum_analyzer():
    SpectrumAnalyzer()
