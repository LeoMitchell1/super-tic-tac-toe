from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from .main_window import MainWindow
from .instructions_window import InstructionsWindow


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Tic Tac Toe")
        self.setFixedSize(450, 600)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title section with ComSSA's label
        title_section = QWidget()
        title_section.setFixedSize(340, 100)
        
        # Main title with colored text
        title = QLabel(title_section)
        title.setObjectName("menuTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setGeometry(0, 35, 340, 60)
        title.setText(
            '<span style="color: #ed4a4a; font-size: 32px;">Super</span> '
            '<span style="color: #2F2F2F; font-size: 32px;">Tic</span> '
            '<span style="color: #557ef9; font-size: 32px;">Tac</span> '
            '<span style="color: #2F2F2F; font-size: 32px;">Toe</span>'
        )
        
        layout.addWidget(title_section, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.mode_selector = QComboBox()
        self.mode_selector.setObjectName("menuComboBox")
        self.mode_selector.setFixedWidth(200)
        self.mode_selector.addItems(["Player vs Player", "Player vs AI"])
        layout.addWidget(self.mode_selector, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.difficulty_selector = QComboBox()
        self.difficulty_selector.setObjectName("menuComboBox")
        self.difficulty_selector.setFixedWidth(200)
        self.difficulty_selector.addItems(["Easy", "Medium", "Hard"])
        layout.addWidget(self.difficulty_selector, alignment=Qt.AlignmentFlag.AlignCenter)
        
        start_btn = QPushButton("Start Game")
        start_btn.setObjectName("menuButton")
        start_btn.setFixedWidth(200)
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        instructions_btn = QPushButton("Instructions")
        instructions_btn.setObjectName("instructionsButton")
        instructions_btn.setFixedWidth(200)
        instructions_btn.clicked.connect(self.show_instructions_window)
        layout.addWidget(instructions_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        quit_btn = QPushButton("Quit")
        quit_btn.setObjectName("quitButton")
        quit_btn.setFixedWidth(200)
        quit_btn.clicked.connect(self.close)
        layout.addWidget(quit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def start_game(self):
        mode = self.mode_selector.currentText()
        difficulty = self.difficulty_selector.currentText()
        self.main_window = MainWindow(mode=mode, difficulty=difficulty)
        self.main_window.show()
        self.close()
    
    def show_instructions_window(self):
        self.instructions_win = InstructionsWindow()
        self.instructions_win.show()
        self.close()