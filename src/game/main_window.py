from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from .board import Board


class MainWindow(QMainWindow):
    def __init__(self, mode="Player vs Player", difficulty=None):
        super().__init__()

        self.mode = mode
        self.difficulty = difficulty

        self.setWindowTitle("Super Tic Tac Toe")
        self.setFixedSize(700, 750)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        self.board = Board(difficulty=self.difficulty if self.mode == "Player vs AI" else None)
        layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignCenter)

        controls = QHBoxLayout()
        controls.setSpacing(100)

        restart = QPushButton("Restart")
        restart.setObjectName("restartButton")
        restart.clicked.connect(self.board.reset_game)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.back)

        controls.addStretch()
        controls.addWidget(restart)
        controls.addWidget(back_btn)
        controls.addStretch()

        layout.addLayout(controls)

        # (Optional debug)
        print(f"Game mode: {self.mode}, difficulty: {self.difficulty}")

    def back(self):
        from .menu_window import MenuWindow
        
        self.menu_window = MenuWindow()
        self.menu_window.show()

        self.close()

