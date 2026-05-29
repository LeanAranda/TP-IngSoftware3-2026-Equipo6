import io
import zipfile
import unittest

from backend.main import procesar_chat_desde_zip

class TestMainProcesarChatDesdeZip(unittest.TestCase):
    def test_main_devuelve_error_si_falta_txt(self):
        # Armamos un ZIP sin .txt para validar el manejo de error en main
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, mode="w") as z:
            z.writestr("archivo.md", "Contenido irrelevante")

        memoria.seek(0)
        resultado = procesar_chat_desde_zip(memoria)

        # Main debe devolver el mensaje generado por la capa reader
        self.assertEqual(resultado, "Error: No se encontró ningún archivo .txt en el ZIP")

    def test_main_devuelve_lineas_si_hay_txt(self):
        # Armamos un ZIP válido para confirmar el flujo feliz
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, mode="w") as z:
            z.writestr("chat.txt", "Hola\nLinea2\n")

        memoria.seek(0)
        resultado = procesar_chat_desde_zip(memoria)

        # Main propaga la lista para el próximo módulo del cronograma
        self.assertEqual(resultado, ["Hola", "Linea2"])

if __name__ == "__main__":
    unittest.main()
