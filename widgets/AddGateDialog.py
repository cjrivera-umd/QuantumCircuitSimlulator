from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QDialogButtonBox, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import QEvent, Qt


class AddGateDialog(QDialog):

    def __init__(self, add_gate_func, parent=None):
        super().__init__(parent)

        self.add_gate_func = add_gate_func

        self.installEventFilter(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Gate')

        # Creating Gate name widgets
        self.name_label = QLabel('Gate Name*')
        self.name_textbox = QLineEdit()
        self.name_textbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Creating Gate alias widgets
        self.alias_label = QLabel('Gate Alias')
        self.alias_textbox = QLineEdit()
        self.alias_textbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Creating gate matrix widgets
        self.matrix_label = QLabel('Gate Matrix*')
        self.matrix_textbox = QPlainTextEdit()
        self.matrix_textbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Creating Save button
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.validate)

        # Creating layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_textbox)
        self.layout.addWidget(self.alias_label)
        self.layout.addWidget(self.alias_textbox)
        self.layout.addWidget(self.matrix_label)
        self.layout.addWidget(self.matrix_textbox)
        self.layout.addWidget(save_button)
        self.setLayout(self.layout)


    def eventFilter(self, obj, event):
        if obj is self and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Escape, Qt.Key.Key_Enter,):
                return True
        return super().eventFilter(obj, event)


    def validate(self):
        # Extract values
        name = self.name_textbox.text()
        alias = self.alias_textbox.text()
        matrix = self.matrix_textbox.toPlainText()

        # Confirm proper values
        valid_form = True
        if not name:
            valid_form = False
            self.name_label.setText('Gate Name* (Needed)')

        if not matrix:
            valid_form = False
            self.matrix_label.setText('Gate Matrix* (Needed)')
        
        if valid_form:
            self.add_gate_func({'name': name, 'alias': alias, 'matrix': matrix})

