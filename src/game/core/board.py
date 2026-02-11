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
        self.time_cap = 120  # 2 minutes time cap for scoring
        
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
            QTimer.singleShot(200, self.ai_make_move)  # 10ms delay for better UX

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
            if self._leads_to_overall_win(move, self.ai_player):
                return move
        
        # 2. Block human from winning the overall game
        for move in moves:
            if self._leads_to_overall_win(move, self.human_player):
                return move
        
        # 3. Win any mini-game to build position
        for move in moves:
            if self._wins_mini_game(move, self.ai_player):
                return move
        
        # 4. Block human from winning any mini-game
        for move in moves:
            if self._wins_mini_game(move, self.human_player):
                return move
        
        # 5. Create two-in-a-row on main board (threatening position)
        for move in moves:
            if self._creates_two_in_row_main(move, self.ai_player):
                return move
        
        # 6. Block human's two-in-a-row on main board
        for move in moves:
            if self._creates_two_in_row_main(move, self.human_player):
                return move
        
        # 7. AVOID sending opponent to won/full boards (gives them freedom)
        constrained_moves = [m for m in moves if not self._sends_to_won_or_full_board(m)]
        if constrained_moves:
            moves = constrained_moves
        
        # 8. Prefer center positions (stronger strategic value)
        center_moves = [m for m in moves if self._is_center_position(m)]
        if center_moves:
            return random.choice(center_moves)
        
        # 9. Fall back to random from remaining moves
        return random.choice(moves)

    def _leads_to_overall_win(self, move, player):
        """Check if move wins the overall game"""
        mg_row, mg_col, sq_row, sq_col = move
        mini_game = self.mini_games[mg_row][mg_col]
        
        original_state = mini_game.squares[sq_row][sq_col].state
        original_winner = mini_game.winner
        
        mini_game.squares[sq_row][sq_col].state = player
        
        if self.check_mini_game_win(mini_game, player):
            mini_game.winner = player
            wins = self.would_win_game(player)
            mini_game.winner = original_winner
        else:
            wins = False
        
        mini_game.squares[sq_row][sq_col].state = original_state
        return wins

    def _wins_mini_game(self, move, player):
        """Check if move wins a mini-game"""
        mg_row, mg_col, sq_row, sq_col = move
        mini_game = self.mini_games[mg_row][mg_col]
        
        original = mini_game.squares[sq_row][sq_col].state
        mini_game.squares[sq_row][sq_col].state = player
        wins = self.check_mini_game_win(mini_game, player)
        mini_game.squares[sq_row][sq_col].state = original
        
        return wins

    def _creates_two_in_row_main(self, move, player):
        """Check if winning this mini-game creates two-in-a-row on main board"""
        if not self._wins_mini_game(move, player):
            return False
        
        mg_row, mg_col = move[0], move[1]
        
        # Check if this creates 2-in-a-row on main board
        # Check row
        row_count = sum(1 for c in range(3) if self.mini_games[mg_row][c].winner == player)
        if row_count == 1:  # Would become 2
            return True
        
        # Check column
        col_count = sum(1 for r in range(3) if self.mini_games[r][mg_col].winner == player)
        if col_count == 1:  # Would become 2
            return True
        
        # Check diagonals
        if mg_row == mg_col:  # Main diagonal
            diag_count = sum(1 for i in range(3) if self.mini_games[i][i].winner == player)
            if diag_count == 1:
                return True
        
        if mg_row + mg_col == 2:  # Anti-diagonal
            anti_diag_count = sum(1 for i in range(3) if self.mini_games[i][2-i].winner == player)
            if anti_diag_count == 1:
                return True
        
        return False

    def _is_center_position(self, move):
        """Check if move is in a strategic center position"""
        mg_row, mg_col, sq_row, sq_col = move
        
        # Prefer center mini-board
        if mg_row == 1 and mg_col == 1:
            return True
        
        # Prefer center square in any mini-board
        if sq_row == 1 and sq_col == 1:
            return True
        
        return False

    def _sends_to_won_or_full_board(self, move):
        """Check if move sends opponent to a won or full board (BAD - gives them freedom!)"""
        sq_row, sq_col = move[2], move[3]
        next_board = self.mini_games[sq_row][sq_col]
        
        # Return True if sending to won/full board (this is BAD for us)
        return next_board.winner is not None or next_board.is_full
    
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
                self.score = 900 + time_bonus
            elif self.difficulty == "Medium":
                self.score = 700 + time_bonus
            else:
                self.score = 500 + time_bonus

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