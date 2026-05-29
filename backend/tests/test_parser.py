import unittest

from backend.parser import parsear_chat_desde_lineas


class TestParserChatDesdeLineas(unittest.TestCase):
    def test_parsea_formato_android_con_concatenacion(self):
        # Preparamos lineas que simulan un chat exportado desde Android
        # En la versión actual de parser.py las líneas de continuación
        # se concatenan al mensaje anterior.
        lineas = [
            "12/05/2021, 15:30 - Alice: Hola",
            "Esto es una continuacion",
            "13/05/2021, 09:00 - Bob: Buen dia",
        ]

        resultado = parsear_chat_desde_lineas(lineas)

        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['Fecha'], '12/05/2021')
        self.assertEqual(resultado[0]['Hora'], '15:30')
        self.assertEqual(resultado[0]['Usuario'], 'Alice')
        # La continuación se concatena al mensaje anterior.
        self.assertEqual(resultado[0]['Mensaje'], 'Hola Esto es una continuacion')
        self.assertEqual(resultado[1]['Usuario'], 'Bob')

    def test_parsea_formato_ios(self):
        # Preparamos lineas que simulan un chat exportado desde iOS
        lineas = [
            "[12/05/2021 15:30:22] Alice: Hola desde iOS",
            "[13/05/2021 09:00] Bob: Buen dia",
        ]

        resultado = parsear_chat_desde_lineas(lineas)

        # El parser devuelve una lista de diccionarios.
        # iOS debe normalizar la hora a hh:mm.
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['Hora'], '15:30')
        self.assertEqual(resultado[1]['Usuario'], 'Bob')

    def test_ignora_lineas_sistema_que_empiezan_con_fecha(self):
        # Las lineas de sistema de WhatsApp no deben convertirse en mensajes.
        # El resultado esperado sigue siendo una lista de diccionarios.
        lineas = [
            "12/05/2021, 15:30 - Alice: Hola",
            "12/05/2021, 15:31 - Alice agregó a Bob",
            "12/05/2021, 15:32 - Bob: Respuesta",
        ]

        resultado = parsear_chat_desde_lineas(lineas)

        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]['Usuario'], 'Alice')
        self.assertEqual(resultado[1]['Usuario'], 'Bob')
