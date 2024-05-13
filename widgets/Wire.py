from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QPalette, QColor

class Wire(QWidget):

    def __init__(self):
        super().__init__()

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('black'))
        self.setPalette(palette)

        self.setFixedHeight(5)
        self.setMinimumWidth(150)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
