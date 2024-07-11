from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QPushButton

class RunStopSection(QGroupBox):
    def __init__(self, run_program_callback, stop_program_callback):
        super().__init__("Run/Stop Program")

        self.run_program_callback = run_program_callback
        self.stop_program_callback = stop_program_callback

        layout = QVBoxLayout()

        run_button = QPushButton("Run Program")
        run_button.setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }")
        run_button.clicked.connect(self.run_program)
        layout.addWidget(run_button)

        stop_button = QPushButton("Stop Program")
        stop_button.setStyleSheet("QPushButton { font-size: 16px; padding: 10px; }")
        stop_button.clicked.connect(self.stop_program)
        layout.addWidget(stop_button)

        self.setLayout(layout)

    def run_program(self):
        self.run_program_callback()

    def stop_program(self):
        self.stop_program_callback()
