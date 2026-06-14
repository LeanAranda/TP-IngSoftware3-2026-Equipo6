import io
import zipfile
import unittest

import pandas as pd


from backend.main import procesar_chat_desde_zip
from backend.stats import calcular_estadisticas_usuarios

class TestMainProcesarChatDesdeZip(unittest.TestCase):
    def test_main_parsea_zip_con_txt_y_devuelve_dataframe_con_concatenacion(self):
        # Armamos un ZIP valido para confirmar que main orquesta reader y parser.
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, mode="w") as z:
            z.writestr("chat.txt", "12/05/2021, 15:30 - Alice: Hola\nEsto es una continuacion\n")

        memoria.seek(0)
        resultado = procesar_chat_desde_zip(memoria)

        # Main debe devolver el DataFrame generado por parser.py.
        self.assertIsInstance(resultado, pd.DataFrame)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado.loc[0, 'Fecha'], '12/05/2021')
        self.assertEqual(resultado.loc[0, 'Hora'], '15:30')
        self.assertEqual(resultado.loc[0, 'Usuario'], 'Alice')
        self.assertEqual(resultado.loc[0, 'Mensaje'], 'Hola Esto es una continuacion')

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

    def test_main_error_estadisticas_vacias(self):
        # 1. Creamos un ZIP con un txt que no tiene mensajes válidos para generar estadísticas
        memoria = io.BytesIO()
        with zipfile.ZipFile(memoria, mode="w") as z:
            z.writestr("chat.txt", "Línea sin formato válido\nOtra línea sin formato")
        memoria.seek(0)

        resultado = procesar_chat_desde_zip(memoria)

        # 2. Main debe lanzar un error al intentar calcular estadísticas con un DataFrame vacío
        with self.assertRaises(ValueError) as error:
            calcular_estadisticas_usuarios(resultado)
        self.assertEqual(str(error.exception), "El DataFrame está vacío. No hay datos para procesar.")

    def test_main_error_columnas__faltante(self):
        # Simulamos un DataFrame que no tiene la columna 'Usuario'
        df_incompleto = pd.DataFrame({'Usuario': ['Alice'], 'Mensaje': ['Hola']})
        
        # Al intentar calcular estadísticas, debería lanzar KeyError

        with self.assertRaises(KeyError) as error:
            calcular_estadisticas_usuarios(df_incompleto)
        self.assertIn("Fecha", str(error.exception))
        self.assertIn("Hora", str(error.exception))

if __name__ == "__main__":
    unittest.main()
