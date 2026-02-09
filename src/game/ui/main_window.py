from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer
from ..core.board import Board

class MainWindow(QMainWindow):
    def __init__(self, mode, difficulty, username=None):
        super().__init__()
        self.username = username        
        self.mode = mode
        self.difficulty = difficulty
        self.setWindowTitle("Super Tic Tac Toe")
        self.setFixedSize(700, 800)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Timer setup (only for Player vs AI mode)
        if self.mode == "Player vs AI":
            timer_container = QFrame()
            timer_container.setObjectName("timerContainer")
            timer_container.setFixedHeight(110)
            timer_layout = QVBoxLayout(timer_container)
            timer_layout.setContentsMargins(0, 0, 0, 0)
            timer_layout.setSpacing(5)
            
            self.timer_label = QLabel("3")
            self.timer_label.setObjectName("timerLabel")
            self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.timer_subtitle = QLabel("Player X's Turn")
            self.timer_subtitle.setObjectName("timerSubtitle")
            self.timer_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            timer_layout.addWidget(self.timer_label)
            timer_layout.addWidget(self.timer_subtitle)
            
            layout.addWidget(timer_container, alignment=Qt.AlignmentFlag.AlignCenter)
            
            self.countdown_timer = QTimer()
            self.countdown_timer.timeout.connect(self.update_timer)
            self.time_remaining = 3
        
        self.board = Board(
            difficulty=self.difficulty if self.mode == "Player vs AI" else None,
            username=username
        )
        self.board.turn_changed.connect(self.on_turn_changed)
        self.board.game_over.connect(self.stop_timer)

        # Wrap board in container to add bottom padding
        board_container = QWidget()
        board_layout = QVBoxLayout(board_container)
        board_layout.setContentsMargins(0, 0, 0, 90)  # 40px bottom padding moves board up
        board_layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(board_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        controls = QHBoxLayout()
        controls.setSpacing(100)
        restart = QPushButton("Restart")
        restart.setObjectName("restartButton")
        restart.clicked.connect(self.restart_game)
        back_btn = QPushButton("Back")
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.back)
        controls.addStretch()
        controls.addWidget(restart)
        controls.addWidget(back_btn)
        controls.addStretch()
        layout.addLayout(controls)
        
        self.start_countdown()
    
    def start_countdown(self):
        if not hasattr(self, 'countdown_timer'):
            return
        if self.difficulty is not None and self.board.current_player == self.board.ai_player:
            self.countdown_timer.stop()
            self.timer_label.setText("AI")
            self.update_timer_color()
            return
        self.time_remaining = 3
        self.timer_label.setText("3")
        self.update_timer_color()
        self.countdown_timer.start(1000)
    
    def update_timer(self):
        self.time_remaining -= 1
        self.timer_label.setText(str(self.time_remaining))
        self.update_timer_color()
        if self.time_remaining <= 0:
            self.countdown_timer.stop()
            self.skip_turn()
    
    def update_timer_color(self):
        if self.difficulty is not None and self.board.current_player == self.board.ai_player:
            self.timer_label.setProperty("state", "ai")
            self.timer_subtitle.setProperty("state", "ai")
        elif self.board.current_player == "X":
            self.timer_label.setProperty("state", "x")
            self.timer_subtitle.setProperty("state", "x")
        else:
            self.timer_label.setProperty("state", "o")
            self.timer_subtitle.setProperty("state", "o")
        self.timer_label.style().unpolish(self.timer_label)
        self.timer_label.style().polish(self.timer_label)
        self.timer_subtitle.style().unpolish(self.timer_subtitle)
        self.timer_subtitle.style().polish(self.timer_subtitle)
    
    def skip_turn(self):
        self.board.current_player = "O" if self.board.current_player == "X" else "X"
        from styling.colours import RED, BLUE
        if self.board.current_player == "X":
            self.board.update_board_colour(RED)
        else:
            self.board.update_board_colour(BLUE)
        if self.board.current_player == "X":
            self.timer_subtitle.setText("Player X's Turn")
        else:
            self.timer_subtitle.setText("Player O's Turn")
        self.start_countdown()
        if self.difficulty is not None and self.board.current_player == self.board.ai_player:
            QTimer.singleShot(350, self.board.ai_make_move)
    
    def on_turn_changed(self):
        if not hasattr(self, 'timer_subtitle'):
            return
        if self.board.current_player == "X":
            self.timer_subtitle.setText("Player X's Turn")
        else:
            self.timer_subtitle.setText("Player O's Turn")
        self.start_countdown()
    
    def stop_timer(self):
        if not hasattr(self, 'countdown_timer'):
            return
        self.countdown_timer.stop()
        self.timer_label.setText("—")
        self.timer_subtitle.setText("Game Over")
        self.timer_label.setProperty("state", "ai")
        self.timer_subtitle.setProperty("state", "ai")
        self.timer_label.style().unpolish(self.timer_label)
        self.timer_label.style().polish(self.timer_label)
        self.timer_subtitle.style().unpolish(self.timer_subtitle)
        self.timer_subtitle.style().polish(self.timer_subtitle)
    
    def restart_game(self):
        self.countdown_timer.stop()
        self.board.reset_game()
        self.timer_subtitle.setText("Player X's Turn")
        self.start_countdown()
    
    def back(self):
        if hasattr(self, 'countdown_timer'):
            self.countdown_timer.stop()
        from .menu_window import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()