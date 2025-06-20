import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QPen, QFont, QColor


class Speedometer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.min_value = 0
        self.max_value = 140
        self._value = 0
        # **Allow this widget to receive focus and key events**
        self.setFocusPolicy(Qt.StrongFocus)

    def setValue(self, value):
        self._value = max(self.min_value, min(self.max_value, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fill background
        painter.fillRect(self.rect(), QColor(20, 20, 20))

        w, h = self.width(), self.height()
        radius = min(w, h) * 0.4
        center = QPointF(w / 2, h / 2)

        # Draw outer circle
        pen = QPen(QColor(200, 200, 200))
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawEllipse(center, radius, radius)

        # Draw ticks and labels
        tick_pen = QPen(QColor(200, 200, 200))
        tick_pen.setWidth(2)
        painter.setPen(tick_pen)

        label_font = QFont('Arial', int(radius * 0.10), QFont.Bold)
        painter.setFont(label_font)

        for i in range(self.min_value, self.max_value + 1, 10):
            angle_deg = 225 - (i / self.max_value) * 270
            angle = math.radians(angle_deg)
            sin_a, cos_a = math.sin(angle), math.cos(angle)
            outer = QPointF(
                center.x() + cos_a * radius,
                center.y() - sin_a * radius
            )
            inner = QPointF(
                center.x() + cos_a * (radius - (15 if i % 20 == 0 else 10)),
                center.y() - sin_a * (radius - (15 if i % 20 == 0 else 10))
            )
            painter.drawLine(inner, outer)

            if i % 20 == 0:
                # Position for label
                label_pt = QPointF(
                    center.x() + cos_a * (radius - 35),
                    center.y() - sin_a * (radius - 35)
                )
                text = str(i)
                # Measure text rectangle
                metrics = painter.fontMetrics()
                tw = metrics.horizontalAdvance(text)
                th = metrics.height()

                # Draw a filled circle behind each label
                bg_radius = max(tw, th) * 0.6
                painter.setBrush(QColor(20, 20, 20))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(label_pt, bg_radius, bg_radius)

                # Draw the number on top
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(
                    QRectF(label_pt.x() - tw/2, label_pt.y() - th/2, tw, th),
                    Qt.AlignCenter,
                    text
                )

        # Draw needle
        needle_angle = math.radians(225 - (self._value / self.max_value) * 270)
        needle_len = radius - 50
        needle = QPointF(
            center.x() + math.cos(needle_angle) * needle_len,
            center.y() - math.sin(needle_angle) * needle_len
        )
        needle_pen = QPen(QColor(255, 0, 0))
        needle_pen.setWidth(6)
        painter.setPen(needle_pen)
        painter.drawLine(center, needle)

        # Center cap
        painter.setBrush(QColor(200, 200, 200))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, 8, 8)

        # Digital readout
        painter.setPen(Qt.white)
        painter.setFont(QFont('Arial', int(radius * 0.15), QFont.Bold))
        painter.drawText(
            QRectF(center.x() - radius * 0.5, center.y() + radius * 0.2,
                   radius, radius * 0.3),
            Qt.AlignCenter,
            f"{self._value} mph"
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.setValue(self._value + 5)
        elif event.key() == Qt.Key_Down:
            self.setValue(self._value - 5)
        else:
            super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gauge = Speedometer(self)
        self.setCentralWidget(self.gauge)
        self.showFullScreen()
        self.setWindowTitle("MPH Speedometer")

    def keyPressEvent(self, event):
        # ESC to exit
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
