import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
from PyQt5.QtCore import Qt, QFile, QTextStream, QDate, QTime, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QScrollArea, QSizePolicy, QGridLayout
from PyQt5.QtGui import QPalette
from util.program import Program
import programs


BUTTON_ROWS = 5
BUTTON_COLS = 2
BUTTON_PROGRAMS = [
    Program("pride flag", programs.pride_flag),
    Program("camera", programs.camera),
    Program("edge\ndetection", programs.edge_detection),
    Program("monitor", programs.monitor),
    Program("bunny\nvideo", programs.bunny_video),
    Program("modified\nsine", programs.modified_sine),
    Program("waveform", programs.waveform),
    Program("spectrum\nanalyzer", programs.spectrum_analyzer)
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        # Set the window title, make fullscreen, and hide mouse cursor
        self.setWindowTitle("PiPanel 2")
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
        self.setObjectName("centralWidget")

        # Load the style sheet
        style_sheet_file = QFile("styles.qss")
        style_sheet_file.open(QFile.ReadOnly | QFile.Text)
        style_stream = QTextStream(style_sheet_file)
        style_sheet = style_stream.readAll()
        self.setStyleSheet(style_sheet)

        # Create the main layout, left layout, and right layout    
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)
        self.right_layout = QGridLayout()
        self.right_layout.setSpacing(0)

        # Create the exit button
        exit_button = QPushButton("X")
        exit_button.setObjectName("exit")
        left_layout.addWidget(exit_button)
        exit_button.show()
        exit_button.clicked.connect(lambda e: self.close())

        # Create the time
        self.time_label = QLabel("00:00")
        self.time_label.setObjectName("time")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.time_label)
        self.update_time_widget()
        self.time_label.show()

        # Create the date
        self.date_label = QLabel("Tuesday, January 17")
        self.date_label.setObjectName("date")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.date_label)
        self.update_date_widget()
        self.date_label.show()

        # Make the left layout start at the top
        left_layout.addStretch()

        # Add layouts to the main layout
        layout.addLayout(left_layout)
        layout.addLayout(self.right_layout)

        # Set up container widget and set centralized widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Create a timer for updating the time widget
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time_widget)
        self.time_timer.start(5000)

        # Create a timer for updating the date widget
        self.date_timer = QTimer()
        self.date_timer.timeout.connect(self.update_date_widget)
        self.date_timer.start(5000)

        # Create the program buttons
        self.create_buttons()

        # Make program buttons be at the top and spaced out
        self.right_layout.setRowStretch(self.right_layout.rowCount(), 1)


    def update_time_widget(self):
        current_time = QTime.currentTime()
        hour = current_time.hour()
        minutes = current_time.minute()

        if hour > 12:
            hour -= 12

        if hour == 0:
            hour = 12

        if hour < 10:
            hour = "0{}".format(hour)

        if minutes < 10:
            minutes = "0{}".format(minutes)

        self.time_label.setText("{}:{}".format(hour, minutes))


    def update_date_widget(self):
        current_date = QDate.currentDate().toString()
        split_date = current_date.split(" ")
        split_date.pop()

        if int(split_date[2]) < 10:
            split_date[2] = "0{}".format(split_date[2])

        current_date = " ".join(split_date)
        self.date_label.setText(current_date)


    def create_buttons(self):
        num_buttons = 0

        for y in range(BUTTON_ROWS):
            for x in range(BUTTON_COLS):
                if num_buttons >= len(BUTTON_PROGRAMS):
                    break

                program = BUTTON_PROGRAMS[num_buttons]

                button = QPushButton(program.name)
                button.clicked.connect(program.function)
                button.show()
                button.setProperty("isProgramButton", ["true"])

                self.right_layout.addWidget(button, y, x, 1, 1, alignment=Qt.AlignHCenter)

                num_buttons += 1


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Breeze")

    window = MainWindow()
    window.show()

    app.exec()