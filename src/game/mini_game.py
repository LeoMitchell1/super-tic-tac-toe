from PyQt6.QtWidgets import QFrame, QGridLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal
from .board_square import BoardSquare
from .grid_overlay import GridOverlay

class MiniGame(QFrame):
    square_clicked = pyqtSignal(object, int, int)
    square_hovered = pyqtSignal(int, int, bool)

    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.winner = None  # 'X', 'O', or None
        self.is_full = False
        self.grid = None
        self.squares = [[None for _ in range(3)] for _ in range(3)]

        self.setMinimumSize(150, 150)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.create_grid()
        self.create_squares()
        self.overlay = self.create_overlay()

    def create_grid(self):
        self.grid = QGridLayout(self)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

    def create_squares(self):
        for r in range(3):
            for c in range(3):
                square = BoardSquare(row=r, col=c)
                self.squares[r][c] = square
                self.grid.addWidget(square, r, c)

                square.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                square.clicked.connect(
                    lambda checked, s=square:
                        self.square_clicked.emit(s, self.row, self.col)
                )

                square.hovered.connect(
                    lambda hovering:
                        self.square_hovered.emit(self.row, self.col, hovering)
                )

                if r == 0 and c == 0: square.setProperty("corner", "top-left")
                elif r == 0 and c == 2: square.setProperty("corner", "top-right") 
                elif r == 2 and c == 0: square.setProperty("corner", "bottom-left") 
                elif r == 2 and c == 2: square.setProperty("corner", "bottom-right")

    def create_overlay(self):
        overlay = GridOverlay(self)
        overlay.setGeometry(self.rect())
        overlay.raise_()

        return overlay
    
    def set_overlay_colour(self, colour):
        self.overlay.set_colour(colour)
        
    def resizeEvent(self, event):
        self.overlay.setGeometry(self.rect())
        super().resizeEvent(event)

