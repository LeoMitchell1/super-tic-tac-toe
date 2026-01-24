from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from .main_window import MainWindow

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super Tic Tac Toe")
        self.setFixedSize(400, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Super Tic Tac Toe")
        title.setObjectName("MenuTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.mode_selector = QComboBox()
        self.mode_selector.setObjectName("MenuComboBox")
        self.mode_selector.addItems(["Player vs Player", "Player vs AI"])
        layout.addWidget(self.mode_selector)

        self.difficulty_selector = QComboBox()
        self.difficulty_selector.setObjectName("MenuComboBox")
        self.difficulty_selector.addItems(["Easy", "Medium", "Hard"])
        layout.addWidget(self.difficulty_selector)

        start_btn = QPushButton("Start Game")
        start_btn.setObjectName("MenuButton")
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn)

    def start_game(self):
        mode = self.mode_selector.currentText()
        difficulty = self.difficulty_selector.currentText()

        self.main_window = MainWindow(mode=mode, difficulty=difficulty)
        self.main_window.show()

        self.close()
