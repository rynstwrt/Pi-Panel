import tkinter
from PIL import Image, ImageTk
from VideoCapture import VideoCapture
import cv2
import pyaudio
from PILVideo import PILVideo
from PILVideoCaptures import PILVideoCapture, PILVideoCaptureEdgeDetection, PILVideoCaptureFile
from PILAudio import PILAudio
from tkvideo import tkvideo
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
    # PILVideo(tkinter.Tk(), "assets/trippy.mp4", PILVideoCaptureFile)
    app = QApplication([])

    window = QWidget()
    window.setGeometry(0, 0, 1024, 600)


def program_monitor():
    show_pil_image(Image.open("assets/monitor.jpg"))


def program_modified_sine():
    plt.rcParams["toolbar"] = "None"

    fig, ax = plt.subplots(facecolor="black")
    fig_manager = plt.get_current_fig_manager()
    fig_manager.full_screen_toggle()
    fig.canvas.mpl_connect("button_press_event", lambda e: plt.close())

    ax.axis("off")
    ax.set_xlim(0, 110)
    ax.set_ylim(-5, 5)

    line, = ax.plot([], [], lw=2, color=(3/255, 160/255, 98/255))
    line.set_data([], [])

    def animate(frame_num): 
        x = np.linspace(0, 110, 110)
        y = np.sin((x + frame_num) * (frame_num + 1))
        line.set_data(x, y)
        return line,

    anim = animation.FuncAnimation(fig, animate, frames=200, interval=20, blit=True)
    plt.show()


def program_waveform(zoom_factor=4):
    p = pyaudio.PyAudio()

    stream = p.open(
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

    line, = ax.plot(x, np.random.rand(AUDIO_CHUNK_SIZE), lw=2, color=(3/255, 160/255, 98/255))

    ax.axis("off")
    ax.set_xlim(0, AUDIO_CHUNK_SIZE / zoom_factor)
    ax.set_ylim(-AUDIO_AMPLITUDE, AUDIO_AMPLITUDE)

    def animate(frame_num): 
        data = stream.read(AUDIO_CHUNK_SIZE)

        data_int = np.array(struct.unpack(str(2 * AUDIO_CHUNK_SIZE) + "B", data), dtype="b")[::2] + 127
        data_int = data_int.reshape(-1, zoom_factor).mean(axis=1)

        line.set_xdata(np.arange(len(data_int)))
        line.set_ydata(data_int)

        return line,

    anim = animation.FuncAnimation(fig, animate, frames=len(x), interval=0, blit=True)
    plt.show()


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

    plt.rcParams["toolbar"] = "None"

    fig, ax = plt.subplots(facecolor="black")
    fig_manager = plt.get_current_fig_manager()
    fig_manager.full_screen_toggle()
    fig.canvas.mpl_connect("button_press_event", lambda e: plt.close())

    x_fft = np.linspace(0, AUDIO_RATE, AUDIO_CHUNK_SIZE)

    line_fft, = ax.semilogx(x_fft, np.random.rand(AUDIO_CHUNK_SIZE), lw=2, color=(3/255, 160/255, 98/255))

    ax.axis("off")
    ax.set_ylim(-.03, .07)
    ax.set_xlim(20, AUDIO_RATE)

    def animate(frame_num): 
        data = stream.read(AUDIO_CHUNK_SIZE)

        data_int = np.array(struct.unpack(str(2 * AUDIO_CHUNK_SIZE) + "B", data), dtype="b")[::2] + 127

        y_fft = np.fft.fft(data_int)
        line_fft.set_ydata(np.abs(y_fft[0:AUDIO_CHUNK_SIZE]) * 2 / (256 * AUDIO_CHUNK_SIZE))

        return line_fft,

    anim = animation.FuncAnimation(fig, animate, interval=0, blit=True)
    plt.show()
