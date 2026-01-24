from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from styling.colours import RED, BLUE

class WinnerOverlay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        self.raise_()
        self.state = parent.winner  # 'X' or 'O' or None
        if self.state == 'X':
            self.overlay_colour = RED  # Red for X
        elif self.state == 'O':
            self.overlay_colour = BLUE  # Blue for O
        else:
            self.overlay_colour = "transparent"

        self.setStyleSheet(f"background-color: {self.overlay_colour};")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        rect = self.contentsRect()
        size = min(rect.width(), rect.height())

        # Scale pen with size
        pen_width = max(2, size // 10)
        pen = QPen(Qt.GlobalColor.white, pen_width)
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

        else:
            # No winner, do not draw anything
            return
        
    def hide(self):
        self.state = None
        self.setStyleSheet("background-color: transparent;")
        self.update()
