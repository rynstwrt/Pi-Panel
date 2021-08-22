import pyaudio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import struct


AUDIO_RATE = 16000
AUDIO_CHUNK_SIZE = 400
AUDIO_AMPLITUDE = 200


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

        self.anim = animation.FuncAnimation(fig, self.animate, frames=len(x), interval=1, blit=True)


    def animate(self, frame_num): 
        data = self.stream.read(AUDIO_CHUNK_SIZE, False)

        data_int = np.array(struct.unpack(str(2 * AUDIO_CHUNK_SIZE) + "B", data), dtype="b")[::2]

        self.line.set_xdata(np.arange(len(data_int)))
        self.line.set_ydata(data_int)

        return self.line,