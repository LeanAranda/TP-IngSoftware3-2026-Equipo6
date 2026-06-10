import unittest

import pandas as pd

from backend.stats import calcular_estadisticas_usuarios

# Define una clase que hereda de unittest.TestCase
class TestStatsCalculos(unittest.TestCase):
    # Caso A: DataFrame sin datos pero con estructura correcta
    def test_falla_dataframe_vacio(self):
        columnas = ['Usuario', 'Fecha', 'Hora', 'Mensaje']
        df_vacio = pd.DataFrame(columns=columnas)
        with self.assertRaises(ValueError) as context:
            calcular_estadisticas_usuarios(df_vacio)
        self.assertEqual(str(context.exception), "El DataFrame está vacío. No hay datos para procesar.")
        
    # Caso B: Estructura de datos incorrecta
    def test_falla_columna_usuario_inexistente(self):
        df_error = pd.DataFrame({'Usuario': ['Alice'], 'Mensaje': ['Hola']})
        with self.assertRaises(KeyError) as context:
            calcular_estadisticas_usuarios(df_error)
        self.assertIn("Fecha", str(context.exception))
        self.assertIn("Hora", str(context.exception))

    def test_camino_feliz_ranking_correcto(self):
        data = {
            'Usuario': ['Alice', 'Alice', 'Bob'], 
            'Mensaje': ['m1', 'm2', 'm3'],
            'Fecha': ['12/05/2021', '12/05/2021', '12/05/2021'],
            'Hora': ['15:30', '15:31', '15:32']
        }
        df = pd.DataFrame(data)
        # Verifica tipos de datos 
        resultado = calcular_estadisticas_usuarios(df)
        # Compara valores
        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado['usuario_top'], 'Alice')
        self.assertEqual(resultado['grafico_usuarios']['Alice'], 2)

# Bloque condicional de ejecución para correr los tests
if __name__ == "__main__":
    unittest.main()