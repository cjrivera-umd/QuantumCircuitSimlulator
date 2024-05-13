import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QMainWindow

from widgets.GateSection import GateSection
from widgets.CircuitSection import CircuitSection
from widgets.OutputSection import OutputSection

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        DEFAULT_WIRE_COUNT = 3
        DEFAULT_DEPTH = 6

        output_section = OutputSection()
        circuit_section = CircuitSection(DEFAULT_WIRE_COUNT, DEFAULT_DEPTH, output_section.measureCircuit)
        gate_section = GateSection(DEFAULT_WIRE_COUNT, circuit_section.placeGate)

        # Maintaning wires consistent in the placement dropdown
        circuit_section.circuit_area.gate_place_area.addWireOption = gate_section.addWireOption
        circuit_section.circuit_area.gate_place_area.removeWireOption = gate_section.removeWireOption

        # Maintaning measurements consistent in the measurment section
        output_section.setMeasurements = circuit_section.circuit_area.measure_area.setMeasurements

        # Setting up layout
        sim_layout = QHBoxLayout()
        sim_layout.addWidget(gate_section)
        sim_layout.addWidget(circuit_section)
        sim_layout.addWidget(output_section)

        sim_widget = QWidget()
        sim_widget.setLayout(sim_layout)
        
        self.setCentralWidget(sim_widget)

        # Main Window setup
        self.setWindowTitle("Quantum Circuit Simulator")
        self.setGeometry(50,50,200,200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec())