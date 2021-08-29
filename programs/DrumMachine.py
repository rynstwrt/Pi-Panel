from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio


PAD_BUTTONS = {
    "kick": "assets/drumkit/kick4.wav",
    "kick 2": "assets/drumkit/kick5.wav",
    "snare": "assets/drumkit/snare2.wav",
    "snare 2": "assets/drumkit/snare3.wav",
    "clap": "assets/drumkit/clap1.wav",
    "clap 2": "assets/drumkit/clap2.wav",
    "hat": "assets/drumkit/hat2.wav",
    "hat 2": "assets/drumkit/hat3.wav"
}
NUM_ROWS = 4
NUM_COLS = 3


class DrumMachine(QWidget):
    def __init__(self):
        super(DrumMachine, self).__init__()

        style_sheet_file = QFile("stylesheets/drummachine.qss")
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

        self.pad_layout = QGridLayout()
        self.pad_layout.setSpacing(25)
        self.pad_layout.setContentsMargins(25, 25, 25, 25)

        layout.addLayout(self.pad_layout)
        layout.addStretch()
        self.setLayout(layout)
        self.show()


    def play_sample(self, path):
        audio = AudioSegment.from_mp3(path)
        _play_with_simpleaudio(audio)


    def create_buttons(self):
        button_index = 0

        for y in range(NUM_ROWS):
            for x in range(NUM_COLS):
                if button_index >= len(PAD_BUTTONS):
                    return

                button_name = list(PAD_BUTTONS.keys())[button_index]

                button = QPushButton(button_name)
                button.setProperty("isDrumMachineButton", ["true"])
                button.clicked.connect(lambda e, button_name=button_name: self.play_sample(PAD_BUTTONS[button_name]))
                self.pad_layout.addWidget(button, y, x)

                button_index += 1
