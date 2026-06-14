import zipfile

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from reader import leer_chat_desde_zip
from parser import parsear_chat_desde_lineas
from stats import calcular_estadisticas_usuarios

# Inicializamos la API
app = FastAPI()

# Permisos para que React se pueda conectar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def procesar_chat_desde_zip(archivo_zip_memoria):
    """
    TAREA Cronograma : [1.2.4] Exportación de datos
    
    Orquestador de la Fase 1. Coordina la lectura del ZIP y el parseo de 
    líneas para consolidar el DataFrame inicial.

    :param archivo_zip_memoria: BinaryIO - Objeto de archivo ZIP recibido por la API.
    :return: pd.DataFrame - El set de datos listo para la fase de cálculos.
    """

    # Delegamos la lectura del ZIP en la capa de IO/reader
    lineas = leer_chat_desde_zip(archivo_zip_memoria)

    # Delegamos el parseo de las lineas en parser.py
    # Ahora el parser devuelve un DataFrame con los mensajes
    datos_chat = parsear_chat_desde_lineas(lineas)

    return datos_chat

@app.post("/api/analizar")
async def analizar(archivo: UploadFile = File(...)):
    """
    Punto de entrada de la API que integra todas las fases del sistema.
    Realiza la captura de excepciones para garantizar la calidad externa.

    :param archivo: UploadFile - Archivo .zip subido desde el frontend (React).
    :return: dict - Estadísticas finales en formato JSON o mensaje de error descriptivo.
    """
    
    try:
        # 1. Fase de Lectura y Parseo (tarea 1.2.1 a 1.2.4)
        df = procesar_chat_desde_zip(archivo.file)

        # 2. Fase de Cálculos (Tarea 1.3.1)
        estadisticas_usuarios = calcular_estadisticas_usuarios(df)

        return estadisticas_usuarios
    except (FileNotFoundError, zipfile.BadZipFile) as e:
        # Usamos 400 Bad Request porque el problema es el archivo que envió el usuario.
        # Conservamos tu mensaje descriptivo original a través de str(e).
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except (ValueError, KeyError) as e:
        # Usamos 422 Unprocessable Entity cuando el archivo es un ZIP válido 
        # pero los datos internos no permiten realizar los cálculos (ej: faltan columnas).
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error al procesar estadísticas: {str(e)}"
        )
    except Exception as e:
        # Usamos 500 para cualquier otro error no previsto en la lógica del servidor.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al procesar los datos."
        )