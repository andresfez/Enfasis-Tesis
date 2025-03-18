from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCharts import *
from preguntas import *
import sys
import os
import librosa
import random
import sounddevice as sd
import numpy as np
import time
#from main import main

class HolaPrueba(QWidget):
    iteracion_signal = pyqtSignal()
    registro_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hola Prueba')
        self.layout = QVBoxLayout()
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)
        self.setLayout(self.layout)
        self.showMaximized()
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        self.hola_imagen()

    def hola_imagen(self):
        self.bienvenida_image = QLabel()
        pixmap = QPixmap("archivos_relacionados/imagenes/iniciaremos_prueba.png").scaled(self.screen_width,self.screen_height,Qt.AspectRatioMode.KeepAspectRatio)
        self.bienvenida_image.setPixmap(pixmap)
        self.bienvenida_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.bienvenida_image)
        self.update()
        self.hola_timer()
    
    def hola_timer(self):
        QTimer.singleShot(2000, self.goto_prueba)

    def goto_prueba(self):
        self.layout.removeWidget(self.bienvenida_image)
        self.bienvenida_image.deleteLater()
        self.bienvenida_image = None
        self.hide()
        self.prueba = Prueba()
        self.prueba.iteracion_signal.connect(self.jump1)
        self.prueba.registro_signal.connect(self.jump2)
        self.prueba.show()
        self.close()

    def jump1(self):
        self.iteracion_signal.emit()

    def jump2(self):
        self.registro_signal.emit()

class Prueba(QWidget):
    iteracion_signal = pyqtSignal()
    registro_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.band = True
        self.bando = False
        self.audio_files = "archivos_relacionados/pistas"
        self.audios = [f for f in os.listdir(self.audio_files) if f.endswith('.mp3')]
        random.shuffle(self.audios)
        self.silence = [1.4, 1.6, 1.8, 2]
        self.setWindowTitle('Conexión')
        self.layout = QVBoxLayout()
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)
        self.setLayout(self.layout)
        self.showMaximized()
        self.start_loop()
    
    def start_loop(self):
        self.update()
        while self.band == True:
            if len(self.audios) > 0:
                audio_path = os.path.join(self.audio_files,self.audios[0])
                silence_duration = random.choice(self.silence)
                print("longitud: ", len(self.audios))
                print("Sonando: ",self.audios[0])
                print("Silence duration:", silence_duration)
                self.band = False
                nombre_guardado = str(self.audios[0])
                self.start_timer(audio_path, silence_duration, nombre_guardado)
                self.audios.pop(0)
            elif len(self.audios) == 0:
                    self.finish_protocol()
                    print("Todas las canciones han sido reproducidas")
                    break

    def start_timer(self,audio_path, silence_duration,nombre_guardado):
        QTimer.singleShot(100, lambda: self.silencio_pic(audio_path, silence_duration,nombre_guardado))

    def silencio_pic(self,audio_path, silence_duration,nombre_guardado):
        self.silence_image = QLabel()
        self.silence_image.setPixmap(QPixmap("archivos_relacionados/imagenes/cruz.png"))
        self.silence_image.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.silence_image)  # Add the silence image to the layout
        self.update()
        self.silencio_timer(audio_path, silence_duration,nombre_guardado)
    
    def silencio_timer(self,audio_path, silence_duration,nombre_guardado):
        QTimer.singleShot(100, lambda: self.silencio_action(audio_path, silence_duration,nombre_guardado))

    def silencio_action(self,audio_path, silence_duration,nombre_guardado):
        data,sr = librosa.load(audio_path)
        mute_duration = int(sr*silence_duration)
        mute_sound = np.zeros(mute_duration,dtype=np.float32)
        sd.play(mute_sound,sr,blocking=True)
        sd.wait()
        self.pista_pic(audio_path, silence_duration,nombre_guardado)

    def pista_pic(self,audio_path, silence_duration,nombre_guardado):
        self.layout.removeWidget(self.silence_image)
        self.silence_image.deleteLater()
        self.silence_image = None
        self.audio_image = QLabel()
        self.audio_image.setPixmap(QPixmap("archivos_relacionados/imagenes/parlante.png"))
        self.audio_image.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.audio_image)  # Add the audio image to the layout
        self.update()
        self.pista_timer(audio_path,silence_duration,nombre_guardado)

    def pista_timer(self,audio_path, silence_duration,nombre_guardado):
        QTimer.singleShot(100, lambda: self.pista_action(audio_path, silence_duration,nombre_guardado))

    def pista_action(self,audio_path, silence_duration,nombre_guardado):
        print("Reproduciendo audio:", audio_path)
        data, sr = librosa.load(audio_path)
        n_samples = int(20 * sr)
        sd.play(data[:n_samples], sr,blocking=True)
        sd.wait()
        self.update_pics(nombre_guardado)

    def update_pics(self,nombre_guardado):
        self.layout.removeWidget(self.audio_image)
        self.audio_image.deleteLater()
        self.audio_image = None
        self.update()
        self.preguntas_action(nombre_guardado)

    def preguntas_action(self,nombre_guardado):
        self.hide()
        self.sam_window = Pregunta_Uno()
        self.sam_window.nombre_cancion = nombre_guardado
        self.sam_window.iteracion_signal.connect(self.update_this_window)
        self.sam_window.show()
        
    def update_this_window(self):
        self.show()
        self.showMaximized()
        self.iteracion_signal.emit()
        self.band = True
        self.start_loop()
        return self.band

    def finish_protocol(self):
        self.hide()
        print("chao")
        self.adios = Adios()
        self.adios.show()
        self.adios.registro_signal.connect(self.jump_chao)
        self.close()

    def jump_chao(self):
        self.registro_signal.emit()

class Adios(QWidget):
    registro_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gracias por participar")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white"))
        self.setPalette(palette)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        self.showMaximized()
        self.adios_pic()

    def adios_pic(self):
        self.chao_image = QLabel()
        pixmap = QPixmap("archivos_relacionados/imagenes/chao.png").scaled(self.screen_width,self.screen_height,Qt.AspectRatioMode.KeepAspectRatio)
        self.chao_image.setPixmap(pixmap)
        self.chao_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.chao_image)  # Add the silence image to the layout
        self.update()
        self.adios_timer()

    def adios_timer(self):
        QTimer.singleShot(5000, self.chao_adios)

    def chao_adios(self):
        self.hide()
        self.registro_signal.emit()
        self.close()

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HolaPrueba()
    window.show()
    app.exec()   