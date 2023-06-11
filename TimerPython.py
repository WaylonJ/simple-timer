import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox, QWidget, QLCDNumber, QSlider
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.time_left = 0

        self.initUI()

    def initUI(self):
        light_color = QColor(199, 66, 75)
        light_color_string = "199, 66, 75"
        dark_color = QColor(89, 10, 15)
        # Set window size, title and color
        self.setWindowTitle('Timer')
        self.setGeometry(300, 300, 200, 200)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint | Qt.WindowStaysOnTopHint)

        p = self.palette()
        p.setColor(self.backgroundRole(), dark_color)
        p.setColor(self.foregroundRole(), light_color)
        self.setPalette(p)

        self.timer.timeout.connect(self.update_timer)

        self.layout = QVBoxLayout()

        self.label = QLCDNumber()
        self.label.display(self.format_time(self.time_left))
        self.layout.addWidget(self.label)

        self.button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setStyleSheet("background-color: rgb(" + light_color_string + ");")
        self.button_layout.addWidget(self.start_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        self.reset_button.setStyleSheet("background-color: rgb(" + light_color_string + ");")
        self.button_layout.addWidget(self.reset_button)

        self.dropdown = QComboBox()
        for i in range(1, 13):
            self.dropdown.addItem(f"{i * 5} minutes")
        self.dropdown.setStyleSheet("background-color: rgb(" + light_color_string + ");")
        self.dropdown.currentIndexChanged.connect(self.set_timer)
        self.button_layout.addWidget(self.dropdown)

        self.layout.addLayout(self.button_layout)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.set_transparency)
        self.layout.addWidget(self.slider)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def start_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("Resume")
        else:
            self.timer.start(1000)
            self.start_button.setText("Pause")

    def reset_timer(self):
        self.timer.stop()
        self.time_left = int(self.dropdown.currentIndex() + 1) * 5 * 60
        self.label.display(self.format_time(self.time_left))
        self.start_button.setText("Start")

    def set_timer(self):
        self.reset_timer()

    def update_timer(self):
        self.time_left -= 1
        if self.time_left <= 0:
            self.reset_timer()
        self.label.display(self.format_time(self.time_left))

    def set_transparency(self, value):
        self.setWindowOpacity(value / 100)

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
