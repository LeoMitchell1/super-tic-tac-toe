from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, pyqtSignal
from styling.colours import RED, BLUE, BACKGROUND, HOVER

class BoardSquare(QPushButton):
    hovered = pyqtSignal(bool)

    def __init__(self, row, col, parent=None):
        super().__init__(parent) # Initialize as a QPushButton
        self.state = None
        self.row = row
        self.col = col
        self.playable = False
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setProperty('cell', 'true')
        self.setMouseTracking(True)
        self.setStyleSheet("""
            QPushButton:hover {
                /* remove default hover effect */
            }
        """)

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
        if self.state == 'X':
            self.setStyleSheet(f"background-color: {RED}")  # red for X
        elif self.state == 'O':
            self.setStyleSheet(f"background-color: {BLUE}")  # blue for O
        else:
            self.setStyleSheet(f"background-color: {BACKGROUND}")  # default

    def enterEvent(self, event):
        if self.playable and self.state is None:  # only hover if square is playable
            self.setStyleSheet(f"background-color: {HOVER}")
            self.hovered.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.playable:
            self.update_background()  # revert to original background
            self.hovered.emit(False)
        super().leaveEvent(event)