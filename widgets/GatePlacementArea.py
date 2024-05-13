from functools import partial

from PyQt6.QtWidgets import QWidget, QScrollArea, QGridLayout, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt

from widgets.GateButton import GateButton
from widgets.Wire import Wire
from models.Gate import Gate
from models.Matrix import Matrix

class GatePlacementArea(QScrollArea):

    def __init__(self, wire_count, circuit_depth, toggle_gate_actions, global_wire_add, placed_gates=None):
        super().__init__()

        self.wire_count = wire_count
        self.circuit_depth = circuit_depth
        self.toggle_gate_actions = toggle_gate_actions
        self.global_wire_add = global_wire_add
        self.selected_gate_button = None
        self.wire_lines = [[Wire() for _ in range(self.circuit_depth)] for _ in range(self.wire_count)]
        self.buttons_per_layer = [[None] * self.wire_count for _ in range(self.circuit_depth)]

        self.initUI()
        self.populateCircuit(placed_gates)

        # if placed_gates:
        #     self.place_gates(placed_gates)


    def initUI(self):
        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(50)

        # Set wires and invisible buttons for consistent padding
        for i, wire_line in enumerate(self.wire_lines):
            for j, wire in enumerate(wire_line):
                self.grid.addWidget(wire, i, j)
        for i in range(self.wire_count):
            inv_gate = Gate(Matrix([[1, 0], [0, 1]]), 'Identity', 'I-Inv')
            self.placeGate(inv_gate, i, invisible=True)

        # Adding spacers at bottom/right of grid
        self.vspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.grid.addItem(self.vspacer, self.wire_count, 0, 1, -1)
        # self.hspacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # self.grid.addItem(self.hspacer, 0, 4, -1, 1)

        # Circuit
        circuit = QWidget()
        circuit.setLayout(self.grid)

        # Scroll Widget setup
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.setWidget(circuit)


    def populateCircuit(self, placed_gates):
        if not placed_gates:
            I_gate = Gate(Matrix([[1, 0], [0, 1]]), 'Identity', 'I')
            self.placeGate(I_gate, 0)


    def placeGate(self, gate, wire, invisible=False, specific_layer=None):
        print(f'Adding gate {gate} to wire {wire}...')
        # Add wires if needed
        if not invisible and wire + gate.input_size > self.wire_count:
            for _ in range((wire + gate.input_size) - self.wire_count):
                self.global_wire_add()

        # Find first layer with an empty spot on the specified wire
        if specific_layer is not None:
            placement_layer = specific_layer
        elif invisible:
            placement_layer = self.circuit_depth - 1
        else:
            placement_layer = 0
            for layer in self.buttons_per_layer:
                if not layer[wire]:
                    break
                placement_layer += 1

        # Add layer if needed
        if not invisible and placement_layer == self.circuit_depth:
            self.addLayer()
            placement_layer = self.circuit_depth - 2

        # Place gate on circuit
        gate_button = GateButton(gate, wire, placement_layer, invisible=invisible)
        gate_button.clicked.connect(partial(self.toggle, gate_button))
        if invisible:
            self.grid.addWidget(gate_button, gate_button.wire, self.circuit_depth - 1, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            self.grid.addWidget(gate_button, gate_button.wire, gate_button.layer, gate.input_size, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        # Save change on layers object
        self.buttons_per_layer[gate_button.layer][gate_button.wire] = gate_button
        for i in range(gate.input_size - 1):
            self.buttons_per_layer[gate_button.layer][gate_button.wire + (1 + i)] = '*'

        # Keep shifted button highlighted
        if specific_layer is not None:
            self.toggle(gate_button)

        self.printCircuitState()

    
    def deleteGate(self, button=None):
        buttton_to_delete = button if button else self.selected_gate_button
        print(f'Deleting gate {buttton_to_delete.gate} from wire {buttton_to_delete.wire} at layer {buttton_to_delete.layer}...')
        
        # Remove from layers object
        for i in range(buttton_to_delete.gate.input_size):
            self.buttons_per_layer[buttton_to_delete.layer][buttton_to_delete.wire + i] = None

        # Remove from grid
        self.grid.removeWidget(buttton_to_delete)
        buttton_to_delete.deleteLater()
        if buttton_to_delete == self.selected_gate_button:
            self.toggle(buttton_to_delete)

        self.printCircuitState()

    
    def addLayer(self):
        # Updating inner circuit representation
        self.buttons_per_layer.append([None] * self.wire_count)
        for wire_line in self.wire_lines:
            wire_line.append(Wire())

        # Set wires and invisible buttons for consistent padding
        for i, wire_line in enumerate(self.wire_lines):
            self.grid.addWidget(wire_line[-1], i, self.circuit_depth)
        self.circuit_depth += 1
        for i in range(self.wire_count):
            inv_gate = Gate(Matrix([[1, 0], [0, 1]]), 'Identity', 'I-Inv')
            self.placeGate(inv_gate, i, invisible=True)

        # Remove previous invisible buttons
        for button in self.buttons_per_layer[-2]:
            self.deleteGate(button)


    def addWire(self):
        # Remove vertical spacer in last row
        self.grid.removeItem(self.vspacer)

        # Updating inner circuit representation
        for layer in self.buttons_per_layer:
            layer.append(None)

        # Add new wire and invisble button (for height) to last row
        self.wire_lines.append([Wire() for _ in range(self.circuit_depth)])
        for i, wire in enumerate(self.wire_lines[-1]):
            self.grid.addWidget(wire, self.wire_count, i)
        I_gate = Gate(Matrix([[1, 0], [0, 1]]), 'Identity', 'I-Inv')
        self.placeGate(I_gate, self.wire_count, invisible=True)
        self.wire_count += 1

        # Place vertical spacer in the new last row
        self.grid.addItem(self.vspacer, self.wire_count, 0, 1, -1)

        # Add wire option from gate placement dropdown
        self.addWireOption(self.wire_count)

        # Reset scrollbar to the bottom
        # self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    
    def deleteWire(self):
        # Remove vertical spacer in last row
        self.grid.removeItem(self.vspacer)

        # Remove gates on last wire
        for layer in self.buttons_per_layer:
            last_button = layer[-1]
            if not last_button:
                continue
            elif type(last_button) == GateButton:
                self.deleteGate(last_button)
            else: # last_gate == '*'
                for button in layer[-2::-1]:
                    if type(button) == GateButton:
                        print(button.gate.getButtonName())
                        self.deleteGate(button)
                        break

        # Remove "wires" on last wire
        for wire in self.wire_lines[-1]:
            self.grid.removeWidget(wire)
            wire.deleteLater()
        self.wire_lines.pop()

        # Remove wire from layers object and update internal model
        for layer in self.buttons_per_layer:
            layer.pop()
        self.wire_count -= 1

        # Place vertical spacer in the new last row
        self.grid.addItem(self.vspacer, self.wire_count, 0, 1, -1)

        # Remove wire option from gate placement dropdown
        self.removeWireOption(self.wire_count)

        self.printCircuitState()


    def lshiftGate(self):
        # Do nothing if already at the left most spot
        if self.selected_gate_button.layer == 0:
            return

        # Find opening to the left
        button = self.selected_gate_button
        input_size = self.selected_gate_button.gate.input_size
        for i, layer in enumerate(self.buttons_per_layer[button.layer - 1::-1]):
            if all(spot is None for spot in layer[button.wire:button.wire + (input_size)]):
                temp_button = self.selected_gate_button.deepcopy()
                self.deleteGate(button)
                self.placeGate(temp_button.gate, temp_button.wire, specific_layer=(button.layer - i - 1))
                break


    def rshiftGate(self):
        # Add layer if gate cannot go right (is in second-to-last layer)
        if self.selected_gate_button.layer == self.circuit_depth - 2:
            self.addLayer()
        
        # Find opening to the right
        button = self.selected_gate_button
        input_size = self.selected_gate_button.gate.input_size
        for i, layer in enumerate(self.buttons_per_layer[button.layer + 1:]):
            if 1 + i + button.layer == self.circuit_depth - 1:     # Reached the end
                self.addLayer()
                temp_button = self.selected_gate_button.deepcopy()
                self.deleteGate(button)
                self.placeGate(temp_button.gate, temp_button.wire, specific_layer=(self.circuit_depth - 2))
            elif all(spot is None for spot in layer[button.wire:button.wire + (input_size)]):
                temp_button = self.selected_gate_button.deepcopy()
                self.deleteGate(button)
                self.placeGate(temp_button.gate, temp_button.wire, specific_layer=(button.layer + i + 1))
                break


    def toggle(self, gate_button):
        if not self.selected_gate_button:
            self.selected_gate_button = gate_button
            self.toggle_gate_actions()
        elif self.selected_gate_button == gate_button:
            self.selected_gate_button = None
            self.toggle_gate_actions()
        else:
            self.selected_gate_button.toggle()
            self.selected_gate_button = gate_button
        gate_button.toggle()
        
        
    def printCircuitState(self):
        circuit_layout = ['' for _ in self.buttons_per_layer[0]]
        for layer in self.buttons_per_layer:
            for i, button in enumerate(layer):
                if not button:
                    gate_rep = '-\t'
                elif type(button) == str:
                    gate_rep = '*\t'
                else:
                    gate_rep = f'{button.gate.getButtonName()}\t'
                circuit_layout[i] += gate_rep
        
        for wire in circuit_layout:
            print(wire)
        print()
