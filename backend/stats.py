import pandas as pd

def calcular_estadisticas_usuarios(df):
    """
    TAREA WBS : [1.3.1] Recuento total de mensajes por usuario
    
    Realiza el análisis cuantitativo sobre el DataFrame para obtener el ranking 
    de participación y el usuario con mayor actividad.

    :param df: pd.DataFrame - DataFrame procesado que debe contener la columna 'Usuario'.
    :return: dict - Diccionario con 'usuario_top' y 'grafico_usuarios' (Top 5).
    :raises: ValueError - Si el DataFrame está vacío.
    :raises: KeyError - Si faltan las columnas requeridas para el cálculo.
    """

    # 1. Definimos las columnas que el módulo NECESITA para no fallar
    columnas_requeridas = ['Usuario', 'Fecha', 'Hora', 'Mensaje']

    # 2. Verificamos si el DataFrame está vacío o si le falta alguna columna
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if df.empty:
        raise ValueError("El DataFrame está vacío. No hay datos para procesar.")
    
    if columnas_faltantes:
        # Informamos exactamente qué columnas faltan para una trazabilidad extrema
        raise KeyError(f"Faltan columnas necesarias en el chat: {', '.join(columnas_faltantes)}")
    # 3. Obtener el ranking completo (Serie de Pandas)
    ranking_usuarios = df['Usuario'].value_counts()

    # 4. Identificamos al ganador (ID del valor máximo)
    user_mas_mensajes= ranking_usuarios.idxmax()

    # 5. Preparamos el "paquete" de retorno (convertimos a diccionario para JSON)

    return {
        "usuario_top": user_mas_mensajes,
        "grafico_usuarios": ranking_usuarios.head(5).to_dict()
    }