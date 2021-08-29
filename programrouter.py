import cv2
from util.VideoCapture import VideoCapture
from util.FullscreenImageWindow import FullscreenImageWindow
from util.FullscreenVideoWindow import FullscreenVideoWindow
from util.FullscreenCameraWindow import FullscreenCameraWindow
from programs.DrumMachine import DrumMachine
from programs.ImageMenu import ImageMenu
from programs.VideoMenu import VideoMenu
from programs.ComputerVisionMenu import ComputerVisionMenu
from programs.AudioMenu import AudioMenu
from programs.LedMatrixController import LedMatrixController


def image_menu():
    ImageMenu().create_buttons()


def video_menu():
    VideoMenu().create_buttons()


def computer_vision_menu():
    ComputerVisionMenu().create_buttons()


def audio_menu():
    AudioMenu().create_buttons()


def modified_sine():
    ModifiedSine()


def waveform():
    WaveForm()


def spectrum_analyzer():
    SpectrumAnalyzer()


def drum_machine():
    DrumMachine().create_buttons()
    

def led_matrix():
    LedMatrixController().create_buttons()