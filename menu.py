from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtCharts import *
from ensayo import *
from prueba import *
from classes import *
#from main import *
import sys

class Menu(QWidget):
    registro_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.content_vmenu()
    
    def content_vmenu(self):
        self.setWindowTitle("Menu")
        self.setGeometry(100, 100, 300, 300)
        layout = QVBoxLayout()  # Layout vertical para los botones
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("white")) #color ventana
        self.setPalette(palette)
        
        # Botones:
        self.validation_button = self.create_button("Validar canales")
        self.start_demo_button = self.create_button("Iniciar Ensayo")
        self.start_test_button = self.create_button("Iniciar Prueba")
        self.end_test_button = self.create_button("Finalizar Prueba")

        layout.addWidget(self.validation_button)
        layout.addWidget(self.start_demo_button)
        layout.addWidget(self.start_test_button)        
        layout.addWidget(self.end_test_button)

        self.setLayout(layout)  # Establecer el layout principal para la ventana

        # Asignación de funciones de botones:
        self.validation_button.clicked.connect(self.goto_validacion)
        self.start_demo_button.clicked.connect(self.goto_ensayo)
        self.start_test_button.clicked.connect(self.goto_prueba)
        self.end_test_button.clicked.connect(self.goto_finalizar)

    def create_button(self, text):
        button = QPushButton(text)
        general_font = QFont("Arial", 14) #fuente usada
        button.setFont(general_font)
        return button            

    def goto_validacion(self):
        connector = Connector()
        ReceiveThread = threading.Thread(target=connector.print_dat)
        ReceiveThread.start()
        self.ChannelPlotWindow = ChannelPlot()
        self.ChannelPlotWindow.setConnector(connector)
        self.ChannelPlotWindow.show()

    def goto_ensayo(self):
        self.ensayo_window = HolaEnsayo() # Si no está abierta, crear una nueva instancia y mostrarla
        self.ensayo_window.show()

    def goto_prueba(self):
        self.conexion_window = HolaPrueba() # Si no está abierta, crear una nueva instancia y mostrarla
        self.conexion_window.registro_signal.connect(self.jump)
        self.conexion_window.show()

    def goto_finalizar(self):
        self.close()

    def jump(self):
        self.registro_signal.emit()

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Menu()
    window.show()
    sys.exit(app.exec())
