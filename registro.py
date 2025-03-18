from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from menu import *
import csv
import os

class Registro(QMainWindow):
    registro_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.consecutivo = 0
        file_exist = os.path.isfile('registro_participantes_EEG.csv')
        if file_exist:
            with open('registro_participantes_EEG.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    last_row = row
                    if last_row and last_row['ID'] != 0:
                        self.consecutivo = int(last_row['ID'])
                        print('contador es: ', self.consecutivo)
                        break
        if  not file_exist:
            self.consecutivo = 0
            print('contador es: ', self.consecutivo)
        self.content_vreg()

    def content_vreg(self):
        self.setWindowTitle('Ingreso') #título de la ventana
        screen_geometry = self.screen().availableGeometry()
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        general_font = QFont("Arial", 16) #fuente usada
        central_widget.setStyleSheet("background-color: white;") #color ventana

        # Fecha
        date_label = QLabel("Fecha: " + QDate.currentDate().toString(Qt.DateFormat.ISODate)) #TextDate #"dddd MMMM d, yyyy" "para mostrar la fecha de hoy"
        date_label.setFont(general_font)
        main_layout.addWidget(date_label)

        # Nombre
        name_layout = QHBoxLayout() 
        name_label = QLabel("Nombre Completo:")
        name_layout.addWidget(name_label)
        name_input = QLineEdit() #campo de escritura para el nombre
        name_input.setObjectName("name_input")
        name_input.setFont(general_font)
        name_label.setFont(general_font)
        name_layout.addWidget(name_input)
        main_layout.addLayout(name_layout)
        main_layout.addSpacing(80)

        # Cédula
        number_layout = QHBoxLayout()
        number_label = QLabel("Cédula de Ciudadanía:")
        number_label.setFont(general_font)
        number_layout.addWidget(number_label)
        number_input = QLineEdit() #campo de escritura para el la cédula
        number_input.setValidator(QIntValidator())  
        number_input.setObjectName("number_input")
        number_input.setFont(general_font)
        number_layout.addWidget(number_input)
        main_layout.addLayout(number_layout)
        main_layout.addSpacing(80)

        # Botón
        next_window_button = QPushButton("Continuar") #el botón
        next_window_button.setFont(general_font)
        next_window_button.clicked.connect(self.open_v2) #conectar a la función del botón
        next_window_button.setStyleSheet("border: 1.2px solid black; border-radius: 8px;")
        main_layout.addWidget(next_window_button)

        self.setCentralWidget(central_widget)

        # Logos
        image_layout = QHBoxLayout()
        image_left = QLabel()
        image_left.setPixmap(QPixmap("archivos_relacionados/imagenes/logo_ECI.png").scaled(265,365,Qt.AspectRatioMode.KeepAspectRatio)) #logo de la escuela
        image_left.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom) #logo en la esquina inferior izquierda 
        image_layout.addWidget(image_left)

        image_center1 = QLabel()
        image_center1.setPixmap(QPixmap("archivos_relacionados/imagenes/Logo_Semillero_ Neurociencia_Basica_Clinica.png").scaled(190,290,Qt.AspectRatioMode.KeepAspectRatio)) #logo de la uniminuto
        image_center1.setAlignment(Qt.AlignmentFlag.AlignBottom) #logo en la esquina inferior derecha
        image_layout.addWidget(image_center1)

        image_center2 = QLabel()
        image_center2.setPixmap(QPixmap("archivos_relacionados/imagenes/logo_PROMISE.png").scaled(415,515,Qt.AspectRatioMode.KeepAspectRatio)) #logo de la uniminuto
        image_center2.setAlignment(Qt.AlignmentFlag.AlignBottom) #logo en la esquina inferior derecha
        image_layout.addWidget(image_center2)

        image_center3 = QLabel()
        image_center3.setPixmap(QPixmap("archivos_relacionados/imagenes/Logo_Semillero_ENEX.png").scaled(215,315, Qt.AspectRatioMode.KeepAspectRatio)) #logo de la uniminuto
        image_center3.setAlignment(Qt.AlignmentFlag.AlignBottom) #logo en la esquina inferior derecha
        image_layout.addWidget(image_center3)

        image_right = QLabel()
        image_right.setPixmap(QPixmap("archivos_relacionados/imagenes/logo_UNIM.png").scaled(290,390,Qt.AspectRatioMode.KeepAspectRatio)) #logo de la uniminuto
        image_right.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom) #logo en la esquina inferior derecha
        image_layout.addWidget(image_right)

        main_layout.addLayout(image_layout)
        self.setCentralWidget(central_widget)

    def registry_function(self, dia, nombre, cedula):
        registry_titles = ['Fecha', 'ID', 'Nombre', 'Cédula de ciudadanía']
        file_exists = os.path.isfile('registro_participantes_EEG.csv')
        with open('registro_participantes_EEG.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=registry_titles)
            if not file_exists: #si no existe el archivo de registro...
                writer.writeheader() #escribir las cabeceras
        if file_exists: #si ya existia el archivo de registro...
            with open('registro_participantes_EEG.csv', 'r', newline='', encoding='utf-8') as csvfile_read:
                reader = csv.DictReader(csvfile_read)
                last_row = None
                for row in reader:
                    last_row = row
                if last_row:
                    self.consecutivo = int(last_row['ID'])
        with open('registro_participantes_EEG.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=registry_titles)
            self.consecutivo += 1
            writer.writerow({'Fecha': dia, 'ID': self.consecutivo, 'Nombre': nombre, 'Cédula de ciudadanía': cedula})

    def open_v2(self):
        self.hide()
        nombre = self.findChild(QLineEdit, "name_input").text()
        cedula= self.findChild(QLineEdit, "number_input").text()
        dia = str(QDate.currentDate().toString(Qt.DateFormat.ISODate))
        self.registry_function(dia,nombre,cedula)
        self.prueba_window = Menu()
        self.prueba_window.registro_signal.connect(self.update_this_window)
        self.prueba_window.show()
        return dia
    
    def update_this_window(self):
        self.show()
        self.registro_signal.emit()
        print("The value of consecutivo is: ", self.consecutivo)
    
if __name__ == "__main__":
    app = QApplication([])
    inicio_window = Registro()
    inicio_window.show()
    app.exec()
