import requests
import json
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout


DEFAULT_COLOR = "#FF00FF"
DEFAULT_TEXT = "SAMPLE TEXT"
BUTTONS = {
    "off": [],
    "rgb": [],
    "theater chase rainbow": [],
    "fill and unfill": [DEFAULT_COLOR],
    "sparkle": [DEFAULT_COLOR],
    "rainbow cycle": [],
    "scrolling text": [DEFAULT_COLOR, DEFAULT_TEXT],
    "rainbow scrolling text": [DEFAULT_TEXT],
    "progress pride flag": [],
    "camera": [],
    "equalizer": [DEFAULT_COLOR],
    "rainbow equalizer": [],
    "clock": [DEFAULT_COLOR],
    "blocks": [],
    "squiggle": [DEFAULT_COLOR],
    "hypnotize": [DEFAULT_COLOR],
    "snake": [DEFAULT_COLOR],
    "object tracking": []
}
NUM_ROWS = 4
NUM_COLS = 4


class LedMatrixController(QWidget):
    def __init__(self):
        super(LedMatrixController, self).__init__()

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
                if button_index >= len(BUTTONS):
                    return

                program_name = list(BUTTONS.keys())[button_index]
                args = BUTTONS[program_name]

                button = QPushButton(program_name.replace(" ", "\n"))
                button.setProperty("isContentButton", ["true"])
                button.clicked.connect(lambda e, program_name=program_name, args=args: self.set_program(program_name, args))

                self.button_layout.addWidget(button, y, x)

                button_index += 1


    def set_program(self, program_name, args):
        data = { "mode_name": program_name }

        for i in range(len(args)):
            if args[i] == DEFAULT_COLOR:
                data["mode_color"] = args[i]
            elif args[i] == DEFAULT_TEXT:
                data["mode_text"] = args[i]

        requests.post("http://10.164.1.124:8000/setmode", data=json.dumps(data))