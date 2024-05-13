from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QSpacerItem, QScrollArea, QComboBox
from PyQt6.QtCore import Qt

from widgets.GateList import GateList

class GateSection(QWidget):

    def __init__(self, intial_wire_count, placement_func):
        super().__init__()

        self.placement_func = placement_func

        self.initUI(intial_wire_count)


    def initUI(self, initial_wire_count):
        # Sizing
        self.setFixedWidth(250)
        self.setMinimumHeight(300)

        # Setting up gate header
        section_label = QLabel('Gates')
        add_gate = QPushButton('+')
        del_gate = QPushButton('–')
        header_box = QHBoxLayout()
        header_box.addWidget(section_label)
        header_box.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        header_box.addWidget(add_gate)
        header_box.addWidget(del_gate)

        # Setting up gate list and scroll widget
        self.gate_list = GateList(add_gate, del_gate)
        gates_scroll = QScrollArea()
        gates_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        gates_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        gates_scroll.setWidgetResizable(True)
        gates_scroll.setWidget(self.gate_list)

        # Action section
        place_gate_button = QPushButton('Place Gate on wire:')
        place_gate_button.clicked.connect(self.placementRequest)
        self.wire_picker = QComboBox()
        self.wire_picker.addItems([str(i) for i in range(initial_wire_count)])

        action_box = QHBoxLayout()
        action_box.addWidget(place_gate_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        action_box.addWidget(self.wire_picker, alignment=Qt.AlignmentFlag.AlignRight)
        

        # Setting up section layout
        section_box = QVBoxLayout()
        section_box.setSpacing(5)
        section_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        section_box.addLayout(header_box)
        section_box.addWidget(self.gate_list)
        section_box.addLayout(action_box)

        self.setLayout(section_box)


    def placementRequest(self):
        gate = self.gate_list.getSelectedGate()
        wire = self.wire_picker.currentText()
        self.placement_func(gate, wire)


    def addWireOption(self, wire):
        self.wire_picker.addItem(str(wire - 1))

    def removeWireOption(self, wire):
        self.wire_picker.removeItem(wire)