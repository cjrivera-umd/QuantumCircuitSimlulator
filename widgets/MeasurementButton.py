from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPalette, QColor

from widgets.QubitProbabilityDialog import QubitProbabilityDialog

class MeasurementButton(QPushButton):

    def __init__(self, wire):
        super().__init__('M')

        self.wire = wire
        self.prob_0 = 0
        self.prob_1 = 0

        self.clicked.connect(self.showProbabilities)

        self.initUI()


    def initUI(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('gray'))
        self.setPalette(palette)

        self.setFixedSize(50, 50)


    def showProbabilities(self):
        self.prob_dialog = QubitProbabilityDialog(self.wire, self.prob_0, self.prob_1)
        self.prob_dialog.exec()