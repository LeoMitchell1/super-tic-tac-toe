from PyQt6.QtWidgets import QWidget, QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import QSize
from .mini_game import MiniGame
from .game_result import GameResultDialog
from styling.colours import RED, BLUE, HIGHLIGHT, GRID


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
        
        # Initialize playable squares and highlights so hover works at startup
        self.update_playable_mini_games()
        self.update_mini_game_highlights()


    def handle_square_click(self, square, mini_game_row, mini_game_col):
        clicked_mini_game = self.mini_games[mini_game_row][mini_game_col]
        # If an active mini_game is set, only allow moves inside it
        if self.active_mini_game is not None:
            if self.active_mini_game != (mini_game_row, mini_game_col):
                return  # Ignore clicks outside the active mini_game

        if square.state is not None:
            return
        
        if clicked_mini_game.winner is not None or clicked_mini_game.is_full:
            return  # Ignore clicks in a mini_game that already has a winner or is full

        square.set_state(self.current_player)

        if clicked_mini_game.check_winner() is not None or clicked_mini_game.is_full:
            self.active_mini_game = None  # No active mini_game if the current one is won or full
            self.update_mini_game_highlights()

        # Determine the next active mini_game based on clicked square
        next_row, next_col = square.row, square.col
        next_mini_game = self.mini_games[next_row][next_col]

        # Only force the next mini-game if it's playable
        if next_mini_game.winner is None and not next_mini_game.is_full:
            self.active_mini_game = (next_row, next_col)
        else:
            self.active_mini_game = None  # free move anywhere

        # Update highlights
        self.update_mini_game_highlights()

        self.update_playable_mini_games()

        # Switch turns
        self.current_player = "O" if self.current_player == "X" else "X"

        if self.current_player == "X":
            self.update_board_colour(RED)  # red for X
        else:
            self.update_board_colour(BLUE)  # blue for O

        self.check_overall_winner()

    def update_mini_game_highlights(self):
        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                if self.active_mini_game == (r, c): #  highlight active mini-game
                    mini_game.setStyleSheet(f"border-color: {HIGHLIGHT}")
                    mini_game.set_overlay_colour(f"{HIGHLIGHT}")
                else:
                    mini_game.setStyleSheet(f"border-color: {GRID}")
                    mini_game.set_overlay_colour(GRID)

    def highlight_mini_game_hover(self, mini_game_row, mini_game_col, hovering):
        if self.active_mini_game is None:
            mini_game = self.mini_games[mini_game_row][mini_game_col]
            if hovering and mini_game.winner is None and not mini_game.is_full: #  highlight hover
                mini_game.setStyleSheet(f"border-color: {HIGHLIGHT}")
                mini_game.set_overlay_colour(f"{HIGHLIGHT}")
            else:
                mini_game.setStyleSheet(f"border-color: {GRID}")
                mini_game.set_overlay_colour(GRID)

    def update_playable_mini_games(self):
        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                if self.active_mini_game is None:
                    mini_game.playable = True
                else:
                    mini_game.playable = (self.active_mini_game == (r, c))

                mini_game.set_playable_squares()

    def update_board_colour(self, colour):
        self.setStyleSheet(f"border-color: {colour};")

    def check_overall_winner(self):
        # Check rows and columns
        for i in range(3):
            if (self.mini_games[i][0].winner is not None and
                self.mini_games[i][0].winner == self.mini_games[i][1].winner == self.mini_games[i][2].winner):
                self.display_winner(self.mini_games[i][0].winner)
            if (self.mini_games[0][i].winner is not None and
                self.mini_games[0][i].winner == self.mini_games[1][i].winner == self.mini_games[2][i].winner):
                self.display_winner(self.mini_games[0][i].winner)

        # Check diagonals
        if (self.mini_games[0][0].winner is not None and
            self.mini_games[0][0].winner == self.mini_games[1][1].winner == self.mini_games[2][2].winner):
            self.display_winner(self.mini_games[0][0].winner)
        if (self.mini_games[0][2].winner is not None and
            self.mini_games[0][2].winner == self.mini_games[1][1].winner == self.mini_games[2][0].winner):
            self.display_winner(self.mini_games[0][2].winner)

        # Check for draw
        if all(self.mini_games[r][c].winner is not None or self.mini_games[r][c].is_full
               for r in range(3) for c in range(3)):
                    self.display_winner("Draw")

        return None
    
    def display_winner(self, winner):
        # Disable all mini-games
        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                mini_game.playable = False
                mini_game.set_playable_squares()

        # Show modern pop-up
        dialog = GameResultDialog(winner, parent=self)
        dialog.exec()

    def reset_game(self):
        self.current_player = "X"
        self.active_mini_game = None

        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                mini_game.reset()

        self.update_board_colour(RED)
        self.update_mini_game_highlights()
                
    def sizeHint(self):
        return QSize(600, 600)

