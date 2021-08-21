import tkinter
from PIL import Image, ImageTk
from VideoCapture import VideoCapture
import cv2
import pyaudio
from PILVideoCaptures import PILVideoCapture, PILVideoCaptureEdgeDetection, PILVideoCaptureFile
import pyaudio
import struct
import numpy as np
import matplotlib
matplotlib.use("qt5agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#################### CONSTANTS ####################
AUDIO_CHUNK_SIZE = 1024 * 2
AUDIO_RATE = 32000
AUDIO_AMPLITUDE = 200


#################### UTILITY CLASSES ####################
class WaveForm:
    def __init__(self):
        p = pyaudio.PyAudio()

        self.stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=AUDIO_RATE,
            input=True,
            output=True,
            frames_per_buffer=AUDIO_CHUNK_SIZE
        )

        plt.rcParams["toolbar"] = "None"

        fig, ax = plt.subplots(facecolor="black")
        fig_manager = plt.get_current_fig_manager()
        fig_manager.full_screen_toggle()
        fig.canvas.mpl_connect("button_press_event", lambda e: plt.close())

        x = np.arange(0, AUDIO_CHUNK_SIZE)

        self.line, = ax.plot(x, np.random.rand(AUDIO_CHUNK_SIZE), lw=2, color=(3/255, 160/255, 98/255))

        ax.axis("off")
        ax.set_xlim(0, AUDIO_CHUNK_SIZE)
        ax.set_ylim(-AUDIO_AMPLITUDE, AUDIO_AMPLITUDE)

        self.anim = animation.FuncAnimation(fig, self.animate, frames=len(x), interval=20, blit=True)


    def animate(self, frame_num): 
        data = self.stream.read(AUDIO_CHUNK_SIZE)

        data_int = np.array(struct.unpack(str(2 * AUDIO_CHUNK_SIZE) + "B", data), dtype="b")[::2]

        self.line.set_xdata(np.arange(len(data_int)))
        self.line.set_ydata(data_int)

        return self.line,


class SpectrumAnalyzer:
    def __init__(self):
        p = pyaudio.PyAudio()

        self.stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=AUDIO_RATE,
            input=True,
            output=True,
            frames_per_buffer=AUDIO_CHUNK_SIZE
        )

        plt.rcParams["toolbar"] = "None"

        fig, ax = plt.subplots(facecolor="black")
        fig_manager = plt.get_current_fig_manager()
        fig_manager.full_screen_toggle()
        fig.canvas.mpl_connect("button_press_event", lambda e: plt.close())

        x_fft = np.linspace(0, AUDIO_RATE, AUDIO_CHUNK_SIZE)

        self.line_fft, = ax.semilogx(x_fft, np.random.rand(AUDIO_CHUNK_SIZE), lw=2, color=(3/255, 160/255, 98/255))

        ax.axis("off")
        ax.set_ylim(-.01, .09)
        ax.set_xlim(20, AUDIO_RATE)

        self.anim = animation.FuncAnimation(fig, self.animate, interval=0, blit=True)

    
    def animate(self, frame_num):
        data = self.stream.read(AUDIO_CHUNK_SIZE)

        data_int = np.array(struct.unpack(str(2 * AUDIO_CHUNK_SIZE) + "B", data), dtype="b")[::2] + 127

        y_fft = np.fft.fft(data_int)
        self.line_fft.set_ydata(np.abs(y_fft[0:AUDIO_CHUNK_SIZE]) * 2 / (256 * AUDIO_CHUNK_SIZE))

        return self.line_fft,


class MatPlotLibModifiedSine:
    def __init__(self):
        plt.ion()
        plt.rcParams["toolbar"] = "None"

        fig, ax = plt.subplots(facecolor="black")
        fig_manager = plt.get_current_fig_manager()
        fig_manager.full_screen_toggle()
        fig.canvas.mpl_connect("button_press_event", lambda e: plt.close())

        ax.axis("off")
        ax.set_xlim(0, 110)
        ax.set_ylim(-5, 5)

        self.line, = ax.plot([], [], lw=2, color=(3/255, 160/255, 98/255))
        self.line.set_data([], [])

        self.anim = animation.FuncAnimation(fig, self.animate, frames=200, interval=20, blit=True)

    def animate(self, frame_num): 
        x = np.linspace(0, 110, 110)
        y = np.sin((x + frame_num) * (frame_num + 1))
        self.line.set_data(x, y)
        return self.line,


class PILVideo:
    def __init__(self, window, device_index, video_capture_func=PILVideoCapture):
        self.window = window
        self.device_index = device_index

        self.cap = video_capture_func(device_index)

        self.w, self.h = window.winfo_screenwidth(), window.winfo_screenheight()
        self.window.overrideredirect(1)
        self.window.geometry("%dx%d+0+0" % (self.w, self.h))
        self.window.focus_set()    
        self.window.bind("<Button>", lambda e: self.window.destroy())

        self.canvas = tkinter.Canvas(self.window, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack()
        self.canvas.configure(background='black', cursor="none")

        self.delay = 20
        self.update()

        self.window.mainloop()

    def update(self):
        frame = self.cap.get_frame()
        pil_image = Image.fromarray(frame).resize((self.w, self.h))

        imgWidth, imgHeight = pil_image.size
        if imgWidth > self.w or imgHeight > self.h:
            ratio = min(self.w / imgWidth, self.h / imgHeight)
            imgWidth = int(imgWidth * ratio)
            imgHeight = int(imgHeight * ratio)
            pil_image = pil_image.resize((imgWidth, imgHeight), Image.ANTIALIAS)
            
        self.photo = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(self.w / 2, self.h / 2, image=self.photo)
        self.window.after(self.delay, self.update)


#################### UTILITY FUNCTIONS ####################
def show_pil_image(pil_image):
    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))

    print(w, h)

    root.focus_set()    
    root.bind("<Button>", lambda e: root.destroy())

    canvas = tkinter.Canvas(root, width=w, height=h, highlightthickness=0)
    canvas.pack()
    canvas.configure(background='black', cursor="none")

    imgWidth, imgHeight = pil_image.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w / imgWidth, h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        pil_image = pil_image.resize((imgWidth, imgHeight), Image.ANTIALIAS)
        
    image = ImageTk.PhotoImage(pil_image)
    canvas.create_image(w / 2, h / 2, image=image)

    root.mainloop()


#################### PROGRAM FUNCTIONS ####################
def pride_flag():
    show_pil_image(Image.open("assets/progressprideflag.jpg"))


def camera():
    PILVideo(tkinter.Tk(), 0)


def edge_detection():
    PILVideo(tkinter.Tk(), 0, PILVideoCaptureEdgeDetection)


def trippy():
    PILVideo(tkinter.Tk(), "assets/trippy.mp4", PILVideoCaptureFile)


def monitor():
    show_pil_image(Image.open("assets/monitor.jpg"))


def modified_sine():
    MatPlotLibModifiedSine()
    

def waveform():
    WaveForm()


def spectrum_analyzer():
    SpectrumAnalyzer()
