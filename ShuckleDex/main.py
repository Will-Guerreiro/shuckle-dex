import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout)
from PyQt6.QtCore import Qt
from requests import RequestException
from api.get_pokemon import get_pokemon_name

class ShuckleDex(QWidget):
    def __init__(self):
        super().__init__()
        self.welcome_label = QLabel("Welcome to Shuckle Dex!", self)
        self.enter_pokemon_name = QLabel("Enter Pokémon name or ID...", self)
        self.pokemon_name = QLineEdit(self)
        self.get_pokemon = QPushButton("Get Pokémon", self)
        self.pokemon_img = QLabel(self)
        self.pokemon_description = QLabel(self)
        self.initUI()



    def initUI(self):
        self.setWindowTitle("Shuckle Dex")
        vbox = QVBoxLayout()
        qform = QFormLayout()

        qform.addRow(self.welcome_label)
        qform.addRow(self.enter_pokemon_name)
        qform.addRow(self.pokemon_name)
        qform.addRow(self.get_pokemon)

        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.enter_pokemon_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pokemon_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(vbox)
        vbox.addLayout(qform)


        vbox.addWidget(self.pokemon_img)
        vbox.addWidget(self.pokemon_description)

        self.welcome_label.setObjectName("welcome_label")
        self.enter_pokemon_name.setObjectName("enter_pokemon_name")
        self.pokemon_name.setObjectName("pokemon_name")
        self.get_pokemon.setObjectName("get_pokemon")
        self.setStyleSheet("""
            QLabel#welcome_label{
                font-size: 40px;
                font-family: calibri;
            }
            QLineEdit#pokemon_name{
                font-size: 40px;
                font-family: calibri;
            }
            QLabel#enter_pokemon_name{
                color: rgba(255, 255, 255, 120);
            }
            QPushButton#get_pokemon{
                font-size: 40px;
                font-family: calibri;
            }
        """)

        self.get_pokemon.clicked.connect(lambda:get_pokemon_name(self.pokemon_name.text()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    shuckle_dex = ShuckleDex()
    shuckle_dex.show()
    sys.exit(app.exec())