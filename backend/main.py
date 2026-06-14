from .reader import leer_chat_desde_zip
from .parser import parsear_chat_desde_lineas

def procesar_chat_desde_zip(archivo_zip_memoria):
    """
    TAREA Cronograma : [1.2.4] Exportación de datos

    Recibe el ZIP subido, delega la lectura en reader.py,
    luego delega el parseo en parser.py y devuelve el DataFrame final.
    """

    # Delegamos la lectura del ZIP en la capa de IO/reader
    lineas = leer_chat_desde_zip(archivo_zip_memoria)

    # Delegamos el parseo de las lineas en parser.py
    # Ahora el parser devuelve un DataFrame con los mensajes
    datos_chat = parsear_chat_desde_lineas(lineas)

    return datos_chat