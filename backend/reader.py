import zipfile # Librería para manipular archivos zip en memoria

def leer_chat_desde_zip(archivo_zip_memoria):
    """
    TAREA Cronograma : [1.2.1] Lectura del chat exportado
    
    Abre un archivo ZIP en memoria, busca el primer .txt disponible
    y extrae sus líneas decodificadas.

    :param archivo_zip_memoria: objeto del archivo ZIP subido.
    :return: list - Una lista con las líneas de texto del chat.
    :raises: FileNotFoundError si el ZIP no contiene archivo.txt.
    """

    # Asegurarnos de poder volver al inicio 
    try: 
        archivo_zip_memoria.seek(0)
    except Exception:
        pass

    # Validación explicita de ZIP
    if not zipfile.is_zipfile(archivo_zip_memoria):
        raise zipfile.BadZipFile("Error: El archivo proporcionado no es un ZIP válido")

    lineas_extraidas = []

    # 1. Abrimos el ZIP usando ´with´ para que sea una operación segura
    with zipfile.ZipFile(archivo_zip_memoria, 'r') as archivo_zip: 
        # 2. Buscamos qué archivos hay dentro que terminen en ".txt"
        #Esto se llama "comprensión de listas", una forma rápida de filtrar en python
        archivos_txt = [nombre for nombre in archivo_zip.namelist() if nombre.endswith('.txt')]
        
        # Si no encontramos ningúnn .txt, avisamos que hay un errror
        if not archivos_txt:
            raise FileNotFoundError("Error: No se encontró ningún archivo .txt en el ZIP")
        
        # 3. Tomamos el primer archivo de texto encontrado
        nombre_txt = archivos_txt[0]

        # Abrimos ese archivo especifico para leer su contenido
        with archivo_zip.open(nombre_txt) as chat_file:

            #Recorremos el archivo liena por linea
            for linea in chat_file:
                # Decodificamos el texto (pasarlo de bytes a letras legibles)
                # .strip() quita los espacios vacíos al principio y final
                lineas_extraidas.append(linea.decode('utf-8').strip())
    return lineas_extraidas
