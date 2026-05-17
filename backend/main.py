from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import re
import pandas as pd
import emoji
from collections import Counter

# Inicializamos la API
app = FastAPI()

# Permisos para que React se pueda conectar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista de emojis que usa WhatsApp para color de piel y género que queremos ignorar
modificadores_ignorar = ['🏻', '🏼', '🏽', '🏾', '🏿', '♂', '♀', '♂️', '♀️']

def procesar_chat_desde_zip(archivo_zip_memoria):
    datos_parseados = []
    
    # Este Regex captura el formato estándar de Android (dd/mm/yy, hh:mm - Usuario: Mensaje)
    # Android (con la coma opcional que vimos antes)
    patron_android = r'^(\d{1,2}/\d{1,2}/\d{2,4}),?\s(\d{1,2}:\d{2})\s-\s([^:]+):\s(.*)$' 

    # iOS (Atrapa los corchetes, ignora la falta de guion, y agarra la hora con o sin segundos)
    patron_ios = r'^\[(\d{1,2}/\d{1,2}/\d{2,4})[,\s]+(\d{1,2}:\d{2}(?::\d{2})?)\]\s([^:]+):\s(.*)$'
    
    # detecta si la línea arranca con una fecha
    patron_es_fecha = r'^\[?\d{1,2}/\d{1,2}/\d{2,4}'
    
    # Usa el archivo que pasa FastAPI en memoria
    with zipfile.ZipFile(archivo_zip_memoria, 'r') as archivo_zip: 
        # Encuentra el archivo de texto dentro del zip
        archivos_txt = [nombre for nombre in archivo_zip.namelist() if nombre.endswith('.txt')]
        
        if not archivos_txt:
            return pd.DataFrame() # Devuelve un DataFrame vacío si hay error
            
        nombre_txt = archivos_txt[0]
        
        # Abre el txt en memoria
        with archivo_zip.open(nombre_txt) as chat_file:
            mensaje_actual = None
            
            for linea in chat_file:
                # decodificar los archivos dentro del zip
                linea_texto = linea.decode('utf-8').strip()
                
                coincidencia_android = re.match(patron_android, linea_texto)
                coincidencia_ios = re.match(patron_ios, linea_texto)
                
                if coincidencia_android:
                    fecha, hora, usuario, texto = coincidencia_android.groups()
                    mensaje_actual = {'Fecha': fecha, 'Hora': hora, 'Usuario': usuario, 'Mensaje': texto}
                    datos_parseados.append(mensaje_actual)
        
                elif coincidencia_ios:
                    fecha, hora, usuario, texto = coincidencia_ios.groups()
                    
                    # Como iOS a veces trae segundos (ej: 15:30:22), lo recortamos para 
                    # que te quede igual que Android (15:30) y no te rompa las franjas horarias luego.
                    hora = hora[:5] 
                    
                    mensaje_actual = {'Fecha': fecha, 'Hora': hora, 'Usuario': usuario, 'Mensaje': texto}
                    datos_parseados.append(mensaje_actual)
                else:
                    ## Si no coincidió con el regex principal, ¿es basura o es un "Enter"?
                    if re.match(patron_es_fecha, linea_texto):
                        # Si la línea empieza con fecha pero cayó acá,
                        # es un mensaje del sistema de WhatsApp.
                        # Ponemos 'pass' para ignorarlo y que no sume emojis falsos.
                        pass
                    elif mensaje_actual and linea_texto:
                        # Si NO empieza con fecha, es la continuación real de un mensaje largo
                        mensaje_actual['Mensaje'] += f" {linea_texto}"
                        
    # Convierte la lista de diccionarios en un DataFrame
    df_chat = pd.DataFrame(datos_parseados)
    return df_chat


# --- ENDPOINT ---
@app.post("/api/analizar")
async def analizar(archivo: UploadFile = File(...)):
    
    # Procesa el dataSet para leerlo (usando el archivo que sube el usuario)
    df = procesar_chat_desde_zip(archivo.file)

    if df.empty:
        return {"error": "No se pudo procesar el archivo zip"}

    # Cuenta los mensajes por usuario y muestra los 5 primeros
    ranking_usuarios = df['Usuario'].value_counts()

    # Nombre del usuario que mas mensajes envio:
    user_mas_mensajes = ranking_usuarios.idxmax()

    # Guarda el dia con mas mensajes
    dias_mas_activos = df['Fecha'].value_counts()

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

    # Extrae todos los emojis de la columna de mensajes
    def extraer_emojis(texto):
        # Primero se sacan todos los caracteres que sean emojis
        emojis_encontrados = [c for c in str(texto) if c in emoji.EMOJI_DATA]
        # Luego se dejan solo los que NO sean modificadores
        emojis_filtrados = [e for e in emojis_encontrados if e not in modificadores_ignorar]
        return ''.join(emojis_filtrados)
        
    # Se aplica la función a nuestra columna
    df['Emojis'] = df['Mensaje'].apply(extraer_emojis)
    # Junta todos los emojis en un solo texto gigante y los cuenta
    todos_los_emojis = ''.join(df['Emojis'])
    conteo_emojis = Counter(todos_los_emojis)

    # Conteo de palabras para la word cloud
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

    # --- RESPUESTA JSON FINAL  ---
    return {
        "usuario_top": user_mas_mensajes,
        "grafico_usuarios": ranking_usuarios.head(5).to_dict(),
        "dias_pico": dias_mas_activos.head(5).to_dict(),
        "horarios": franjas_agrupadas.to_dict(),
        "emojis": [{"emoji": e[0], "cantidad": e[1]} for e in conteo_emojis.most_common(5)],
        "nube_palabras": formato_react
    }