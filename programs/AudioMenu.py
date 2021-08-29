from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout
from util.ModifiedSine import ModifiedSine
from util.WaveForm import WaveForm
from util.SpectrumAnalyzer import SpectrumAnalyzer


PROGRAMS = {
    "modified sine": ModifiedSine,
    "waveform": WaveForm,
    "spectrum analyzer": SpectrumAnalyzer
}
NUM_ROWS = 4
NUM_COLS = 3


class AudioMenu(QWidget):
    def __init__(self):
        super(AudioMenu, self).__init__()

        style_sheet_file = QFile("stylesheets/buttonmenu.qss")
        style_sheet_file.open(QFile.ReadOnly | QFile.Text)
        style_stream = QTextStream(style_sheet_file)
        style_sheet = style_stream.readAll()
        self.setStyleSheet(style_sheet)

        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
        layout = QVBoxLayout()

        exit_button = QPushButton("X")
        exit_button.setObjectName("exit")
        layout.addWidget(exit_button)
        exit_button.show()
        exit_button.clicked.connect(lambda e: self.close())

        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(25)
        self.button_layout.setContentsMargins(25, 25, 25, 25)

        layout.addLayout(self.button_layout)
        layout.addStretch()
        self.setLayout(layout)
        self.show()


    def create_buttons(self):
        button_index = 0

        for y in range(NUM_ROWS):
            for x in range(NUM_COLS):
                if button_index >= len(PROGRAMS):
                    return

                button_name = list(PROGRAMS.keys())[button_index]
                program_class = PROGRAMS[button_name]

                button = QPushButton(button_name)
                button.setProperty("isContentButton", ["true"])
                button.clicked.connect(lambda e, program_class=program_class: program_class())

                self.button_layout.addWidget(button, y, x)

                button_index += 1
