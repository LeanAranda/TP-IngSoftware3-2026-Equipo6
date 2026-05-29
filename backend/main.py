from .reader import leer_chat_desde_zip

def procesar_chat_desde_zip(archivo_zip_memoria):
    """
    TAREA Cronograma : [1.2.1] Orquestación de lectura del chat

    Recibe el ZIP subido, delega la lectura en reader.py y
    devuelve las líneas extraídas para las siguientes tareas.
    """

    try:
        # Delegamos la lectura del ZIP en la capa de IO/reader
        lineas = leer_chat_desde_zip(archivo_zip_memoria)

    except FileNotFoundError as err:
        return str(err)
    
    for linea in lineas:
        print(linea)  # Aquí podríamos agregar más lógica de procesamiento si fuera necesario

    return lineas