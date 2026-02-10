from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QInputDialog, QMessageBox, QSizePolicy, QSpacerItem, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .main_window import MainWindow
from .instructions_window import InstructionsWindow
from game.data.database import get_usernames, clear_leaderboard


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Tic Tac Toe")
        self.showFullScreen()  # opens full screen automatically

        # Initialize placeholders
        self.title_label = None
        self.scalable_widgets = []

        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)  # top/bottom margin
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Top spacer for vertical centering
        layout.addSpacerItem(QSpacerItem(0, 70, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Title section
        self.title_section = QWidget()
        title_layout = QVBoxLayout(self.title_section)
        title_layout.setContentsMargins(0, 0, 0, 0)  # top padding
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel()
        self.title_label.setObjectName("menuTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        title_layout.addWidget(self.title_label)
        layout.addWidget(self.title_section, alignment=Qt.AlignmentFlag.AlignCenter)

        # Combo boxes (do not set fixed width, allow expanding)
        self.mode_selector = QComboBox()
        self.mode_selector.setObjectName("menuComboBox")
        self.mode_selector.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.mode_selector.setMinimumWidth(360)  # base minimum width
        self.mode_selector.addItems(["Player vs AI", "Player vs Player"])
        layout.addWidget(self.mode_selector, alignment=Qt.AlignmentFlag.AlignCenter)

        self.difficulty_selector = QComboBox()
        self.difficulty_selector.setObjectName("menuComboBox")
        self.difficulty_selector.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.difficulty_selector.setMinimumWidth(360)
        self.difficulty_selector.addItems(["Easy (500+)", "Medium (1000+)", "Hard (1500+)"])
        layout.addWidget(self.difficulty_selector, alignment=Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.buttons = []
        base_button_width = 400  # uniform base width
        for btn_text, btn_func, btn_name in [
            ("Start Game", self.start_game, "menuButton"),
            ("Instructions", self.show_instructions_window, "instructionsButton"),
            ("Leaderboard", self.show_leaderboard_window, "leaderboardButton"),
            ("Quit", self.close, "quitButton"),
        ]:
            btn = QPushButton(btn_text)
            btn.setObjectName(btn_name)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.setMinimumWidth(base_button_width)
            btn.clicked.connect(btn_func)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
            self.buttons.append(btn)

        # Bottom spacer for vertical centering
        layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Widgets to scale dynamically
        self.scalable_widgets = self.buttons + [self.title_label, self.mode_selector, self.difficulty_selector]

        # Initial font update
        self.update_scaled_fonts()

    def resizeEvent(self, event):
        if getattr(self, "title_label", None) is not None:
            self.update_scaled_fonts()
        super().resizeEvent(event)

    def update_scaled_fonts(self):
        scale = self.height() / 600  # base design height

        # Title label
        base_size = int(32 * scale)
        self.title_label.setText(
            f'<span style="color: #ed4a4a; font-size: {base_size}px;">Super</span> '
            f'<span style="color: #2F2F2F; font-size: {base_size}px;">Tic</span> '
            f'<span style="color: #557ef9; font-size: {base_size}px;">Tac</span> '
            f'<span style="color: #2F2F2F; font-size: {base_size}px;">Toe</span>'
        )

        for widget in self.scalable_widgets:
            font = widget.font()
            font.setPointSizeF(100 * scale)
            widget.setFont(font)

            if isinstance(widget, QPushButton):
                widget.setMinimumHeight(int(50 * scale))
                widget.setMinimumWidth(int(200 * scale))  # keep buttons proportional
            # Do NOT change combo box width here; let layout handle it

    def start_game(self):
        mode = self.mode_selector.currentText()
        difficulty = self.difficulty_selector.currentText()
        if difficulty == "Easy (500+)":
            difficulty = "Easy"
        elif difficulty == "Medium (1000+)":
            difficulty = "Medium"
        else:
            difficulty = "Hard"

        username = None
        if mode == "Player vs AI":
            username = self._prompt_username_required()
            if username is None:
                return

        self.main_window = MainWindow(mode=mode, difficulty=difficulty, username=username)
        self.main_window.showFullScreen()  # open main window full screen
        self.close()

    def show_instructions_window(self):
        self.instructions_win = InstructionsWindow()
        self.instructions_win.showFullScreen()
        self.close()

    def show_leaderboard_window(self):
        from .leaderboard_window import LeaderboardWindow
        self.leaderboard_win = LeaderboardWindow()
        self.leaderboard_win.showFullScreen()
        self.close()

    def _prompt_username_required(self) -> str | None:
        existing_usernames = get_usernames()
        
        while True:
            # Create dialog instance
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Username Required")
            dialog.setLabelText("Enter your username (required for Player vs AI):")
            dialog.setStyleSheet("font-weight: bold; border: none;")
            dialog.setTextValue("")  # default empty
            dialog.setOkButtonText("OK")
            dialog.setCancelButtonText("Cancel")

            # Access the QLineEdit inside the dialog
            line_edit = dialog.findChild(QLineEdit)
            if line_edit:
                line_edit.setStyleSheet(
                    "QLineEdit {"
                    "   border: 3px solid gray;"
                    "   border-radius: 6px;"
                    "   padding: 4px;"
                    "   font-size: 14px;"
                    "}"
                )

            ok = dialog.exec()
            username = dialog.textValue().strip().lower()

            if not ok:
                return None

            existing_usernames = {u.lower() for u in get_usernames()}

            if not username:
                QMessageBox.warning(self, "Invalid Username", "Username cannot be empty.")
                continue

            if username in existing_usernames:
                QMessageBox.warning(self, "Username Taken", "That username is already taken. Please choose another.")
                continue

            return username