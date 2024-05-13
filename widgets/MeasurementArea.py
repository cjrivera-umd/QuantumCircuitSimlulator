from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QLabel, QSpacerItem, QSizePolicy, QFrame
from PyQt6.QtCore import Qt

from widgets.MeasurementButton import MeasurementButton

class MeasurementArea(QScrollArea):

    def __init__(self, wire_count):
        super().__init__()

        self.wire_count = wire_count
        self.measure_buttons = [MeasurementButton(i) for i in range(self.wire_count)]

        self.initUI()


    def initUI(self):
        self.setFixedWidth(80)
        self.setFrameShape(QFrame.Shape.NoFrame)

        self.widget = QWidget()
        self.grid = QGridLayout()
        self.grid.setVerticalSpacing(50)

        for i, button in enumerate(self.measure_buttons):
            button.setEnabled(False)
            self.grid.addWidget(button, i, 0, Qt.AlignmentFlag.AlignHCenter)
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

        # Add measurment button to last row
        new_button = MeasurementButton(self.wire_count)
        new_button.setEnabled(False)
        self.grid.addWidget(new_button, self.wire_count, 0, Qt.AlignmentFlag.AlignHCenter)
        self.measure_buttons.append(new_button)
        self.wire_count += 1

        # Place vertical spacer in the new last row
        self.grid.addItem(self.vspacer, self.wire_count, 0, 1, -1)

        # Reset scrollbar to the bottom
        # self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


    def deleteWire(self):
        # Remove vertical spacer in last row
        self.grid.removeItem(self.vspacer)

        # Remove measurement button in last row
        self.grid.removeWidget(self.measure_buttons[-1])
        self.measure_buttons = self.measure_buttons[:-1]
        self.wire_count -= 1

        # Place vertical spacer in the new last row
        self.grid.addItem(self.vspacer, self.wire_count, 0, 1, -1)


    def setMeasurements(self, possible_post_measurement_states):
        # Calculating probability of 0 or 1 for each qubit
        for qubit_i, button in enumerate(self.measure_buttons):
            prob_0, prob_1 = 0, 0
            for (post_measurement_state, prob) in possible_post_measurement_states:
                if post_measurement_state[qubit_i] == '0':
                    prob_0 += prob
                else:   # post_measurement_state[qubit_i] == '1'
                    prob_1 += prob
            button.prob_0 = prob_0
            button.prob_1 = prob_1
            button.setEnabled(True)

            print(f'For qubit {qubit_i}: Pr[0] = {format(button.prob_0, ".2%")}, Pr[1] = {format(button.prob_1, ".2%")}')