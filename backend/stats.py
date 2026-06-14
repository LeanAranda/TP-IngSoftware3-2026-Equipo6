import pandas as pd
import emoji 
import re
from collections import Counter

# Lista de emojis que usa WhatsApp para color de piel y género que queremos ignorar
modificadores_ignorar = ['🏻', '🏼', '🏽', '🏾', '🏿', '♂', '♀', '♂️', '♀️', '\ufe0f']

def calcular_estadisticas_usuarios(df):
    """
    Realiza un análisis cuantitativo integral sobre el DataFrame para obtener 
    métricas de participación, uso de emojis y tendencias temporales.

    TAREA WBS : [1.3.1] Recuento total de mensajes por usuario.
    TAREA WBS : [1.3.2] Buscar emoji más utilizado.
    TAREA WBS : [2.1.1] Calcular franja horaria con mayor actividad.
    TAREA WBS : [2.1.2] Calcular días con mayor cantidad de mensajes (días pico).
    TAREA WBS : [2.1.3] Recuento de palabras más frecuentes (Word Cloud).

    :param df: pd.DataFrame - DataFrame procesado que debe contener las columnas 
                'Usuario', 'Fecha', 'Hora' y 'Mensaje'.
    :return: dict - Diccionario con los resultados del análisis:
            - 'usuario_top' (str): Nombre del usuario con más mensajes.
            - 'grafico_usuarios' (dict): Top 5 de usuarios y su conteo de mensajes.
            - 'emojis' (list): Top 5 de emojis normalizados y su frecuencia.
            - 'horarios' (dict): Distribución de mensajes por franjas horarias.
            - 'dias_pico' (dict): Top 5 de fechas con mayor volumen de actividad.
            - 'nube_palabras' (list): Top 50 de palabras clave en formato para React 
            [{"text": p, "value": c}].
    :raises: ValueError - Si el DataFrame está vacío.
    :raises: KeyError - Si faltan columnas requeridas para los cálculos avanzados.
    """

    # 1. Validación preventiva de integridad
    columnas_requeridas = ['Usuario', 'Fecha', 'Hora', 'Mensaje']
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if df.empty:
        raise ValueError("El DataFrame está vacío. No hay datos para procesar.")
    
    if columnas_faltantes:
        # Informamos exactamente qué columnas faltan para una trazabilidad extrema
        raise KeyError(f"Faltan columnas necesarias en el chat: {', '.join(columnas_faltantes)}")
    
    # 2. Lógica Tarea [1.3.1]: Ranking de Usuarios
    ranking_usuarios = df['Usuario'].value_counts()
    user_mas_mensajes= ranking_usuarios.idxmax()

    # 3. Lógica Tarea [1.3.2]: Conteo de Emojis
    def extraer_emojis(texto):
        """ 
        Identifica secuencias completas de emojis y las unifica a su base
        eliminando modificadores de tono, género y selectores de variación.
        :param texto: str - El mensaje original del chat.
        :return: list - Lista de emojis (strings) normalizados.
        """
        # 1. Detecta el bloque completo (ej: '👩‍⚕️' o '👍🏾')
        lista_deteccion = emoji.emoji_list(str(texto))
    
        emojis_normalizados = []
        for item in lista_deteccion:
            # 2. Limpia los modificadores de ADENTRO de la secuencia detectada
            base = ''.join([c for c in item['emoji'] if c not in modificadores_ignorar])
            if base:
                emojis_normalizados.append(base)
            
        # CAMBIO CLAVE 1: Devolvemos una LISTA, no un string unido
        return emojis_normalizados
    
    # CAMBIO CLAVE 2: Creamos una lista plana con todos los emojis detectados
    todas_las_listas = df['Mensaje'].apply(extraer_emojis)
    lista_final_emojis = [emj for sublista in todas_las_listas for emj in sublista]

    # CAMBIO CLAVE 3: El Counter ahora recibe una LISTA de strings (unidades completas)
    conteo_emojis = Counter(lista_final_emojis)

    # Preparamos el formato específico para el frontend (top 5)
    top_emojis = [{"emoji": e[0], "cantidad": e[1]} for e in conteo_emojis.most_common(5)]

    # 4. Lógica Tarea [2.1.1]: Agrupación por franjas horarias
    # Extrae la hora pero convertida a NÚMERO (entero)
    df['Hora_Num'] = df['Hora'].apply(lambda x: int(x.split(':')[0]))
    
    # Define los "cortes" (bins) y las etiquetas
    # El -1 es  para que el rango incluya la hora 0 (la medianoche).
    # Los cortes son: de -1 a 6, de 6 a 12, de 12 a 19, y de 19 a 24.
    limites = [-1, 6, 12, 19, 24]
    nombres_rangos = ['Madrugada (00-06hs)', 'Mañana (07-12hs)', 'Tarde (13-19hs)', 'Noche (20-23hs)']
    
    # Se usa pd.cut para que Pandas clasifique cada fila automáticamente
    df['Rango_Horario'] = pd.cut(df['Hora_Num'], bins=limites, labels=nombres_rangos)

    # Ahora se cuentan los valores sobre esta nueva columna
    franjas_agrupadas = df['Rango_Horario'].value_counts()

    # 5. Lógica Tarea [2.1.2]: Días con mayor cantidad de mensajes
    # Guarda el dia con mas mensajes
    dias_mas_activos = df['Fecha'].value_counts()

    # 6. Lógica Tarea [2.1.3]: Conteo de palabras para la word cloud

    # 7. Paquete de retorno integrado

    # Junta todos los mensajes en un texto gigante
    texto_completo = " ".join(df['Mensaje'].dropna())
    # Pasa todo a minúsculas y extrae solo las palabras (se ignoran comas, puntos, emojis)
    # Esta expresión regular busca secuencias de letras (incluyendo acentos y ñ)
    palabras = re.findall(r'\b[a-záéíóúñ]+\b', texto_completo.lower())
    # Palabras que no aportan valor
    stopwords = {'que', 'de', 'la', 'el', 'en', 'y', 'a', 'los', 'se', 'del', 'las', 'un', 'por',
                'con', 'no', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'más', 'pero', 'sus',
                'le', 'ya', 'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin',
                'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos',
                'eso', 'te', 'si', 'multimedia', 'omitido', 'omitida', 'imagen', 'sticker', 'audio', 'documento'}
    # Filtra las stopwords y palabras muy cortitas (ej: "ja", "ah")
    palabras_limpias = [p for p in palabras if p not in stopwords and len(p) > 2]
    # Cuenta las frecuencias
    conteo_palabras = Counter(palabras_limpias)
    # Arma el formato que pide React (una lista de diccionarios)
    # Agarra el Top 50 para que la nube no sea muy extensa
    formato_react = [{"text": palabra, "value": cantidad} for palabra, cantidad in conteo_palabras.most_common(50)]

    return {
        "usuario_top": user_mas_mensajes,
        "grafico_usuarios": ranking_usuarios.head(5).to_dict(),
        "emojis": top_emojis,
        "horarios": franjas_agrupadas.to_dict(),
        "dias_pico": dias_mas_activos.head(5).to_dict(),
        "nube_palabras": formato_react
    }