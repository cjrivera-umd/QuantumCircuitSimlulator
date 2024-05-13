from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QLabel, QSpacerItem, QSizePolicy, QFrame
from PyQt6.QtCore import Qt

from widgets.InitialStateButton import InitialStateButton
from models.InitialState import InitialState

class InitialStateArea(QScrollArea):

    def __init__(self, wire_count):
        super().__init__()

        self.wire_count = wire_count
        self.state_buttons = [(QLabel(f'{i}:'), InitialStateButton(InitialState.ZERO)) for i in range(self.wire_count)]

        self.initUI()


    def initUI(self):
        self.setFixedWidth(100)
        self.setFrameShape(QFrame.Shape.NoFrame)

        self.widget = QWidget()
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(50)

        for i, (label, button) in enumerate(self.state_buttons):
            self.grid.addWidget(label, i, 0, Qt.AlignmentFlag.AlignHCenter)
            self.grid.addWidget(button, i, 1, Qt.AlignmentFlag.AlignHCenter)
        self.vspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.grid.addItem(self.vspacer, self.wire_count, 0, 1, -1)

        self.widget.setLayout(self.grid)

        # Scroll Widget setup
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.widget)


    def addWire(self):
        # Remove vertical spacer in last row
        self.grid.removeItem(self.vspacer)

        # Add initial state button to last row
        new_state_label = QLabel(f'{self.wire_count}:')
        new_state_button = InitialStateButton(InitialState.ZERO)
        self.grid.addWidget(new_state_label, self.wire_count, 0, Qt.AlignmentFlag.AlignHCenter)
        self.grid.addWidget(new_state_button, self.wire_count, 1, Qt.AlignmentFlag.AlignHCenter)
        self.wire_count += 1
        self.state_buttons.append((new_state_label, new_state_button))

        # Place vertical spacer in the new last row
        self.grid.addItem(self.vspacer, self.wire_count, 0, 1, -1)

        # Reset scrollbar to the bottom
        # self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    
    def deleteWire(self):
        # Remove vertical spacer in last row
        self.grid.removeItem(self.vspacer)

        # Remove initial state button in last row
        last_label, last_button = self.state_buttons[-1]
        self.grid.removeWidget(last_label)
        self.grid.removeWidget(last_button)
        self.state_buttons = self.state_buttons[:-1]
        self.wire_count -= 1

        # Place vertical spacer in the new last row
        self.grid.addItem(self.vspacer, self.wire_count, 0, 1, -1)


    def getState(self):
        state = self.state_buttons[0][1].getVector()
        for _, button in self.state_buttons[1:]:
            state = state ** button.getVector()

        return state


