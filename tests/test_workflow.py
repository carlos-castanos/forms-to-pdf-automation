import unittest

import pandas as pd

from datos_publicadores import combinar_publicador
from pdf import (
    determinar_precursor_auxiliar,
    normalizar_valores_pdf,
    obtener_campos_mes,
)


class WorkflowTests(unittest.TestCase):
    def test_combina_datos_de_referencia_y_respuestas(self):
        respuestas = {
            "A001": {
                "Horas de servicio": 8,
                "Notas": "Ejemplo",
            }
        }
        referencia = {
            "A001": {
                "NOMBRE": "Persona de prueba",
                "TIPO": "REG",
                "GRUPO": 1,
            }
        }

        resultado = combinar_publicador(respuestas, referencia)

        self.assertEqual(resultado["A001"]["NOMBRE"], "Persona de prueba")
        self.assertEqual(resultado["A001"]["Horas de servicio"], 8)
        self.assertEqual(resultado["A001"]["TIPO"], "REG")

    def test_obtiene_identificadores_de_campos_del_mes(self):
        campos = obtener_campos_mes("SEPTIEMBRE")

        self.assertEqual(campos["participacion"], "901_20_CheckBox")
        self.assertEqual(campos["cursos"], "902_20_Text_C_SanSerif")
        self.assertEqual(campos["horas"], "904_20_S21_Value")

    def test_rechaza_mes_no_configurado(self):
        with self.assertRaises(ValueError):
            obtener_campos_mes("MES_INVENTADO")

    def test_normaliza_valores_de_casillas_y_campos_vacios(self):
        valores = {
            "901_20_CheckBox": "Sí",
            "903_20_CheckBox": "No",
            "902_20_Text_C_SanSerif": pd.NA,
            "904_20_S21_Value": 12,
        }

        resultado = normalizar_valores_pdf(valores)

        self.assertEqual(resultado["901_20_CheckBox"], "/Yes")
        self.assertEqual(resultado["903_20_CheckBox"], "/Off")
        self.assertEqual(resultado["902_20_Text_C_SanSerif"], "")
        self.assertEqual(resultado["904_20_S21_Value"], "12")

    def test_determina_clasificacion_auxiliar_segun_reglas_actuales(self):
        self.assertFalse(
            determinar_precursor_auxiliar(
                {"Horas de servicio": pd.NA, "TIPO": "PUB"}
            )
        )
        self.assertFalse(
            determinar_precursor_auxiliar(
                {"Horas de servicio": 5, "TIPO": "REG"}
            )
        )
        self.assertTrue(
            determinar_precursor_auxiliar(
                {"Horas de servicio": 5, "TIPO": "PUB"}
            )
        )


if __name__ == "__main__":
    unittest.main()
