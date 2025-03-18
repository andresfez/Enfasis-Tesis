from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import os
import csv

class Pregunta_Uno(QWidget):
    iteracion_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.contador = 0
        self.nombre_cancion = ""
        file_exist = os.path.isfile("registro_participantes_EEG.csv")
        if file_exist:
            with open("registro_participantes_EEG.csv", 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                last_row = None
                for row in reader:
                    if row['ID'] != '0':
                        last_row = row
                if last_row:
                    self.contador = int(last_row['ID'])
                    print("Contador en preguntas.py es: ", self.contador)
                else:
                    self.contador = 0
        self.content_fam()

    def content_fam(self):
        self.setWindowTitle("Pregunta Uno") #título de la ventana
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))  #color de la ventana
        self.setPalette(palette)
        layout = QVBoxLayout()

        # Texto de la pregunta
        layout.addSpacing(140)
        first_question_label = QLabel("¿Qué tan familiar le resultó la pieza musical?") #pregunta a mostrar
        first_question_label.setFont(QFont("Arial", 29))
        first_question_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(first_question_label)

        # Botones de respuesta
        buttons_layout = QHBoxLayout()
        for i in range(1, 6):
            button = QPushButton(str(i)) #botones que van del 1 al 5
            button.setStyleSheet("border: 1.6px solid black; border-radius: 8px;")
            button.setFont(QFont("Arial", 16))
            button.clicked.connect(lambda _, num=i: self.answer_fam(num))
            buttons_layout.addWidget(button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignBaseline)
        layout.addLayout(buttons_layout)

        # Texto debajo de los botones
        final_text_layout = QHBoxLayout()
        first_text = QLabel("Nada\nfamiliar") #debajo del botón "1"
        first_text.setFont(QFont("Arial", 28))
        first_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        final_text_layout.addWidget(first_text)

        second_text = QLabel("Altamente\nfamiliar") #debajo del botón "5"
        second_text.setFont(QFont("Arial", 28))
        second_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        final_text_layout.addWidget(second_text)

        layout.addLayout(final_text_layout)
        self.setLayout(layout)
        self.showMaximized()

    def answer_fam(self, answer):
        print("Respuesta seleccionada:", answer)
        self.result_1 = answer #nombra la respuesta
        self.cont = self.contador
        self.nom_can = self.nombre_cancion
        self.registry_SAMs() #guarda la respuesta
        self.close()
        self.next_window = Pregunta_Dos(self.result_1,self.cont,self.nom_can) #exporta la respuesta a la siguiente clase
        self.next_window.iteracion_signal.connect(self.jump)
        self.next_window.show()

    def jump(self):
        self.iteracion_signal.emit()
    
    def registry_SAMs(self):
        namefile = 'respuestas_participante_'+str(self.contador)+'.csv'
        with open(namefile, 'a', newline='', encoding='utf-8') as csvfile: #para crear la tabla con las respuestas SAM
            writer = csv.writer(csvfile)
            if os.stat(namefile).st_size == 0: #si no existe  el archivo...
                writer.writerow(['Nombre cancion', 'Respuesta Familiaridad', 'Respuesta SAM 1', 'Respuesta SAM 2']) #... lo crea, y establece los títulos de las columnas

class Pregunta_Dos(QWidget):
    iteracion_signal = pyqtSignal()

    def __init__(self, first_answer, contador,nom_can):
        super().__init__()
        self.first_answer = first_answer
        self.contador = contador
        self.nom_can = nom_can
        self.content_sam1()

    def content_sam1(self):
        self.showMaximized()
        self.setWindowTitle("Pregunta Dos") #título de la ventana
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white")) #color ventana
        self.setPalette(palette)
        layout = QVBoxLayout()

        # Texto de la pregunta
        layout.addSpacing(140)
        second_question_label = QLabel("¿Qué tan activante o relajante\nle resultó la pieza musical?") #pregunta a mostrar
        second_question_label.setFont(QFont("Arial", 29))
        second_question_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(second_question_label)

        # Botones de respuesta
        buttons_layout = QHBoxLayout()
        for i in range(1, 6):
            button = QPushButton()
            button.setStyleSheet("border: 1.6px solid black; border-radius: 8px;")
            pixmap = QPixmap(f"archivos_relacionados/imagenes/icono_dos{i}.png").scaled(150,150, Qt.AspectRatioMode.KeepAspectRatio) #botones que van del 1 al 5
            button.setIcon(QIcon(pixmap))
            button.setIconSize(pixmap.size())
            button.clicked.connect(lambda _, num=i: self.answer_sam1(num))
            buttons_layout.addWidget(button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignBaseline)
        layout.addLayout(buttons_layout)

        # Texto debajo de los botones
        final_text_layout = QHBoxLayout()
        first_text = QLabel("Relajante") #debajo del botón "1"
        first_text.setFont(QFont("Arial", 28))
        first_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        final_text_layout.addWidget(first_text)

        second_text = QLabel("Activante") #debajo del botón "5"
        second_text.setFont(QFont("Arial", 28)) 
        second_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        final_text_layout.addWidget(second_text)

        layout.addLayout(final_text_layout)
        self.setLayout(layout)

    def answer_sam1(self, answer):
        print("Respuesta seleccionada:", answer)
        self.result_1 = self.first_answer
        self.result_2 = answer #nombra la respuesta
        self.nombre_pista = self.nom_can
        self.close()
        self.next_window = Pregunta_Tres(self.result_1,self.result_2,self.contador,self.nombre_pista) #exporta la respuesta a la siguiente clase
        self.next_window.iteracion_signal.connect(self.jump_again)
        self.next_window.show()

    def jump_again(self):
        self.iteracion_signal.emit()

class Pregunta_Tres(QWidget):
    iteracion_signal = pyqtSignal()
    
    def __init__(self, first_answer, second_answer, contador,nombre_pista):
        super().__init__()
        self.first_answer = first_answer
        self.second_answer = second_answer
        self.contador = contador
        self.nombre_pista = nombre_pista
        self.content_sam2()

    def content_sam2(self):
        self.showMaximized()
        self.setWindowTitle("Pregunta Tres") #título de la ventana
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white")) #color ventana
        self.setPalette(palette)
        layout = QVBoxLayout()

        # Texto de la pregunta
        layout.addSpacing(140)
        second_question_label = QLabel("¿Qué tan agradable o desagradable\nle resultó la pieza musical?") #pregunta a mostrar
        second_question_label.setFont(QFont("Arial", 28))
        second_question_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(second_question_label)

        ## Botones de respuesta
        buttons_layout = QHBoxLayout()
        for i in range(1, 6):
            button = QPushButton()
            button.setStyleSheet("border: 1.6px solid black; border-radius: 8px;")
            pixmap = QPixmap(f"archivos_relacionados/imagenes/icono_tres{i}.png").scaled(150,150, Qt.AspectRatioMode.KeepAspectRatio) #botones que van del 1 al 5
            button.setIcon(QIcon(pixmap))
            button.setIconSize(pixmap.size())
            button.clicked.connect(lambda _, num=i: self.answer_sam2(num))
            buttons_layout.addWidget(button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignBaseline)
        layout.addLayout(buttons_layout)

        # Texto debajo de los botones
        final_text_layout = QHBoxLayout()
        first_text = QLabel("Desagradable") #debajo del botón "1"
        first_text.setFont(QFont("Arial", 28))
        first_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        final_text_layout.addWidget(first_text)

        second_text = QLabel("Agradable") #debajo del botón "5"
        second_text.setFont(QFont("Arial", 28)) 
        second_text.setAlignment(Qt.AlignmentFlag.AlignRight)
        final_text_layout.addWidget(second_text)

        layout.addLayout(final_text_layout)
        self.setLayout(layout)

    def answer_sam2(self, answer): #importa la primera respuesta SAM
        print("Respuesta seleccionada:", answer)
        namefile = 'respuestas_participante_'+str(self.contador)+'.csv'
        with open(namefile, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.nombre_pista ,self.first_answer, self.second_answer, answer]) #redacta ambas respuestas en la tabla de respuestas SAM
        self.iteracion_signal.emit()
        self.close()  #cerrar ventana segunda pregunta SAM

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Pregunta_Uno()
    window.show()
    app.exec()   