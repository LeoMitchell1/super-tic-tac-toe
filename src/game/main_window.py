from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt
from .board import Board


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super Tic Tac Toe")
        self.setFixedSize(700, 750)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        self.board = Board()
        layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignCenter)

        controls = QHBoxLayout()
        controls.setSpacing(100)

        restart = QPushButton("Restart")
        restart.setObjectName("restartButton")
        restart.clicked.connect(self.board.reset_game)

        quit_btn = QPushButton("Quit")
        quit_btn.setObjectName("quitButton")
        quit_btn.clicked.connect(self.close)

        controls.addStretch()
        controls.addWidget(restart)
        controls.addWidget(quit_btn)
        controls.addStretch()

        layout.addLayout(controls)
