from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from styling.colours import GRID

class GridOverlay(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        self.grid_colour = GRID

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        pen = QPen(QColor(self.grid_colour))
        pen.setWidth(4)
        painter.setPen(pen)

        w, h = self.width(), self.height()

        # exact floating division
        xs = [round(w * i / 3) for i in range(1, 3)]
        ys = [round(h * i / 3) for i in range(1, 3)]

        for x in xs:
            painter.drawLine(x, 0, x, h)

        for y in ys:
            painter.drawLine(0, y, w, y)

    def set_colour(self, colour):
        self.grid_colour = colour
        self.update()
