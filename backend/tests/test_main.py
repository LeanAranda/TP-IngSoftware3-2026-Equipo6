import io
import zipfile
import unittest



from backend.main import procesar_chat_desde_zip

class TestMainProcesarChatDesdeZip(unittest.TestCase):
    def test_main_devuelve_lista_si_hay_txt(self):
        # Armamos un ZIP valido para confirmar que main orquesta reader y parser.
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, mode="w") as z:
            z.writestr("chat.txt", "12/05/2021, 15:30 - Alice: Hola\nEsto es una continuacion\n")

        memoria.seek(0)
        resultado = procesar_chat_desde_zip(memoria)

        # Main debe devolver exactamente una lista de diccionarios.
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['Fecha'], '12/05/2021')
        self.assertEqual(resultado[0]['Hora'], '15:30')
        self.assertEqual(resultado[0]['Usuario'], 'Alice')
        # La continuación se ignora en la versión actual de parser.py
        self.assertEqual(resultado[0]['Mensaje'], 'Hola')

    def test_main_lanza_error_si_falta_txt(self):
        # Armamos un ZIP sin .txt para validar el manejo de error en main
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, mode="w") as z:
            z.writestr("archivo.md", "Contenido irrelevante")

        memoria.seek(0)

        # Main debe propagar el error que viene de reader.py
        with self.assertRaises(FileNotFoundError) as error:
            procesar_chat_desde_zip(memoria)
        self.assertEqual(str(error.exception), "Error: No se encontró ningún archivo .txt en el ZIP")

if __name__ == "__main__":
    unittest.main()
