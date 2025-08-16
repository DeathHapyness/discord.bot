import sys
import threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from bot_logic import run_bot  

log_text_widget = None

def log_message(msg):
    if log_text_widget:
        log_text_widget.append(msg)

class BotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BotDiscord Dashboard")
        self.setGeometry(300, 300, 400, 190)
        layout = QVBoxLayout()

        self.status_label = QLabel("Status: Bot offline")
        self.status_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(self.status_label)

        self.setStyleSheet("background-color: #1e1e1e;")



        self.start_button = QPushButton("Iniciar Bot")
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 8px; padding: 8px 16px;")
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Parar Bot (encerra app)")
        self.stop_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 8px; padding: 8px 16px;")
        self.stop_button.clicked.connect(self.stop_bot)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def start_bot(self):
        self.status_label.setText("Status: Bot online")
        threading.Thread(target=run_bot, daemon=True).start()

    def stop_bot(self):
        log_message("Encerrando aplicação...")
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotGUI()
    window.show()
    sys.exit(app.exec())
