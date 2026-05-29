import io
import zipfile
import unittest

from backend.reader import leer_chat_desde_zip

class TestProcesarChatDesdeZip(unittest.TestCase):
    def test_error_si_no_hay_txt_en_zip(self):
        # Creamos un ZIP en memoria que no contiene archivos .txt
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, mode="w") as z:
            z.writestr("archivo.md", "Contenido irrelevante")

        memoria.seek(0)

        # Esperamos que reader lance error cuando no haya .txt
        with self.assertRaises(FileNotFoundError) as error:
            leer_chat_desde_zip(memoria)
        self.assertEqual(str(error.exception), "Error: No se encontró ningún archivo .txt en el ZIP")

    def test_lectura_correcta_del_txt_en_zip(self):
        # Creamos un ZIP en memoria con un archivo chat.txt
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, mode="w") as z:
            z.writestr("chat.txt", "Hola\nLinea2\n")

        memoria.seek(0)

        # Reader devuelve las líneas como lista para tareas siguientes
        resultado = leer_chat_desde_zip(memoria)
        self.assertEqual(resultado, ["Hola", "Linea2"])

    def test_levanta_badzipfile_si_no_es_zip(self):
        memoria = io.BytesIO(b"no es un zip")
        with self.assertRaises(zipfile.BadZipFile) as ctx:
            leer_chat_desde_zip(memoria)
        self.assertEqual(str(ctx.exception), "Error: El archivo proporcionado no es un ZIP válido")

if __name__ == "__main__":
    unittest.main()