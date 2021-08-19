import tkinter
from PIL import Image, ImageTk
from VideoCapture import VideoCapture
import cv2
import pyaudio
from PILVideo import PILVideo
from PILVideoCaptures import PILVideoCapture, PILVideoCaptureEdgeDetection, PILVideoCaptureFile
from PILAudio import PILAudio
from tkvideo import tkvideo

#################### CONSTANTS ####################
AUDIO_CHUNK_SIZE = 4096
AUDIO_RATE = 32000
AUDIO_ZOOM_FACTOR = 1
AUDIO_AMPLITUDE = 150


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
def program_pride_flag():
    show_pil_image(Image.open("assets/progressprideflag.jpg"))


def program_camera():
    PILVideo(tkinter.Tk(), 0)


def program_edge_detection():
    PILVideo(tkinter.Tk(), 0, PILVideoCaptureEdgeDetection)


def program_equalizer(num_cols=8):
    PILAudio(tkinter.Tk(), num_cols)


def program_trippy():
    PILVideo(tkinter.Tk(), "assets/trippy.mp4", PILVideoCaptureFile)


def program_monitor():
    show_pil_image(Image.open("assets/monitor.jpg"))


def program_spectrum_analyzer():
    print("A")

import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
def program_spectrum_analyzer():
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=AUDIO_RATE,
        input=True,
        output=True,
        frames_per_buffer=AUDIO_CHUNK_SIZE
    )

    plt.rcParams['toolbar'] = 'None'

    fig, (ax, ax2) = plt.subplots(2, figsize=(15, 8))
    fig.show()
    fig.canvas.draw()
    
    fig_manager = plt.get_current_fig_manager()
    fig_manager.full_screen_toggle()

    x = np.arange(0, 2 * AUDIO_CHUNK_SIZE, 2)
    x_fft = np.linspace(0, AUDIO_RATE, AUDIO_CHUNK_SIZE)


    line, = ax.plot(x, np.random.rand(AUDIO_CHUNK_SIZE))
    line_fft, = ax2.semilogx(x_fft, np.random.rand(AUDIO_CHUNK_SIZE), "-", lw=2)

    ax.set_ylim(-AUDIO_AMPLITUDE, AUDIO_AMPLITUDE)
    ax.set_xlim(0, AUDIO_CHUNK_SIZE / AUDIO_ZOOM_FACTOR)

    ax2.set_ylim(0, 0.1)
    ax2.set_xlim(20, AUDIO_RATE / 2)

    while True:
        data = stream.read(AUDIO_CHUNK_SIZE)

        data_int = np.array(struct.unpack(str(2 * AUDIO_CHUNK_SIZE) + "B", data), dtype="b")[::2] + 127
        data_int = data_int.reshape(-1, AUDIO_ZOOM_FACTOR).mean(axis=1)

        line.set_xdata(np.arange(len(data_int)))
        line.set_ydata(data_int)

        y_fft = np.fft.fft(data_int)
        line_fft.set_ydata(np.abs(y_fft[0:AUDIO_CHUNK_SIZE]) * 2 / (256 * AUDIO_CHUNK_SIZE))

        try:
            fig.canvas.draw()
            fig.canvas.flush_events()
        except TclError:
            break