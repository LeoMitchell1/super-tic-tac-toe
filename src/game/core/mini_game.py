from PyQt6.QtWidgets import QFrame, QGridLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal
from .board_square import BoardSquare
from ..ui.grid_overlay import GridOverlay
from ..ui.winner_overlay import WinnerOverlay

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
        self.winner_overlay = None
        self.squares = [[None for _ in range(3)] for _ in range(3)]
        self.playable = True  # Whether this mini-game can be played in

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

        if self.winner_overlay:
            self.winner_overlay.setGeometry(self.rect())

        super().resizeEvent(event)

    def check_winner(self):
        # Don't re-check if there's already a winner
        if self.winner is not None:
            return self.winner
        
        # Check rows and columns
        for i in range(3):
            if (self.squares[i][0].state == self.squares[i][1].state ==
                self.squares[i][2].state) and self.squares[i][0].state is not None:
                self.winner = self.squares[i][0].state
                self.display_winner()
                return self.winner
            if (self.squares[0][i].state == self.squares[1][i].state ==
                self.squares[2][i].state) and self.squares[0][i].state is not None:
                self.winner = self.squares[0][i].state
                self.display_winner()
                return self.winner

        # Check diagonals
        if (self.squares[0][0].state == self.squares[1][1].state ==
            self.squares[2][2].state) and self.squares[0][0].state is not None:
            self.winner = self.squares[0][0].state
            self.display_winner()
            return self.winner

        if (self.squares[0][2].state == self.squares[1][1].state ==
            self.squares[2][0].state) and self.squares[0][2].state is not None:
            self.winner = self.squares[0][2].state
            self.display_winner()
            return self.winner

        # Check for draw
        if all(self.squares[r][c].state is not None for r in range(3) for c in range(3)):
            self.is_full = True

        return None
    
    def display_winner(self):
        if self.winner is not None:
            self.winner_overlay = WinnerOverlay(self)
            self.winner_overlay.setGeometry(self.rect())
            self.winner_overlay.show()

    def set_playable_squares(self):
        for r in range(3):
            for c in range(3):
                self.squares[r][c].playable = self.playable

    def reset(self):
        self.winner = None
        self.is_full = False
        self.playable = True

        if self.winner_overlay:
            self.winner_overlay.deleteLater()
            self.winner_overlay = None

        for r in range(3):
            for c in range(3):
                self.squares[r][c].set_state(None)
                self.squares[r][c].playable = True
                self.squares[r][c].update_background()  # reset background

    def refresh_hovers(self):
        for r in range(3):
            for c in range(3):
                self.squares[r][c].update_background()
            



        


