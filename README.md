# Enfasis-Tesis
Este repositorio contiene los códigos utilizados en el desarrollo de mi Énfasis/Tesis. 

## Descripción del Proyecto
El sistema implementado está diseñado para la recopilación de datos EEG durante la reproducción de pistas musicales y la evaluación de respuestas subjetivas de los participantes. La arquitectura consta de múltiples módulos interconectados, los cuales se detallan a continuación.

## Estructura del Código

### Archivos principales

- **registro.py**  
  - Gestiona el registro de los participantes.  
  - Guarda los datos en un archivo CSV.  
  - Una vez finalizado, redirige a `menu.py`.

- **menu.py**  
  - Interfaz principal de la aplicación.  
  - Opciones disponibles:
    - **Validar canales** (pendiente de implementación con hilos).  
    - **Iniciar Ensayo**: Redirige a `ensayo.py`.  
    - **Iniciar Prueba**: Redirige a `prueba.py`.  
    - **Finalizar Prueba**: Cierra el menú y retorna a `registro.py`.

- **ensayo.py**  
  - Ejecuta un ensayo sin registro de datos EEG.  
  - Finaliza redirigiendo nuevamente a `menu.py`.

- **prueba.py**  
  - Controla el protocolo de reproducción de pistas musicales.  
  - Recoge datos EEG (actualmente inactivo por falta de implementación de hilos).  
  - Tras cada iteración, redirige a `preguntas.py` para registrar las respuestas del participante.

- **preguntas.py**  
  - Recoge respuestas de los participantes tras cada pista musical.  
  - Guarda la información en relación con cada canción.  
  - Tras la última pregunta, retorna a `registro.py`.

- **eeg.py**  
  - Implementación de la recepción de datos EEG (sin integración actual con la API).  
  - Funciona de manera paralela a `prueba.py`, pero aún no está activo.  
  - Incluye funcionalidad para almacenar datos en CSV periódicamente.

## Requisitos
Para ejecutar este proyecto, asegúrate de contar con las siguientes librerías instaladas:

```bash
pip install numpy pandas pyqt6 pylsl sounddevice librosa
