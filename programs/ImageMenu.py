from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout
from util.FullscreenImageWindow import FullscreenImageWindow 


IMAGES = {
    "pride\nflag": "assets/progressprideflag.jpg",
    "monitor": "assets/monitor.jpg",
    "beach": "assets/beach.jpg",
    "mountains": "assets/mountains.jpg",
    "retro\ncity": "assets/retrocity.jpg"
}
NUM_ROWS = 4
NUM_COLS = 3


class ImageMenu(QWidget):
    def __init__(self):
        super(ImageMenu, self).__init__()

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
                if button_index >= len(IMAGES):
                    return

                button_name = list(IMAGES.keys())[button_index]
                image_location = IMAGES[button_name]

                button = QPushButton(button_name)
                button.setProperty("isContentButton", ["true"])
                button.clicked.connect(lambda e, image_location=image_location: FullscreenImageWindow(image_location))

                self.button_layout.addWidget(button, y, x)

                button_index += 1
