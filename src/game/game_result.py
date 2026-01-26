from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt

class GameResultDialog(QDialog):
    def __init__(self, winner, parent=None):
        super().__init__(parent)
        colour = "#ed4a4a" if winner == "X" else "#557ef9" if winner == "O" else "#9E9E9E"
        
        # Frameless + translucent for rounded corners
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main layout of the dialog
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Container frame with rounded corners
        self.container = QFrame()
        self.container.setObjectName("gameResultContainer")
        self.container.setMinimumSize(200, 100)
        
        main_layout.addWidget(self.container)
        
        # Layout inside the container
        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.setSpacing(20)
        
        # Result label
        result_text = "It's a Draw!" if winner == "Draw" else f"{winner} Wins!"
        result_label = QLabel(result_text)
        result_label.setObjectName("gameResultLabel")
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(result_label)
        
        # Restart button
        restart_btn = QPushButton("Restart Game")
        restart_btn.setObjectName("gameResultButton")
        restart_btn.setStyleSheet(f"background-color: {colour}")
        restart_btn.clicked.connect(self.restart_game)
        container_layout.addWidget(restart_btn)
        
        self.parent_board = parent
        
        # Center the dialog relative to parent
        if parent:
            self.center_on_parent()
    
    def center_on_parent(self):
        """Center the dialog on the parent widget"""
        if self.parent_board:
            parent_geo = self.parent_board.window().geometry()
            dialog_geo = self.geometry()
            
            x = parent_geo.x() + (parent_geo.width() - dialog_geo.width()) // 2
            y = parent_geo.y() + (parent_geo.height() - dialog_geo.height()) // 2
            
            self.move(x, y)
    
    def showEvent(self, event):
        """Override showEvent to ensure centering after geometry is calculated"""
        super().showEvent(event)
        self.center_on_parent()
    
    def restart_game(self):
        self.accept()
        if self.parent_board:
            self.parent_board.reset_game()