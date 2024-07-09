from PyQt5.QtWidgets import QTextEdit

class TerminalOutput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFixedHeight(150)
        self.append("System Messages will appear here.")
    
    def print_to_terminal(self, message):
        self.append(message)
        self.ensureCursorVisible() 
