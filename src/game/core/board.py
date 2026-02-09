from PyQt6.QtWidgets import QWidget, QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import QSize, QTimer, pyqtSignal
from .mini_game import MiniGame
from ..ui.game_result import GameResultDialog
from styling.colours import RED, BLUE, HIGHLIGHT, GRID
import random
import time

class Board(QWidget):
    turn_changed = pyqtSignal()  # Signal emitted when turn changes
    game_over = pyqtSignal()  # Signal emitted when game ends
    
    def __init__(self, difficulty=None, parent=None, username=None):
        super().__init__(parent)
        
        self.current_player = "X"
        self.active_mini_game = None
        self.difficulty = difficulty  # None, "Easy", "Medium", or "Hard"
        self.ai_player = "O"  # AI always plays as O
        self.human_player = "X"  # Human always plays as X
        self.username = username
        self.score = 0
        self.start_time = None  # Track when first move is made
        self.time_taken = 0  # Time taken to complete the game
        self.time_cap = 240  # 4 minutes time cap for scoring
        
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
        # If AI mode and it's AI's turn, ignore human clicks
        if self.difficulty is not None and self.current_player == self.ai_player:
            return
            
        clicked_mini_game = self.mini_games[mini_game_row][mini_game_col]
        
        # If an active mini_game is set, only allow moves inside it
        if self.active_mini_game is not None:
            if self.active_mini_game != (mini_game_row, mini_game_col):
                return  # Ignore clicks outside the active mini_game

        if square.state is not None:
            return
        
        if clicked_mini_game.winner is not None or clicked_mini_game.is_full:
            return  # Ignore clicks in a mini_game that already has a winner or is full

        self.make_move(square, mini_game_row, mini_game_col)

    def make_move(self, square, mini_game_row, mini_game_col):
        # Start timing on the first move
        if self.start_time is None:
            self.start_time = time.time()
        
        clicked_mini_game = self.mini_games[mini_game_row][mini_game_col]
        
        # Place the mark
        square.set_state(self.current_player)

        # Check if this move won the mini-game
        mini_game_winner = clicked_mini_game.check_winner()
        
        if mini_game_winner is not None or clicked_mini_game.is_full:
            self.active_mini_game = None  # No active mini_game if the current one is won or full
            self.update_mini_game_highlights()

        # Determine the next active mini_game based on clicked square position
        next_row, next_col = square.row, square.col
        next_mini_game = self.mini_games[next_row][next_col]

        # Only force the next mini-game if it's playable (not won and not full)
        if next_mini_game.winner is None and not next_mini_game.is_full:
            self.active_mini_game = (next_row, next_col)
        else:
            # If the target mini-game is won or full, player can go anywhere
            self.active_mini_game = None

        # Update highlights
        self.update_mini_game_highlights()
        self.update_playable_mini_games()

        # Switch turns
        self.current_player = "O" if self.current_player == "X" else "X"

        if self.current_player == "X":
            self.update_board_colour(RED)  # red for X
        else:
            self.update_board_colour(BLUE)  # blue for O

        # Emit signal that turn has changed
        self.turn_changed.emit()

        # Check for winner before AI move
        if self.check_overall_winner():
            return
        
        # If AI mode and now it's AI's turn, make AI move after a short delay
        if self.difficulty is not None and self.current_player == self.ai_player:
            QTimer.singleShot(500, self.ai_make_move)  # 500ms delay for better UX

    def ai_make_move(self):
        if self.difficulty == "Easy":
            move = self.get_random_move()
        elif self.difficulty == "Medium":
            move = self.get_medium_move()
        elif self.difficulty == "Hard":
            move = self.get_hard_move()
        else:
            return
        
        if move:
            mini_game_row, mini_game_col, square_row, square_col = move
            mini_game = self.mini_games[mini_game_row][mini_game_col]
            square = mini_game.squares[square_row][square_col]
            self.make_move(square, mini_game_row, mini_game_col)

        

    def get_available_moves(self):
        moves = []
        
        if self.active_mini_game is not None:
            # Only moves in the active mini-game
            mg_row, mg_col = self.active_mini_game
            mini_game = self.mini_games[mg_row][mg_col]
            if mini_game.winner is None and not mini_game.is_full:
                for r in range(3):
                    for c in range(3):
                        if mini_game.squares[r][c].state is None:
                            moves.append((mg_row, mg_col, r, c))
        else:
            # Moves in any playable mini-game
            for mg_row in range(3):
                for mg_col in range(3):
                    mini_game = self.mini_games[mg_row][mg_col]
                    if mini_game.winner is None and not mini_game.is_full:
                        for r in range(3):
                            for c in range(3):
                                if mini_game.squares[r][c].state is None:
                                    moves.append((mg_row, mg_col, r, c))
        
        return moves

    def get_random_move(self):
        moves = self.get_available_moves()
        return random.choice(moves) if moves else None

    def get_medium_move(self):
        moves = self.get_available_moves()
        if not moves:
            return None
        
        # Try to win a mini-game
        for move in moves:
            mg_row, mg_col, sq_row, sq_col = move
            mini_game = self.mini_games[mg_row][mg_col]
            # Simulate move - save original state
            original_state = mini_game.squares[sq_row][sq_col].state
            mini_game.squares[sq_row][sq_col].state = self.ai_player
            
            # Manually check for win without calling check_winner()
            would_win = self.check_mini_game_win(mini_game, self.ai_player)
            
            # Restore original state
            mini_game.squares[sq_row][sq_col].state = original_state
            
            if would_win:
                return move
        
        # Try to block human from winning a mini-game
        for move in moves:
            mg_row, mg_col, sq_row, sq_col = move
            mini_game = self.mini_games[mg_row][mg_col]
            # Simulate human move - save original state
            original_state = mini_game.squares[sq_row][sq_col].state
            mini_game.squares[sq_row][sq_col].state = self.human_player
            
            # Manually check for win without calling check_winner()
            would_win = self.check_mini_game_win(mini_game, self.human_player)
            
            # Restore original state
            mini_game.squares[sq_row][sq_col].state = original_state
            
            if would_win:
                return move
        
        # Otherwise random
        return random.choice(moves)

    def get_hard_move(self):
        moves = self.get_available_moves()
        if not moves:
            return None
        
        # 1. Try to win the overall game
        for move in moves:
            mg_row, mg_col, sq_row, sq_col = move
            mini_game = self.mini_games[mg_row][mg_col]
            
            # Simulate winning this mini-game - save original state
            original_state = mini_game.squares[sq_row][sq_col].state
            original_winner = mini_game.winner
            
            mini_game.squares[sq_row][sq_col].state = self.ai_player
            
            # Check if this would win the mini-game
            if self.check_mini_game_win(mini_game, self.ai_player):
                # Temporarily set winner to check overall game
                mini_game.winner = self.ai_player
                would_win = self.would_win_game(self.ai_player)
                mini_game.winner = original_winner
                
                # Restore original state
                mini_game.squares[sq_row][sq_col].state = original_state
                
                if would_win:
                    return move
            
            # Restore original state
            mini_game.squares[sq_row][sq_col].state = original_state
        
        # 2. Block human from winning the overall game
        for move in moves:
            mg_row, mg_col, sq_row, sq_col = move
            mini_game = self.mini_games[mg_row][mg_col]
            
            # Simulate human winning this mini-game - save original state
            original_state = mini_game.squares[sq_row][sq_col].state
            original_winner = mini_game.winner
            
            mini_game.squares[sq_row][sq_col].state = self.human_player
            
            # Check if this would win the mini-game
            if self.check_mini_game_win(mini_game, self.human_player):
                # Temporarily set winner to check overall game
                mini_game.winner = self.human_player
                would_win = self.would_win_game(self.human_player)
                mini_game.winner = original_winner
                
                # Restore original state
                mini_game.squares[sq_row][sq_col].state = original_state
                
                if would_win:
                    return move
            
            # Restore original state
            mini_game.squares[sq_row][sq_col].state = original_state
        
        # 3. Fall back to medium strategy
        return self.get_medium_move()
    
    def check_mini_game_win(self, mini_game, player):
        squares = mini_game.squares
        
        # Check rows
        for i in range(3):
            if (squares[i][0].state == player and
                squares[i][1].state == player and
                squares[i][2].state == player):
                return True
        
        # Check columns
        for i in range(3):
            if (squares[0][i].state == player and
                squares[1][i].state == player and
                squares[2][i].state == player):
                return True
        
        # Check diagonals
        if (squares[0][0].state == player and
            squares[1][1].state == player and
            squares[2][2].state == player):
            return True
        
        if (squares[0][2].state == player and
            squares[1][1].state == player and
            squares[2][0].state == player):
            return True
        
        return False

    def would_win_game(self, player):
        # Check rows
        for i in range(3):
            if (self.mini_games[i][0].winner == player and
                self.mini_games[i][1].winner == player and
                self.mini_games[i][2].winner == player):
                return True
        
        # Check columns
        for i in range(3):
            if (self.mini_games[0][i].winner == player and
                self.mini_games[1][i].winner == player and
                self.mini_games[2][i].winner == player):
                return True
        
        # Check diagonals
        if (self.mini_games[0][0].winner == player and
            self.mini_games[1][1].winner == player and
            self.mini_games[2][2].winner == player):
            return True
        
        if (self.mini_games[0][2].winner == player and
            self.mini_games[1][1].winner == player and
            self.mini_games[2][0].winner == player):
            return True
        
        return False

    def update_mini_game_highlights(self):
        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                if self.active_mini_game == (r, c):  # highlight active mini-game
                    mini_game.setStyleSheet(f"border-color: {HIGHLIGHT}")
                    mini_game.set_overlay_colour(f"{HIGHLIGHT}")
                else:
                    mini_game.setStyleSheet(f"border-color: {GRID}")
                    mini_game.set_overlay_colour(GRID)

    def highlight_mini_game_hover(self, mini_game_row, mini_game_col, hovering):
        # Disable hover highlighting during AI turn
        if self.difficulty is not None and self.current_player == self.ai_player:
            return
            
        if self.active_mini_game is None:
            mini_game = self.mini_games[mini_game_row][mini_game_col]
            if hovering and mini_game.winner is None and not mini_game.is_full:  # highlight hover
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

                mini_game.refresh_hovers()

    def update_board_colour(self, colour):
        self.setStyleSheet(f"border-color: {colour};")

    def check_overall_winner(self):
        winner = None
        
        # Check rows and columns
        for i in range(3):
            if (self.mini_games[i][0].winner is not None and
                self.mini_games[i][0].winner == self.mini_games[i][1].winner == self.mini_games[i][2].winner):
                winner = self.mini_games[i][0].winner
                break
            if (self.mini_games[0][i].winner is not None and
                self.mini_games[0][i].winner == self.mini_games[1][i].winner == self.mini_games[2][i].winner):
                winner = self.mini_games[0][i].winner
                break

        # Check diagonals
        if winner is None:
            if (self.mini_games[0][0].winner is not None and
                self.mini_games[0][0].winner == self.mini_games[1][1].winner == self.mini_games[2][2].winner):
                winner = self.mini_games[0][0].winner
            elif (self.mini_games[0][2].winner is not None and
                self.mini_games[0][2].winner == self.mini_games[1][1].winner == self.mini_games[2][0].winner):
                winner = self.mini_games[0][2].winner

        # Check for draw
        if winner is None:
            if all(self.mini_games[r][c].winner is not None or self.mini_games[r][c].is_full
                   for r in range(3) for c in range(3)):
                winner = "Draw"

        if winner:
            self.game_over.emit()  # Emit signal to stop timer
            self.display_winner(winner)
            return True
        
        return False
    
    def display_winner(self, winner):
        # Disable all mini-games
        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                mini_game.playable = False
                mini_game.set_playable_squares()

        self.update_board_colour(winner == 'X' and RED or winner == 'O' and BLUE or GRID)

        # Calculate time taken (in seconds)
        if self.start_time is not None:
            self.time_taken = time.time() - self.start_time
        else:
            self.time_taken = 0

        time_bonus = max(0, self.time_cap - int(self.time_taken)) 

        if winner == "X":
            if self.difficulty == "Hard":
                self.score = 1000 + time_bonus
            elif self.difficulty == "Medium":
                self.score = 600 + time_bonus
            else:
                self.score = 300 + time_bonus

        # Show modern pop-up
        dialog = GameResultDialog(winner, self.score, parent=self, username=self.username)
        dialog.exec()

    def reset_game(self):
        self.current_player = "X"
        self.active_mini_game = None
        self.start_time = None  # Reset timer
        self.time_taken = 0
        self.score = 0

        for r in range(3):
            for c in range(3):
                mini_game = self.mini_games[r][c]
                # Ensure winner overlay is properly destroyed
                if mini_game.winner_overlay:
                    mini_game.winner_overlay.deleteLater()
                    mini_game.winner_overlay = None
                mini_game.reset()

        self.update_board_colour(RED)
        self.update_mini_game_highlights()
        self.update_playable_mini_games()
        
        # Emit signal to restart timer
        self.turn_changed.emit()
                
    def sizeHint(self):
        return QSize(600, 600)