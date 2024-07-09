from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
from PyQt5.QtCore import Qt

class SuggestSettings(QGroupBox):
    def __init__(self, suggest_settings_callback, push_settings_callback, run_program_callback, stop_program_callback):
        super().__init__("Answer These For Setting Suggestions")

        self.run_program_callback = run_program_callback
        self.stop_program_callback = stop_program_callback

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.entries = {}

        questions = [
            "Water volume for relays 1 & 2 (uL):",
            "Water volume for relays 3 & 4 (uL):",
            "Water volume for relays 5 & 6 (uL):",
            "Water volume for relays 7 & 8 (uL):",
            "Water volume for relays 9 & 10 (uL):",
            "Water volume for relays 11 & 12 (uL):",
            "Water volume for relays 13 & 14 (uL):",
            "Water volume for relays 15 & 16 (uL):",
            "How often should each cage receive water? (Seconds):",
            "Water window start (hour, 24-hour format):",
            "Water window end (hour, 24-hour format):"
        ]

        for question in questions:
            entry = QLineEdit()
            entry.setStyleSheet("QLineEdit { font-size: 14px; padding: 5px; }")
            entry.setText("0")
            form_layout.addRow(QLabel(question), entry)
            self.entries[question] = entry

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        suggest_button = QPushButton("Suggest Settings")
        suggest_button.setStyleSheet("QPushButton { font-size: 14px; padding: 5px; }")
        suggest_button.clicked.connect(suggest_settings_callback)
        button_layout.addWidget(suggest_button)

        push_button = QPushButton("Push Settings")
        push_button.setStyleSheet("QPushButton { font-size: 14px; padding: 5px; }")
        push_button.clicked.connect(push_settings_callback)
        button_layout.addWidget(push_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_setting_input(self, layout, label_text, default_value):
        layout.addWidget(QLabel(label_text))
        entry = QLineEdit()
        entry.setStyleSheet("QLineEdit { font-size: 14px; padding: 5px; }")
        entry.setText(str(default_value))
        layout.addWidget(entry)
        return entry

    def get_entry_values(self):
        values = {}
        for label, entry in self.entries.items():
            try:
                values[label] = int(entry.text())
            except ValueError:
                QMessageBox.warning(self, "Input Error", f"Please enter a valid integer for: {label}")
                return None
        return values
