import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import librosa
import sounddevice as sd
import numpy as np

class HolaEnsayo(QWidget):
    def __init__(self):
        super().__init__()
        self.tiempo_lectura = 6000
        self.setWindowTitle("Hola Ensayo")
        self.showMaximized()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        self.hola_imagen()

    def hola_imagen(self):
        self.bienvenida_image = QLabel()
        pixmap = QPixmap("archivos_relacionados/imagenes/bienvenida_o_a.png").scaled(self.screen_width,self.screen_height,Qt.AspectRatioMode.KeepAspectRatio)
        self.bienvenida_image.setPixmap(pixmap)
        self.bienvenida_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bienvenida_image)
        self.update()
        self.hola_timer()

    def hola_timer(self):
        QTimer.singleShot(self.tiempo_lectura, self.a_continuacion_imagen)

    def a_continuacion_imagen(self):
        self.layout.removeWidget(self.bienvenida_image)
        self.bienvenida_image.deleteLater()
        self.bienvenida_image = None
        self.acont_image = QLabel()
        pixmap = QPixmap("archivos_relacionados/imagenes/a_continuacion.png").scaled(self.screen_width,self.screen_height,Qt.AspectRatioMode.KeepAspectRatio)
        self.acont_image.setPixmap(pixmap)
        self.acont_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.acont_image)
        self.update()
        self.a_continuacion_timer()

    def a_continuacion_timer(self):
        QTimer.singleShot(self.tiempo_lectura, self.primero_escuchara_imagen)

    def primero_escuchara_imagen(self):
        self.layout.removeWidget(self.acont_image)
        self.acont_image.deleteLater()
        self.acont_image = None
        self.priesc_image = QLabel()
        pixmap = QPixmap("archivos_relacionados/imagenes/primero_escuchara.png").scaled(self.screen_width,self.screen_height,Qt.AspectRatioMode.KeepAspectRatio)
        self.priesc_image.setPixmap(pixmap)
        self.priesc_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.priesc_image)
        self.update()
        self.primero_escuchara_timer()

    def primero_escuchara_timer(self):
        QTimer.singleShot(self.tiempo_lectura, self.goto_ensayo_imagen)

    def goto_ensayo_imagen(self):
        self.layout.removeWidget(self.priesc_image)
        self.priesc_image.deleteLater()
        self.priesc_image = None
        self.iniciemos_image = QLabel()
        pixmap = QPixmap("archivos_relacionados/imagenes/iniciemos_ensayo.png").scaled(self.screen_width,self.screen_height,Qt.AspectRatioMode.KeepAspectRatio)
        self.iniciemos_image.setPixmap(pixmap)
        self.iniciemos_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.iniciemos_image)
        self.update()
        self.goto_ensayo_timer()

    def goto_ensayo_timer(self):
        QTimer.singleShot(self.tiempo_lectura, self.goto_ensayo)

    def goto_ensayo(self):
        self.layout.removeWidget(self.iniciemos_image)
        self.iniciemos_image.deleteLater()
        self.iniciemos_image = None
        self.hide()
        self.ensayo = EnsayoMusical()
        self.ensayo.show()
        self.close()

class EnsayoMusical(QWidget):

    def __init__(self):
        super().__init__()
        self.audio_file = "archivos_relacionados/pista_ensayo/7_rel_manantial _de_amor.mp3"
        self.shhhhh = 1.98
        self.setWindowTitle("Ensayo Musical")
        self.showMaximized()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)

        self.silencio_imagen()

    def silencio_imagen(self):
        self.silence_image = QLabel()
        self.silence_image.setPixmap(QPixmap("archivos_relacionados/imagenes/cruz.png"))
        self.silence_image.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.silence_image)  # Add the silence image to the layout
        self.update()
        self.silencio_timer()
    
    def silencio_timer(self):
        QTimer.singleShot(100, self.silencio_action)

    def silencio_action(self):
        if self.audio_file:
            data,sr = librosa.load(self.audio_file)
            mute_duration = int(sr*self.shhhhh)
            mute_sound = np.zeros(mute_duration,dtype=np.float32)
            sd.play(mute_sound,sr)
            sd.wait()
            self.pista_imagen()

    def pista_imagen(self):
        self.layout.removeWidget(self.silence_image)
        self.silence_image.deleteLater()
        self.silence_image = None
        self.audio_image = QLabel()
        self.audio_image.setPixmap(QPixmap("archivos_relacionados/imagenes/parlante.png"))
        self.audio_image.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.audio_image)  # Add the audio image to the layout
        self.update()
        self.pista_timer()

    def pista_timer(self):
        QTimer.singleShot(100, self.pista_action)  # Delay the call to self.pista_action() by 100 ms

    def pista_action(self):
        if self.audio_file:
            print("Reproduciendo audio:", self.audio_file)
            data, sr = librosa.load(self.audio_file)
            n_samples = int(20 * sr)
            sd.play(data[:n_samples], sr)
            sd.wait()
            self.show_pregunta1()

    def show_pregunta1(self):
        self.close()
        self.pregunta1_window = EnsayoPregunta1()
        self.pregunta1_window.show()

class EnsayoPregunta1(QWidget):
    volver_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.content_sam1()

    def content_sam1(self):
        self.setWindowTitle("Pregunta Uno") #título de la ventana
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))  #color de la ventana
        self.setPalette(palette)
        layout = QVBoxLayout()
        self.showMaximized()

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
            button.clicked.connect(lambda _, num=i: self.answer_sam1(num))
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

    def answer_sam1(self, answer):
        print("Respuesta seleccionada:", answer)
        self.close()
        self.next_window = EnsayoPregunta2()
        self.next_window.show()


class EnsayoPregunta2(QWidget):

    def __init__(self):
        super().__init__()
        self.content_sam2()

    def content_sam2(self):
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
            button.clicked.connect(lambda _, num=i: self.answer_sam2(num))
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

    def answer_sam2(self, answer):
        print("Respuesta seleccionada:", answer)
        self.close()
        self.next_window = EnsayoPregunta3() #exporta la respuesta a la siguiente clase
        self.next_window.show()

class EnsayoPregunta3(QWidget):
    
    def __init__(self):
        super().__init__()
        self.content_sam3()

    def content_sam3(self):
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

        # Botones de respuesta
        buttons_layout = QHBoxLayout()
        for i in range(1, 6):
            button = QPushButton()
            button.setStyleSheet("border: 1.6px solid black; border-radius: 8px;")
            pixmap = QPixmap(f"archivos_relacionados/imagenes/icono_tres{i}.png").scaled(150,150, Qt.AspectRatioMode.KeepAspectRatio) #botones que van del 1 al 5
            button.setIcon(QIcon(pixmap))
            button.setIconSize(pixmap.size())
            button.clicked.connect(lambda _, num=i: self.answer_sam3(num))
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

    def answer_sam3(self,answer): #importa la primera respuesta SAM
        print("Respuesta seleccionada:", answer)        
        self.close()
        self.repeat_or_not()

    def repeat_or_not(self):
        popup = QMessageBox()
        popup.setWindowTitle("Repetir ensayo")
        popup.setText("¿Quiere repetir el ensayo?")
        popup.setIcon(QMessageBox.Icon.Question)
        popup.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        popup.setDefaultButton(QMessageBox.StandardButton.No)
        popup.buttonClicked.connect(self.repeat_or_not_answer)
        popup.exec()

    def repeat_or_not_answer(self, button):
        if button.text() == "&Yes":
            self.close()
            self.next = HolaEnsayo()
            self.next.show()
        elif button.text() == "&No":
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HolaEnsayo()
    window.show()
    app.exec()   
