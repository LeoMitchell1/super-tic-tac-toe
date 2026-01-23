from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, pyqtSignal

class BoardSquare(QPushButton):
    hovered = pyqtSignal(bool)

    def __init__(self, row, col, parent=None):
        super().__init__(parent) # Initialize as a QPushButton
        
        self.state = None  # Can be 'X', 'O', or None
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setProperty('cell', 'true')
        self.row = row
        self.col = col

        self.setMouseTracking(True)  # Enable mouse tracking for hover events

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.state is None:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        rect = self.contentsRect()
        size = min(rect.width(), rect.height())

        # Scale pen with size
        pen_width = max(2, size // 10)
        pen = QPen(QColor("#ffffff"), pen_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        margin = size * 0.25
        cx = rect.center().x()
        cy = rect.center().y()

        if self.state == "X":
            offset = size / 2 - margin
            painter.drawLine(
                int(cx - offset), int(cy - offset),
                int(cx + offset), int(cy + offset)
            )
            painter.drawLine(
                int(cx + offset), int(cy - offset),
                int(cx - offset), int(cy + offset)
            )

        elif self.state == "O":
            radius = size / 2 - margin
            painter.drawEllipse(
                int(cx - radius), int(cy - radius),
                int(radius * 2), int(radius * 2)
            )


    def set_state(self, state):
        if state in ('X', 'O', None):
            self.state = state
            self.update_background()  # update background immediately
            self.update()  # trigger repaint

    def update_background(self):
        """Set the button's background color depending on its state."""
        if self.state == 'X':
            self.setStyleSheet("background-color: #ff4d4d")  # red for X
        elif self.state == 'O':
            self.setStyleSheet("background-color: #4d79ff")  # blue for O
        else:
            self.setStyleSheet("background-color: #ffffff")  # default white

    def enterEvent(self, event):
        self.hovered.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered.emit(False)
        super().leaveEvent(event)