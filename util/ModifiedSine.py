import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class ModifiedSine:
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