from math import log2

from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt

from models.Matrix import Matrix

class OutputSection(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        # Sizing
        self.setFixedWidth(250)
        self.setMinimumHeight(300)

        # Setting up label
        section_label = QLabel('Output Probabilities')
        label_box = QHBoxLayout()
        label_box.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        label_box.addWidget(section_label)
        label_box.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Setting up output table and scroll widgets
        self.output_table = QTableWidget()
        self.output_table.setRowCount(0)
        self.output_table.setColumnCount(2)
        self.output_table.verticalHeader().setVisible(False)
        self.output_table.setHorizontalHeaderLabels(['Amplitude', 'Probability'])
        self.output_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        # self.output_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.output_table.horizontalHeader().setStretchLastSection(True)
        # self.output_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # This doesn't allow for chaning horizontal sizes

        output_scroll = QScrollArea()
        output_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        output_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        output_scroll.setWidgetResizable(True)
        output_scroll.setWidget(self.output_table)

        # Setting up section layout
        section_box = QVBoxLayout()
        section_box.setSpacing(5)
        section_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        section_box.addLayout(label_box)
        section_box.addWidget(self.output_table)

        self.setLayout(section_box)


    def measureCircuit(self, state):
        # Initializing list of possible outcomes
        possible_post_measurement_states = []

        # Calculating percentage for each possible measurement
        l = len(state)
        input_bits = int(log2(l))
        measurement_states = [([[0]] * (i)) + [[1]] + ([[0]] * (l - i - 1)) for i in range(l)]
        for measurement_state in measurement_states:
            matrix = Matrix(measurement_state)
            proj_op = matrix * matrix.T()
            # print('Projection operator:')
            # print(proj_op)
            # print()

            projection = proj_op * state
            # print('Projection:')
            # print(projection)

            magnitude = projection.norm()
            if magnitude:
                possible_post_measurement_states.append((projection.toBitstring(input_bits), magnitude))

        # Clearing table
        self.output_table.setRowCount(0)

        # Inserting new measurements
        self.output_table.setRowCount(len(possible_post_measurement_states))
        for i, (bitstring, prob) in enumerate(possible_post_measurement_states):
            # print(bitstring, prob)
            self.output_table.setItem(i, 0, QTableWidgetItem(bitstring))
            self.output_table.setItem(i, 1, QTableWidgetItem(format(prob, '.2%')))

        # Sending measurements to measure area
        self.setMeasurements(possible_post_measurement_states)
