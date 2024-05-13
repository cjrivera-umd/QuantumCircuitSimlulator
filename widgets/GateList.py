from PyQt6.QtWidgets import QListWidget

from models.Gate import Gate
from models.Matrix import Matrix
from models.Coefficient import Coefficient

from widgets.AddGateDialog import AddGateDialog

class GateList(QListWidget):

    def __init__(self, add_button, del_button):
        super().__init__()
        
        add_button.clicked.connect(self.showAddDialog)
        del_button.clicked.connect(self.delGate)

        self.gates = [
            Gate(Matrix([[1, 0], [0, 1]]), 'Identity', 'I'),
            Gate(Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]), 'Identity', 'I_2'),
            Gate(Matrix([[0, 1], [1, 0]]), 'Pauli X', 'X'),
            Gate(Matrix([[1, 0], [0, -1]]), 'Pauli Z', 'Z'),
            Gate(Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]), 'Controlled NOT', 'CNOT'),
            Gate(Matrix([[1, 1], [1, -1]], Coefficient(1, 2, den_sqrt=True)), 'Hadamard', 'H')
        ]
        self.selected = None

        self.initUI()
    

    def initUI(self):
        self.currentItemChanged.connect(self.newSelection)

        for gate in self.gates:
            self.addItem(gate.getListName())


    def getSelectedGate(self):
        for gate in self.gates:
            if self.selected == gate.getListName():
                return gate
        
        return None


    def newSelection(self, selected):
        self.selected = selected.text()


    def showAddDialog(self):
        self.add_dialog = AddGateDialog(self.addGate, self)
        self.add_dialog.exec()


    def addGate(self, gate_info):
        # Extracting gate name and alias
        name = gate_info['name']
        alias = gate_info['alias'] if gate_info['alias'] else None

        # Extracting gate coefficient and matrix strings
        matrix_str = gate_info['matrix'].strip()
        coeff = Coefficient(1)
        if matrix_str[0] != '[':            # There is a coefficient
            matrix_start = matrix_str.find('[')
            coef_str, matrix_str = matrix_str[:matrix_start], matrix_str[matrix_start:]
            
            # Coefficient handling
            coef_str, num, den, num_sqrt, den_sqrt = coef_str.strip(), 1, 1, False, False
            if '/' in coef_str:                 # Has denominator
                num_str, den_str = coef_str.split('/')
                if '√' in num_str:              # Numerator has sqrt
                    num_sqrt = True
                    num_str = num_str[1:]
                if '√' in den_str:              # Denominator has sqrt
                    den_sqrt = True
                    den_str = den_str[1:]
                num, den = int(num_str), int(den_str)
            else:                               # No denominator
                if '√' in coef_str:             # Numerator has sqrt
                    num_sqrt = True
                    coef_str = coef_str[1:]
                num = int(coef_str)
            coef = Coefficient(num, den, num_sqrt, den_sqrt)

        # Matrix handling
        matrix_str = matrix_str.strip()
        matrix_str = matrix_str[1:-1]       # Removing [ ]
        rows_str = matrix_str.split(';')    # Dividing rows
        rows = []
        for row_str in rows_str:            # Converting rows to integers
            row = [int(elem) for elem in row_str.split(' ')]
            rows.append(row)
        matrix = Matrix(rows, coef)         # Creating matrix

        # Creating gate
        new_gate = Gate(matrix, name, alias)

        # Adding to list
        self.gates.append(new_gate)
        self.addItem(new_gate.getListName())

        self.add_dialog.close()


    def delGate(self):
        if (selectedRow := self.currentRow()):
            self.takeItem(selectedRow)