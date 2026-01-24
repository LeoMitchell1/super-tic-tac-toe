from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt

class GameResultDialog(QDialog):
    def __init__(self, winner, parent=None):
        super().__init__(parent)

        # Frameless + translucent for rounded corners
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Main layout of the dialog
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Container frame with rounded corners
        self.container = QFrame()
        self.container.setObjectName("GameResultContainer")
        self.container.setMinimumSize(200, 100)  # <-- make frame bigger
        main_layout.addWidget(self.container)

        # Layout inside the container
        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.setSpacing(20)  # space between text and button

        # Result label
        result_text = "It's a Draw!" if winner == "Draw" else f"{winner} Wins!"
        result_label = QLabel(result_text)
        result_label.setObjectName("GameResultLabel")
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(result_label)

        # Restart button
        restart_btn = QPushButton("Restart Game")
        restart_btn.setObjectName("GameResultButton")
        restart_btn.clicked.connect(self.restart_game)
        container_layout.addWidget(restart_btn)

        self.parent_board = parent

    def restart_game(self):
        self.accept()
        if self.parent_board:
            self.parent_board.reset_game()
