# Enfasis-Tesis
Códigos que usé para mi Énfasis/Tesis

(03/18/2025) V.1 codes:
  - registro.py
    - guarda los datos de registro de cada participante.
    - finalizado, avanza a "menu.py"
  - menu.py (sin funcion de hilos)
    - menu de la API:
      - Validar canales (inactivo; sin funcion de hilos): ir a "eeg.py"
      - Iniciar Ensayo: ir a "ensayo.py"
      - Iniciar Prueba: ir a "prueba.py"
      - Finalizar Prueba: cerrar menu, acabar prueba, ir a "registro.py"
  - ensayo.py
    - permite ensayo, no guarda datos EEG
    - al finalizar, vuelve a "menu.py"
  - prueba.py
    - protocolo de reproducción de pistas musicals + toma de datos EEG (inactivo; sin funcion de hilos)
    - por cada iteración, al acabar ir a "preguntas.py"
    - guarda los datos EEG (inactivo; sin funcion de hilos)
  - preguntas.py
    - toma datos con respecto a preguntas
    - guarda datos de preguntas en relación al participante y a la canción previa
    - al finalizar el proceso con la última canción, vuelve a "registro.py"
  - eeg.py (sin implementar a la API)
    - funcion que recibe datos EEG (inactiva)
    - funciona al mismo tiempo que "prueba.py"
    
