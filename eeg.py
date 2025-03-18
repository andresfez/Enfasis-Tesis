
import numpy as np
import math
import pylsl
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from typing import List
import pandas as pd  # Importamos pandas para guardar los datos
import time  # Para manejar el tiempo de guardado

# Parámetros básicos para la ventana de gráficos
plot_duration = 5  # cuántos segundos de datos mostrar
update_interval = 60  # ms entre actualizaciones de pantalla
pull_interval = 500  # ms entre cada operación de pull
save_interval = 5  # guardar datos cada 5 segundos

class Inlet:
    def __init__(self, info: pylsl.StreamInfo):
        self.inlet = pylsl.StreamInlet(info, max_buflen=plot_duration,
                                       processing_flags=pylsl.proc_clocksync | pylsl.proc_dejitter)
        self.name = info.name()
        self.channel_count = info.channel_count()

    def pull_and_plot(self, plot_time: float, plt: pg.PlotItem):
        pass


class DataInlet(Inlet):
    dtypes = [[], np.float32, np.float64, None, np.int32, np.int16, np.int8, np.int64]

    def __init__(self, info: pylsl.StreamInfo, plt: pg.PlotItem):
        super().__init__(info)
        bufsize = (2 * math.ceil(info.nominal_srate() * plot_duration), info.channel_count())
        self.buffer = np.empty(bufsize, dtype=self.dtypes[info.channel_format()])
        empty = np.array([])
        self.curves = [pg.PlotCurveItem(x=empty, y=empty, autoDownsample=True) for _ in range(self.channel_count)]
        for curve in self.curves:
            plt.addItem(curve)

        # Buffer para almacenar datos antes de guardarlos
        self.data_buffer = []
        self.last_save_time = time.time()  # Para controlar el guardado periódico

    def pull_and_plot(self, plot_time, plt):
        # Pull data
        _, ts = self.inlet.pull_chunk(timeout=0.0,
                                      max_samples=self.buffer.shape[0],
                                      dest_obj=self.buffer)
        if ts:
            ts = np.asarray(ts)
            y = self.buffer[0:ts.size, :]

            # Almacenar los datos en el buffer
            for i in range(ts.size):
                self.data_buffer.append(np.hstack((ts[i], y[i, :])))  # Guardar timestamp y datos

            # Graficar los datos
            this_x = None
            old_offset = 0
            new_offset = 0
            for ch_ix in range(self.channel_count):
                old_x, old_y = self.curves[ch_ix].getData()
                if ch_ix == 0:
                    old_offset = old_x.searchsorted(plot_time)
                    new_offset = ts.searchsorted(plot_time)
                    this_x = np.hstack((old_x[old_offset:], ts[new_offset:]))
                this_y = np.hstack((old_y[old_offset:], y[new_offset:, ch_ix] - ch_ix))
                self.curves[ch_ix].setData(this_x, this_y)

            # Guardar datos periódicamente
            current_time = time.time()
            if current_time - self.last_save_time >= save_interval:
                self.save_data()
                self.last_save_time = current_time

    def save_data(self):
        if self.data_buffer:

            # Convertir el buffer a un DataFrame de pandas
            columns = ['timestamp'] + [f'channel_{i}' for i in range(self.channel_count)]
            df = pd.DataFrame(self.data_buffer, columns=columns)

            # Guardar el DataFrame en un archivo CSV
            filename = f"eeg_data_{time.strftime('%Y_%m_%d_%H_%M_%S')}.csv"
            df.to_csv(filename, index=False)
            print(f"Datos guardados en {filename}")

            # Limpiar el buffer
            self.data_buffer = []
        else:
            print("No hay datos en el buffer")


class MarkerInlet(Inlet):
    def __init__(self, info: pylsl.StreamInfo):
        super().__init__(info)

    def pull_and_plot(self, plot_time, plt):
        strings, timestamps = self.inlet.pull_chunk(0)
        if timestamps:
            for string, ts in zip(strings, timestamps):
                plt.addItem(pg.InfiniteLine(ts, angle=90, movable=False, label=string[0]))


def main():
    # Resolver todos los streams disponibles
    inlets: List[Inlet] = []
    print("Buscando streams...")
    streams = pylsl.resolve_streams()

    # Crear la ventana de pyqtgraph
    pw = pg.plot(title='LSL Plot')
    plt = pw.getPlotItem()
    plt.enableAutoRange(x=False, y=True)

    # Iterar sobre los streams encontrados y crear inlets
    for info in streams:
        if info.type() == 'Markers':
            if info.nominal_srate() != pylsl.IRREGULAR_RATE \
                    or info.channel_format() != pylsl.cf_string:
                print('Stream de marcadores inválido: ' + info.name())
            print('Añadiendo inlet de marcadores: ' + info.name())
            inlets.append(MarkerInlet(info))
        elif info.nominal_srate() != pylsl.IRREGULAR_RATE \
                and info.channel_format() != pylsl.cf_string:
            print('Añadiendo inlet de datos: ' + info.name())
            inlets.append(DataInlet(info, plt))
        else:
            print('No se sabe qué hacer con el stream: ' + info.name())

    def scroll():
        plot_time = pylsl.local_clock()
        fudge_factor = pull_interval * .002
        pw.setXRange(plot_time - plot_duration + fudge_factor, plot_time - fudge_factor)

    def update():
        mintime = pylsl.local_clock() - plot_duration
        for inlet in inlets:
            inlet.pull_and_plot(mintime, plt)

    # Temporizador para mover la vista
    update_timer = QtCore.QTimer()
    update_timer.timeout.connect(scroll)
    update_timer.start(update_interval)

    # Temporizador para actualizar los datos
    pull_timer = QtCore.QTimer()
    pull_timer.timeout.connect(update)
    pull_timer.start(pull_interval)

    # Iniciar la aplicación
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QGuiApplication.instance().exec()


if __name__ == '__main__':
    main()