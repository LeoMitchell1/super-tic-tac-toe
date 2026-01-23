from PyQt6.QtWidgets import QWidget, QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import QSize
from .mini_game import MiniGame


class Board(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_player = "X"
        self.active_mini_game = None

        outer_layout = QGridLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        board_frame = QFrame(self)
        board_frame.setObjectName("boardFrame")
        board_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        outer_layout.addWidget(board_frame)

        board_layout = QGridLayout(board_frame)
        board_layout.setSpacing(15)
        board_layout.setContentsMargins(15, 15, 15, 15)

        for i in range(3):
            board_layout.setRowStretch(i, 1)
            board_layout.setColumnStretch(i, 1)


        self.mini_games = [[None for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                mini_game = MiniGame(row, col)
                board_layout.addWidget(mini_game, row, col)
                self.mini_games[row][col] = mini_game

                mini_game.square_clicked.connect(self.handle_square_click)
                mini_game.square_hovered.connect(self.highlight_mini_game_hover)

    def handle_square_click(self, square, mini_game_row, mini_game_col):
        # If an active mini_game is set, only allow moves inside it
        if self.active_mini_game is not None:
            if self.active_mini_game != (mini_game_row, mini_game_col):
                return  # Ignore clicks outside the active mini_game

        if square.state is not None:
            return

        square.set_state(self.current_player)

        # Determine the next active mini_game based on clicked square's position
        self.active_mini_game = (square.row, square.col)

        # Highlight only the active mini_game
        self.update_mini_game_highlights()

        # Switch turns
        self.current_player = "O" if self.current_player == "X" else "X"

        if self.current_player == "X":
            self.update_board_colour("#ff4d4d")  # red for X
        else:
            self.update_board_colour("#4d79ff")  # blue for O

        # self.check_winner()

    def update_mini_game_highlights(self):
        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                if self.active_mini_game == (r, c):
                    mini_game.setStyleSheet("border-color: #5f5f5f")  # keep highlighted
                    mini_game.set_overlay_colour("#5f5f5f")
                else:
                    mini_game.setStyleSheet("border-color: #b4b4b4")
                    mini_game.set_overlay_colour("#b4b4b4")

    def highlight_mini_game_hover(self, mini_game_row, mini_game_col, hovering):
        # Only show hover if no active mini_game, otherwise ignore
        if self.active_mini_game is None:
            mini_game = self.mini_games[mini_game_row][mini_game_col]
            if hovering:
                mini_game.setStyleSheet("border-color: #5f5f5f")
                mini_game.set_overlay_colour("#5f5f5f")
            else:
                mini_game.setStyleSheet("border-color: #b4b4b4")
                mini_game.set_overlay_colour("#b4b4b4")

    def update_board_colour(self, colour):
        self.setStyleSheet(f"border-color: {colour};")

    def reset_game(self):
        self.current_player = "X"
        self.active_mini_game = None

        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                mini_game.setStyleSheet("border-color: #b4b4b4")
                mini_game.set_overlay_colour("#b4b4b4")

                # Reset all squares in this mini_game
                layout = mini_game.layout()
                for i in range(layout.count()):
                    square = layout.itemAt(i).widget()
                    square.set_state(None)

    def sizeHint(self):
        return QSize(600, 600)

