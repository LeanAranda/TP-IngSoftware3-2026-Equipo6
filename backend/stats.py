import pandas as pd
import emoji 
from collections import Counter

# Lista de emojis que usa WhatsApp para color de piel y género que queremos ignorar
modificadores_ignorar = ['🏻', '🏼', '🏽', '🏾', '🏿', '♂', '♀', '♂️', '♀️', '\ufe0f']

def calcular_estadisticas_usuarios(df):
    """
    TAREA WBS : [1.3.1] Recuento total de mensajes por usuario.
    TAREA WBS : [1.3.2] Buscar emoji más utilizado.
    TAREA WBS: [2.1.1] Calcular franja horaria con mayor actividad.
    TAREA WBS: [2.1.2] Calcular días con mayor cantidad de mensajes (días pico).
    Realiza el análisis cuantitativo sobre el DataFrame para obtener el ranking 
    de participación y el usuario con mayor actividad y el top de emojis utilizados.

    :param df: pd.DataFrame - DataFrame procesado que debe contener la columna 'Usuario'.
    :return: dict - Diccionario con 'usuario_top' y 'grafico_usuarios' (Top 5) y 'emojis'.
    :raises: ValueError - Si el DataFrame está vacío.
    :raises: KeyError - Si faltan las columnas requeridas para el cálculo.
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

    # 6. Paquete de retorno integrado

    return {
        "usuario_top": user_mas_mensajes,
        "grafico_usuarios": ranking_usuarios.head(5).to_dict(),
        "emojis": top_emojis,
        "horarios": franjas_agrupadas.to_dict(),
        "dias_pico": dias_mas_activos.head(5).to_dict()
    }