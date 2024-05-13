from functools import partial, reduce

from PyQt6.QtWidgets import QWidget, QHBoxLayout

from widgets.InitialStateArea import InitialStateArea
from widgets.GatePlacementArea import GatePlacementArea
from widgets.MeasurementArea import MeasurementArea

from widgets.GateButton import GateButton

from models.Matrix import Matrix
from models.Gate import Gate

class CircuitArea(QWidget):

    def __init__(self, initial_wire_count, initial_depth, toggle_gate_actions):
        super().__init__()

        self.wire_count = initial_wire_count
        self.circuit_depth = initial_depth

        self.initUI(toggle_gate_actions)


    def initUI(self, toggle_gate_actions):
        self.setStyleSheet('''
        /* VERTICAL SCROLLBAR */
            QScrollBar:vertical {
                width: 0px;
            }
        ''')
        self.layout = QHBoxLayout()

        self.init_state_area = InitialStateArea(self.wire_count)
        self.gate_place_area = GatePlacementArea(self.wire_count, self.circuit_depth, toggle_gate_actions, self.addWire)
        self.measure_area = MeasurementArea(self.wire_count)

        self.init_state_area.verticalScrollBar().valueChanged.connect(partial(self.alignScrolls, 'init'))
        self.gate_place_area.verticalScrollBar().valueChanged.connect(partial(self.alignScrolls, 'gate'))
        self.measure_area.verticalScrollBar().valueChanged.connect(partial(self.alignScrolls, 'meas'))

        self.layout.addWidget(self.init_state_area)
        self.layout.addWidget(self.gate_place_area)
        self.layout.addWidget(self.measure_area)
        self.setLayout(self.layout)


    def alignScrolls(self, sender_key):
        receivers = { 'init': self.init_state_area, 'gate': self.gate_place_area, 'meas': self.measure_area }
        sender_vscroll = receivers[sender_key].verticalScrollBar()
        for receiver_key in [key for key in receivers.keys() if key != sender_key]:
            receiver_vscroll = receivers[receiver_key].verticalScrollBar()
            receiver_vscroll.setValue(sender_vscroll.value())


    def addWire(self):
        self.init_state_area.addWire()
        self.gate_place_area.addWire()
        self.measure_area.addWire()


    def deleteWire(self):
        if self.gate_place_area.wire_count > 1:
            self.init_state_area.deleteWire()
            self.gate_place_area.deleteWire()
            self.measure_area.deleteWire()


    def getInitialState(self):
        return self.init_state_area.getState()
    

    def getCircuitMatrix(self):
        all_layers = self.gate_place_area.buttons_per_layer
        
        # Extract useful layers
        populated_layers = list(filter(lambda layer: not all(elem is None for elem in layer), all_layers))

        # Extract * from layers
        cleaned_layers = list(map(lambda layer: list(filter(lambda elem: not elem or type(elem) == GateButton, layer)), populated_layers))
        
        # Fill empty spots with Identity matrices
        I_matrix = Matrix([[1, 0], [0, 1]])
        I_gate_button = GateButton(Gate(I_matrix, 'Identity', 'I'))
        for layer in cleaned_layers:
            for i, spot in enumerate(layer):
                if not spot:
                    layer[i] = I_gate_button

        # Extract gates from layers
        cleaned_layers = [list(map(lambda button: button.gate, layer)) for layer in cleaned_layers]

        # Calculate circuit matrix
        if not len(cleaned_layers):     # Empty circuit
            return None
        if len(cleaned_layers[0]) == 1: # Single wire
            circuit_matrix = cleaned_layers[0][0].matrix
            for layer in cleaned_layers[1:]:
                circuit_matrix = layer[0].matrix * circuit_matrix
            return circuit_matrix
        elif len(cleaned_layers) == 1:  # Single layer
            layer_matrix = cleaned_layers[0][0].matrix
            for gate in cleaned_layers[0][1:]:
                layer_matrix = layer_matrix ** gate.matrix
            return layer_matrix
        else:                           # Multiple wires and layers
            layer_matrix = cleaned_layers[0][0].matrix
            for gate in cleaned_layers[0][1:]:
                layer_matrix = layer_matrix ** gate.matrix
            circuit_matrix = layer_matrix
            for layer in cleaned_layers[1:]:
                layer_matrix = layer[0].matrix
                for gate in layer[1:]:
                    layer_matrix = layer_matrix ** gate.matrix
                circuit_matrix = layer_matrix * circuit_matrix
            return circuit_matrix

    
    def placeGate(self, gate, wire):
        self.gate_place_area.placeGate(gate, int(wire))


