import sys
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from requests import RequestException
from api.get_pokemon import get_pokemon_info

class ShuckleDex(QWidget):
    def __init__(self):
        super().__init__()
        self.welcome_label = QLabel("Welcome to Shuckle Dex!", self)
        self.enter_pokemon_name = QLabel("Enter Pokémon name or ID...", self)
        self.pokemon_name_input = QLineEdit(self)
        self.get_pokemon = QPushButton("Get Pokémon", self)
        self.pokemon_img_default = QLabel(self)
        self.pokemon_img_shiny = QLabel(self)
        self.pokemon_name = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Shuckle Dex")
        vbox = QVBoxLayout()
        qform = QFormLayout()
        hbox1 = QHBoxLayout()
        qform.addRow(self.welcome_label)
        qform.addRow(self.enter_pokemon_name)
        qform.addRow(self.pokemon_name_input)
        qform.addRow(self.get_pokemon)

        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.enter_pokemon_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pokemon_name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(vbox)
        vbox.addLayout(qform)
        vbox.addLayout(hbox1)

        hbox1.addWidget(self.pokemon_name)
        hbox1.addWidget(self.pokemon_img_default)
        hbox1.addWidget(self.pokemon_img_shiny)

        self.pokemon_img_default.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pokemon_img_shiny.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pokemon_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.welcome_label.setObjectName("welcome_label")
        self.enter_pokemon_name.setObjectName("enter_pokemon_name")
        self.pokemon_name_input.setObjectName("pokemon_name_input")
        self.get_pokemon.setObjectName("get_pokemon")
        self.pokemon_img_default.setObjectName("pokemon_img_default")
        self.pokemon_img_default.setObjectName("pokemon_img_shiny")
        self.pokemon_name.setObjectName("pokemon_name")
        self.setStyleSheet("""
            QLabel#welcome_label{
                font-size: 40px;
                font-family: calibri;
            }
            QLabel#pokemon_name{
                font-size: 40px;
            }
            QLineEdit#pokemon_name_input{
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

        self.get_pokemon.clicked.connect(self.handle_click)
        self.pokemon_name_input.returnPressed.connect(self.handle_click)

    def handle_click(self):
        name = self.pokemon_name_input.text()
        self.pokemon_name_input.clear()
        self.pokemon_img_default.clear()
        self.pokemon_name.clear()
        self.pokemon_img_default.setStyleSheet("font-size: 50px;")
        self.pokemon_img_default.setText("Buscando...")
        QApplication.processEvents()
        try:
            data = get_pokemon_info(name)
            self.display_pokemon_info(data)
        except requests.exceptions.HTTPError as http_error:
            match http_error.response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nPokémon not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

    def display_pokemon_info(self, data):
        name = data["name"]
        front_sprite = data["sprites"]["front_default"]
        front_shiny_sprite = data["sprites"]["front_shiny"]
        self.pokemon_name.setText(name.capitalize())
        pixmap_default = self.load_image(front_sprite)
        self.pokemon_img_default.setPixmap(pixmap_default)
        pixmap_shiny = self.load_image(front_shiny_sprite)
        self.pokemon_img_shiny.setPixmap(pixmap_shiny)

    def display_error(self, message):
        self.pokemon_name.clear()
        self.pokemon_img_default.clear()
        self.pokemon_img_shiny.clear()
        self.pokemon_name.setText(message)

    def load_image(self, url):
        response = requests.get(url)
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        return pixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    shuckle_dex = ShuckleDex()
    shuckle_dex.show()
    sys.exit(app.exec())