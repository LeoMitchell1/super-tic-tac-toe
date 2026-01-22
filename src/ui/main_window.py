from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QFrame,
    QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt


def create_main_window():
    window = QMainWindow()
    window.setWindowTitle("Super Tic Tac Toe")
    window.setFixedSize(700, 750)

    central_widget = QWidget()
    window.setCentralWidget(central_widget)

    main_layout = QVBoxLayout(central_widget)
    main_layout.setSpacing(20)
    main_layout.setContentsMargins(20, 20, 20, 20)

    # ──────────────────────────────
    # BOARD OUTER BORDER
    # ──────────────────────────────
    board_frame = QFrame()
    board_frame.setObjectName("boardFrame")
    board_frame.setFrameShape(QFrame.Shape.Box)
    board_frame.setFixedSize(620, 620)

    board_layout = QGridLayout(board_frame)
    board_layout.setSpacing(10)
    board_layout.setContentsMargins(10, 10, 10, 10)

    # ──────────────────────────────
    # 3×3 BIG FRAMES
    # ──────────────────────────────
    for row in range(3):
        for col in range(3):
            inner_frame = QFrame()
            inner_frame.setFixedSize(180, 180)

            frame_layout = QGridLayout(inner_frame)
            frame_layout.setSpacing(0)
            frame_layout.setContentsMargins(0, 0, 0, 0)

            # 3×3 BUTTONS
            for r in range(3):
                for c in range(3):
                    btn = QPushButton()
                    btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    btn.setProperty("cell", True)  # all grid buttons
                    # mark outer corners
                    if r == 0 and c == 0:
                        btn.setProperty("corner", "top-left")
                    elif r == 0 and c == 2:
                        btn.setProperty("corner", "top-right")
                    elif r == 2 and c == 0:
                        btn.setProperty("corner", "bottom-left")
                    elif r == 2 and c == 2:
                        btn.setProperty("corner", "bottom-right")
                    elif r == 1 and c == 1:
                        btn.setProperty("corner", "center")
                    else:
                        btn.setProperty("corner", "none")  # middle buttons or edges
                    frame_layout.addWidget(btn, r, c)

            board_layout.addWidget(inner_frame, row, col)

    main_layout.addWidget(board_frame, alignment=Qt.AlignmentFlag.AlignCenter)

    # ──────────────────────────────
    # CONTROL BUTTONS
    # ──────────────────────────────
    controls_layout = QHBoxLayout()
    controls_layout.setSpacing(100)

    restart_button = QPushButton("Restart")
    restart_button.setObjectName("restartButton")
    restart_button.setFixedSize(100, 35)

    quit_button = QPushButton("Quit")
    quit_button.setObjectName("quitButton")
    quit_button.setFixedSize(100, 35)

    controls_layout.addStretch()
    controls_layout.addWidget(restart_button)
    controls_layout.addWidget(quit_button)
    controls_layout.addStretch()

    main_layout.addLayout(controls_layout)

    return window
