from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt

class InstructionsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("How to Play")
        self.setFixedSize(520, 700)
        
        # Modern scroll area with custom styling
        scroll = QScrollArea()
        scroll.setObjectName("modernScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(scroll)
        
        container = QWidget()
        container.setObjectName("scrollContent")
        scroll.setWidget(container)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)
        
        # ---------- Title ----------
        title = QLabel("How to Play")
        title.setObjectName("menuTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)


        # Main title with colored text
        subtitle = QLabel("Title")
        subtitle.setObjectName("menuTitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setText(
            '<span style="color: #ed4a4a; font-size: 25px;">Super</span> '
            '<span style="color: #2F2F2F; font-size: 25px;">Tic</span> '
            '<span style="color: #557ef9; font-size: 25px;">Tac</span> '
            '<span style="color: #2F2F2F; font-size: 25px;">Toe</span>'
        )
        layout.addWidget(subtitle)
        
        # ---------- Step sections ----------
        layout.addWidget(self.step_card(
            "Step 1 — Choose Your Mode",
            "Select Player vs Player or Player vs Computer.\n"
            "If playing against the AI, choose a difficulty level.",
            image_label="(Menu screenshot here)"
        ))
        
        layout.addWidget(self.step_card(
            "Step 2 — Play Your Turn",
            "Click on a square to place your mark.\n"
            "Your move determines which mini-board your opponent must play next.",
            image_label="(Board interaction screenshot)"
        ))
        
        layout.addWidget(self.step_card(
            "Step 3 — Win Mini Boards",
            "Get three in a row inside a mini-board to claim it.\n"
            "Claimed boards count toward the final victory.",
            image_label="(Mini-board win example)"
        ))
        
        layout.addWidget(self.step_card(
            "Step 4 — Win the Game",
            "Win three mini-boards in a row (horizontally, vertically, or diagonally) to win the game!",
            image_label="(Overall win example)"
        ))
        
        # ---------- Back button ----------
        back_btn = QPushButton("Back to Menu")
        back_btn.setObjectName("instructionsBackButton")
        back_btn.clicked.connect(self.back_to_menu)
        back_btn.setFixedHeight(40)
        back_btn.setFixedWidth(200)
        layout.addSpacing(10)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add stretch at the end for better spacing
        layout.addStretch()
    
    # ---------- Helper for step cards ----------
    def step_card(self, title_text, body_text, image_label=""):
        card = QFrame()
        card.setObjectName("instructionCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel(title_text)
        title.setObjectName("instructionCardTitle")
        card_layout.addWidget(title)
        
        body = QLabel(body_text)
        body.setObjectName("instructionCardBody")
        body.setWordWrap(True)
        card_layout.addWidget(body)
        
        # Image placeholder
        image = QLabel(image_label)
        image.setObjectName("instructionImagePlaceholder")
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setFixedHeight(120)
        card_layout.addWidget(image)
        
        return card
    
    def back_to_menu(self):
        from .menu_window import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()