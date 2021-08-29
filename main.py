from PyQt5.QtCore import Qt, QFile, QTextStream, QDate, QTime, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QScrollArea, QSizePolicy, QGridLayout
from PyQt5.QtGui import QPalette, QPixmap
from util.program import Program
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
from dotenv import Dotenv
import programrouter
import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


dotenv = Dotenv(".env")


BUTTON_ROWS = 5
BUTTON_COLS = 2
BUTTON_PROGRAMS = [
    Program("image\nmenu", programrouter.image_menu),
    Program("video\nmenu", programrouter.video_menu),
    Program("computer\nvision", programrouter.computer_vision_menu),
    Program("audio\nmenu", programrouter.audio_menu),
    Program("drum\nmachine", programrouter.drum_machine),
    Program("led\nmatrix", programrouter.led_matrix)
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
        style_sheet_file = QFile("stylesheets/main.qss")
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
        self.right_layout.setSpacing(15)
        self.right_layout.setContentsMargins(15, 15, 15, 15)

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
        self.update_time()
        self.time_label.show()

        # Create the date
        self.date_label = QLabel("Tuesday, January 17")
        self.date_label.setObjectName("date")
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.date_label)
        self.update_date()
        self.date_label.show()

        # Create the weather row (icon and temperature)
        weather_row = QHBoxLayout()
        weather_row.setSpacing(0)
        weather_row.addStretch()

        # Create the weather icon
        self.weather_image = QLabel()
        self.weather_image.setObjectName("weathericon")
        self.weather_image.setAlignment(Qt.AlignCenter)
        self.weather_image.setContentsMargins(0, 0, 0, 0)
        self.weather_image.show()
        weather_row.addWidget(self.weather_image)

        # Create the temperature
        self.temperature = QLabel()
        self.temperature.setObjectName("temperature")
        self.temperature.setAlignment(Qt.AlignCenter)
        self.temperature.setContentsMargins(0, 0, 0, 0)
        self.temperature.show()
        weather_row.addWidget(self.temperature)

        # Finish creating the weather row
        weather_row.addStretch()
        left_layout.addLayout(weather_row)
        self.update_weather()

        # Make the left layout start at the top
        left_layout.addStretch()

        # Add layouts to the main layout
        layout.addLayout(left_layout, stretch=1)
        layout.addLayout(self.right_layout, stretch=1)

        # Set up container widget and set centralized widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Create a timer for updating the time 
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(5000)

        # Create a timer for updating the date 
        self.date_timer = QTimer()
        self.date_timer.timeout.connect(self.update_date)
        self.date_timer.start(5000)

        # Create a timer for updating the weather row
        self.weather_timer = QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(600000) # every 10 minutes

        # Create the program buttons
        self.create_buttons()

        # Make program buttons be at the top and spaced out
        self.right_layout.setRowStretch(self.right_layout.rowCount(), 1)


    def update_time(self):
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


    def update_date(self):
        current_date = QDate.currentDate().toString()
        split_date = current_date.split(" ")
        split_date.pop()

        if int(split_date[2]) < 10:
            split_date[2] = "0{}".format(split_date[2])

        current_date = " ".join(split_date)
        self.date_label.setText(current_date)


    def update_weather(self):
        try:
            api_key = dotenv["WEATHER_API_KEY"]
            data = json.loads(urlopen("https://api.weatherbit.io/v2.0/current?city=Plano,TX&country=US&key={}&units=I".format(api_key)).read().decode("utf-8"))["data"][0]
            
            weather_icon_url = "https://www.weatherbit.io/static/img/icons/{}.png".format(data["weather"]["icon"])
            temperature_string = "{}°F".format(round(data["temp"]))

            icon_data = urlopen(weather_icon_url).read()
            icon_pixmap = QPixmap(50, 50)
            icon_pixmap.loadFromData(icon_data)
            self.weather_image.setPixmap(icon_pixmap)
            self.weather_image.setScaledContents(True)

            self.temperature.setText(temperature_string)
        except HTTPError:
            pass
        except URLError:
            pass


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

                self.right_layout.addWidget(button, y, x, alignment=Qt.AlignHCenter)

                num_buttons += 1


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Breeze")

    window = MainWindow()
    window.show()

    app.exec()