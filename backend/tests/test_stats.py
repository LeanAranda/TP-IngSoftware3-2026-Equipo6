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

    def test_comportamiento_emojis_compuestos_y_colores(self):
        """
        PRUEBA DE FUNDAMENTACIÓN:
        Verifica que el sistema identifique emojis complejos como una unidad
        y unifique los diferentes tonos de piel al emoji base.
        """
        # 1. Preparación de datos "ruidosos"
        data = {
            'Usuario': ['Ana', 'Pedro', 'Ana', 'Pedro'],
            'Mensaje': [
                'Pulgar oscuro 👍🏾',          # Secuencia: Base + Modificador piel
                'Pulgar claro 👍🏻',           # Secuencia: Base + Modificador piel
                'Familia ZWJ 👨‍👩‍👧‍👦',         # Secuencia: 4 emojis + 3 ZWJ
                'Corazón con estilo ❤️'     # Secuencia: Corazón + Selector Variación
            ],
            'Fecha': ['10/06/2026'] * 4,
            'Hora': ['10:00'] * 4
        }
        df = pd.DataFrame(data)
        
        # 2. Ejecución de la lógica de stats.py
        resultado = calcular_estadisticas_usuarios(df)
        ranking = resultado['emojis']
        
        # --- TEORÍA 1: UNIFICACIÓN DE COLORES ---
        # Los dos pulgares (oscuro y claro) deben sumar 2 en el emoji base '👍'
        pulgar_base = next(item for item in ranking if item["emoji"] == "👍")
        self.assertEqual(pulgar_base["cantidad"], 2, "Error: No se unificaron los tonos de piel al base.")

        # --- TEORÍA 2: UNIDAD DE EMOJIS COMPUESTOS ---
        # La familia debe contar como 1 unidad, no como 4 personas por separado
        familia = next(item for item in ranking if item["emoji"] == "👨‍👩‍👧‍👦")
        self.assertEqual(familia["cantidad"], 1, "Error: El emoji compuesto se fragmentó en caracteres individuales.")

        # --- TEORÍA 3: NORMALIZACIÓN DE SELECTORES ---
        # El corazón debe aparecer como el carácter base '❤' (sin el selector invisible)
        corazon = next(item for item in ranking if item["emoji"] == "❤")
        self.assertEqual(corazon["cantidad"], 1, "Error: El corazón no fue normalizado a su forma base.")

# Bloque condicional de ejecución para correr los tests
if __name__ == "__main__":
    unittest.main()