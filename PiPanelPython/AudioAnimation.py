import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys

class Plot2D():
    def __init__(self):
        self.traces = dict()
        self.phase = 0
        self.t = np.arange(0, 3.0, 0.01)

        pg.setConfigOptions(antialias=True)
        
        self.app = QtGui.QApplication([])
        
        self.win = pg.GraphicsWindow(title="Audio Visualizer")
        self.win.resize(1024, 600)
        self.win.setWindowTitle("Audio Visualizer")

        self.canvas = self.win.addPlot()


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
            QtGui.QApplication.instance().exec_()


    def trace(self, name, dataset_x, dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x, dataset_y)
        else:
            self.traces[name] = self.canvas.plot(pen="y")

    
    def update(self):
        s = np.sin(2 * np.pi * self.t + self.phase)
        c = np.cos(2 * np.pi * self.t + self.phase)
        self.trace("sin", self.t, s)
        self.trace("cos", self.t, c)
        self.phase += 0.1
        

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(30)
        self.start()


if __name__ == "__main__":
    p = Plot2D()
    p.animation()