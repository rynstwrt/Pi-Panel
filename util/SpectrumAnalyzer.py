import pyaudio
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import struct

AUDIO_RATE = 16000
AUDIO_CHUNK_SIZE = 400
AUDIO_AMPLITUDE = 200

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

        self.anim = animation.FuncAnimation(fig, self.animate, interval=1, blit=True)

    
    def animate(self, frame_num):
        data = self.stream.read(AUDIO_CHUNK_SIZE)

        data_int = np.array(struct.unpack(str(2 * AUDIO_CHUNK_SIZE) + "B", data), dtype="b")[::2] + 127

        y_fft = np.fft.fft(data_int)
        self.line_fft.set_ydata(np.abs(y_fft[0:AUDIO_CHUNK_SIZE]) * 2 / (256 * AUDIO_CHUNK_SIZE))

        return self.line_fft,
