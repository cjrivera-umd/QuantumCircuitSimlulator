from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QSpacerItem

from widgets.CircuitArea import CircuitArea

class CircuitSection(QWidget):

    def __init__(self, initial_wire_count, initial_depth, measurement_func):
        super().__init__()

        self.measurement_func = measurement_func
        self.gate_selected = False

        self.initUI(initial_wire_count, initial_depth)


    def initUI(self, intial_wire_count, initial_depth):
        # Sizing
        self.setMinimumSize(600, 400)

        # Creating circuit
        self.circuit_area = CircuitArea(intial_wire_count, initial_depth, self.toggleGateActions)

        # Circuit buttons
        run_circuit_button = QPushButton('► Run Circuit')
        run_circuit_button.clicked.connect(self.runCircuit)
        self.delete_gate_button = QPushButton('Delete Gate')
        self.delete_gate_button.clicked.connect(self.deleteGate)
        self.lshift_gate_button = QPushButton('<')
        self.lshift_gate_button.clicked.connect(self.lshiftGate)
        self.rshift_gate_button = QPushButton('>')
        self.rshift_gate_button.clicked.connect(self.rshiftGate)
        add_wire_button = QPushButton('+ Wire')
        add_wire_button.clicked.connect(self.circuit_area.addWire)
        del_wire_button = QPushButton('– Wire')
        del_wire_button.clicked.connect(self.circuit_area.deleteWire)

        # Highlight move buttons
        self.lshift_gate_button.setEnabled(False)
        self.delete_gate_button.setEnabled(False)
        self.rshift_gate_button.setEnabled(False)

        # Buttons layout
        buttons_box = QHBoxLayout()
        buttons_box.addWidget(run_circuit_button)
        buttons_box.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        buttons_box.addWidget(self.lshift_gate_button)
        buttons_box.addWidget(self.delete_gate_button)
        buttons_box.addWidget(self.rshift_gate_button)
        buttons_box.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        buttons_box.addWidget(add_wire_button)
        buttons_box.addWidget(del_wire_button)

        # Preparing circuit section
        section_box = QVBoxLayout()
        section_box.setSpacing(5)
        section_box.addLayout(buttons_box)
        section_box.addWidget(self.circuit_area)
        self.setLayout(section_box)


    def runCircuit(self):
        initial_state = self.circuit_area.getInitialState()
        # print('Initial State:')
        # print(initial_state)

        circuit_matrix = self.circuit_area.getCircuitMatrix()
        # print('Circuit Matrix:')
        # print(circuit_matrix)

        final_state = circuit_matrix * initial_state if circuit_matrix else initial_state
        # print('Final state:')
        # print(final_state)

        self.measurement_func(final_state)


    def toggleGateActions(self):
        self.gate_selected = not self.gate_selected
        self.lshift_gate_button.setEnabled(self.gate_selected)
        self.delete_gate_button.setEnabled(self.gate_selected)
        self.rshift_gate_button.setEnabled(self.gate_selected)


    def deleteGate(self):
        self.circuit_area.gate_place_area.deleteGate()


    def lshiftGate(self):
        self.circuit_area.gate_place_area.lshiftGate()


    def rshiftGate(self):
        self.circuit_area.gate_place_area.rshiftGate()


    def placeGate(self, gate, wire):
        self.circuit_area.placeGate(gate, wire)