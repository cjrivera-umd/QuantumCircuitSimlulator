from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QDialogButtonBox, QVBoxLayout, QSizePolicy

class QubitProbabilityDialog(QDialog):

    def __init__(self, wire, prob_0, prob_1, parent=None):
        super().__init__(parent)

        self.initUI(wire, prob_0, prob_1)


    def initUI(self, wire, prob_0, prob_1):
        self.setWindowTitle(f'Qubit {wire} Probability Distribution')

        # Creating read-only text boxes
        self.prob_0_label = QLabel('Probability of 0')
        self.prob_0_textbox = QLineEdit()
        self.prob_0_textbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.prob_0_textbox.setText(format(prob_0, ".2%"))
        self.prob_0_textbox.setReadOnly(True)

        self.prob_1_label = QLabel('Probability of 1')
        self.prob_1_textbox = QLineEdit()
        self.prob_1_textbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.prob_1_textbox.setText(format(prob_1, ".2%"))
        self.prob_1_textbox.setReadOnly(True)

        # Creating Ok button
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.close)

        # Create layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.prob_0_label)
        self.layout.addWidget(self.prob_0_textbox)
        self.layout.addWidget(self.prob_1_label)
        self.layout.addWidget(self.prob_1_textbox)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


        def close(self):
            print('')