from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
from pathlib import Path

class InstructionsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("How to Play")
        self.setFixedSize(520, 700)
        
        # Get the images directory path
        # This gets the directory where this file is located, goes up one level, then into images
        self.images_dir = Path(__file__).parent.parent / "images"
        
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
            image_label="menu_image.png"
        ))
        
        layout.addWidget(self.step_card(
            "Step 2 — Play Your Turn",
            "Click on a square to place your mark.\n"
            "Your move determines which mini-board your opponent must play next. Be quick, you only have 3 seconds!",
            image_label="turn_image.png"
        ))
        
        layout.addWidget(self.step_card(
            "Step 3 — Win Mini Boards",
            "Get three in a row inside a mini-board to claim it.\n"
            "Claimed boards count toward the final victory.",
            image_label="mini_win_image.png"
        ))
        
        layout.addWidget(self.step_card(
            "Step 4 — Win the Game",
            "Win three mini-boards in a row (horizontally, vertically, or diagonally) to win the game! \n"
            "Note: Your score is based on the difficulty and how quickly you manage to win!",
            image_label="overall_win_image.png"
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
        image = QLabel()
        image.setObjectName("instructionImagePlaceholder")
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setScaledContents(False)  # Don't stretch the image
        image.setMaximumWidth(400)  # Set max width for the container
        
        # Try to load the image if it's an actual filename (not placeholder text)
        if image_label and not image_label.startswith("("):
            # Build the full path
            image_path = self.images_dir / image_label
            
            if image_path.exists():
                pixmap = QPixmap(str(image_path))
                if not pixmap.isNull():
                    # Scale the image to fit the max width while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(
                        400, 2000,  # Max width 400, large height limit
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    image.setPixmap(scaled_pixmap)
                else:
                    image.setText(f"[Could not load: {image_label}]")
                    image.setFixedHeight(60)
            else:
                image.setText(f"[Image not found: {image_label}]")
                image.setFixedHeight(60)
        else:
            # It's placeholder text
            image.setText(image_label if image_label else "[No image]")
            image.setFixedHeight(60)
        
        card_layout.addWidget(image, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the image container
        
        return card
    
    def back_to_menu(self):
        from .menu_window import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()