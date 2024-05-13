from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPalette, QColor, QFont

class GateButton(QPushButton):

    def __init__(self, gate, wire=None, layer=None, invisible=False):
        super().__init__(gate.getButtonName())

        self.gate = gate
        self.wire = wire
        self.layer = layer
        self.invisible = invisible
        self.toggled = False

        self.initUI()


    def initUI(self):
        button_width, button_height = 60, 50 + (90 * (self.gate.input_size - 1))
        self.setFixedSize(button_width, button_height)

        self.toggled = False

        if self.invisible:
            sp_retain = self.sizePolicy()
            sp_retain.setRetainSizeWhenHidden(True)
            self.setSizePolicy(sp_retain)
            self.setEnabled(False)
            self.hide()
        else:
            self.setAutoFillBackground(True)
            self.palette = QPalette()


    def toggle(self):
        self.toggled = not self.toggled
        if self.toggled:
            self.palette.setColor(QPalette.ColorRole.ButtonText, QColor(50, 200, 90))
            self.setPalette(self.palette)
            self.setFont(QFont('.AppleSystemUIFont', 13, QFont.Weight.DemiBold))
        else:
            self.palette.setColor(QPalette.ColorRole.ButtonText, QColor('white'))
            self.setPalette(self.palette)
            self.setFont(QFont('.AppleSystemUIFont', 13))


    def deepcopy(self):
        return GateButton(self.gate, self.wire, self.layer, self.invisible)