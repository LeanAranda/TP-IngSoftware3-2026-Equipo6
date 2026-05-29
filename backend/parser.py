import re


# Regex que detecta el formato estándar de Android
PATRON_ANDROID = r'^(\d{1,2}/\d{1,2}/\d{2,4}),?\s(\d{1,2}:\d{2})\s-\s([^:]+):\s(.*)$'

# Regex que detecta el formato de iOS
PATRON_IOS = r'^\[(\d{1,2}/\d{1,2}/\d{2,4})[,\s]+(\d{1,2}:\d{2}(?::\d{2})?)\]\s([^:]+):\s(.*)$'

# Regex que detecta si una linea empieza con una fecha
PATRON_ES_FECHA = r'^\[?\d{1,2}/\d{1,2}/\d{2,4}'


def parsear_chat_desde_lineas(lineas_chat):
    """
    TAREA Cronograma : [1.2.2] Implementacion de Regex (Android vs ios)

    Recibe una lista de lineas extraidas del txt y devuelve una lista
    de diccionarios con las claves Fecha, Hora, Usuario y Mensaje.
    """

    datos_parseados = [] # Lista para guardar los mensajes estructurados
    mensaje_actual = None # Variable para acumular mensajes que se extienden en varias lineas

    for linea in lineas_chat:
        if linea is None:
            continue

        linea_texto = linea.strip()
        if not linea_texto:
            continue

        coincidencia_android = re.match(PATRON_ANDROID, linea_texto)
        coincidencia_ios = re.match(PATRON_IOS, linea_texto)

        if coincidencia_android:
            fecha, hora, usuario, texto = coincidencia_android.groups()
            mensaje_actual = {
                'Fecha': fecha,
                'Hora': hora,
                'Usuario': usuario,
                'Mensaje': texto,
            }
            datos_parseados.append(mensaje_actual)

        elif coincidencia_ios:
            fecha, hora, usuario, texto = coincidencia_ios.groups()

            # iOS a veces trae segundos, asi que normalizamos a hh:mm
            hora = hora[:5]

            mensaje_actual = {
                'Fecha': fecha,
                'Hora': hora,
                'Usuario': usuario,
                'Mensaje': texto,
            }
            datos_parseados.append(mensaje_actual)

    return datos_parseados
