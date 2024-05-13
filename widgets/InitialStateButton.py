from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPalette, QColor

from models.InitialState import InitialState

class InitialStateButton(QPushButton):

    STATE_CYCLE = [InitialState.ZERO, InitialState.ONE, InitialState.PLUS, InitialState.MINUS]

    def __init__(self, state):
        super().__init__(f'|{state.value["repr"]}⟩')

        self.state = state
        
        self.clicked.connect(self.cycleState)

        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('gray'))
        self.setPalette(palette)

        self.setFixedSize(50, 50)

    def cycleState(self):
        curr_state_idx = self.STATE_CYCLE.index(self.state)
        next_state_idx = (curr_state_idx + 1) % 4
        self.state = self.STATE_CYCLE[next_state_idx]
        self.setText(f'|{self.state.value["repr"]}⟩')

    def getVector(self):
        return self.state.value['vector']