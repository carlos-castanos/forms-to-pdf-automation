import os

from pypdf import PdfReader


# =========================
# LOCALIZAR PDF
# =========================

def localizar_pdf(datos, carpeta_pdfs):

    archivo_pdf = datos["ARCHIVO_PDF"]

    ruta_pdf = os.path.join(carpeta_pdfs, archivo_pdf)

    if os.path.exists(ruta_pdf):
        return ruta_pdf

    return None


# =========================
# MESES
# =========================

MESES = {
    "SEPTIEMBRE": 20,
    "OCTUBRE": 21,
    "NOVIEMBRE": 22,
    "DICIEMBRE": 23,
    "ENERO": 24,
    "FEBRERO": 25,
    "MARZO": 26,
    "ABRIL": 27,
    "MAYO": 28,
    "JUNIO": 29,
    "JULIO": 30,
    "AGOSTO": 31
}


# =========================
# OBTENER CAMPOS DEL MES
# =========================

def obtener_campos_mes(mes):

    mes = mes.upper()

    if mes not in MESES:
        raise ValueError(f"Mes no válido: {mes}")

    indice = MESES[mes]

    campos = {
        "participacion": f"901_{indice}_CheckBox",
        "cursos": f"902_{indice}_Text_C_SanSerif",
        "precursor_auxiliar": f"903_{indice}_CheckBox",
        "horas": f"904_{indice}_S21_Value",
        "notas": f"905_{indice}_Text_SanSerif"
    }

    return campos

def preparar_datos_pdf(datos, campos):

    es_pa = determinar_precursor_auxiliar(datos)

    valores = {
        campos["participacion"]:
            datos["Participó en el ministerio"],

        campos["cursos"]:
            datos["Cursos bíblicos"],

        campos["precursor_auxiliar"]:
            "Sí" if es_pa else "No",    

        campos["horas"]:
            datos["Horas de servicio"],

        campos["notas"]:
            datos["Notas"]
    }

    return valores

import pandas as pd


def normalizar_valores_pdf(valores):

    valores_normalizados = {}

    for campo, valor in valores.items():

        # Casillas de participación y precursor auxiliar
        if campo.startswith("901_") or campo.startswith("903_"):

            if valor == "Sí":
                valores_normalizados[campo] = "/Yes"
            else:
                valores_normalizados[campo] = "/Off"

        # Campos vacíos
        elif pd.isna(valor):

            valores_normalizados[campo] = ""

        # Cualquier otro valor
        else:

            valores_normalizados[campo] = str(valor)

    return valores_normalizados


from pypdf import PdfReader, PdfWriter


def escribir_campos_pdf(ruta_pdf, valores):

    reader = PdfReader(ruta_pdf)
    writer = PdfWriter()

    writer.clone_document_from_reader(reader)

    writer.update_page_form_field_values(
        writer.pages[0],
        valores,
        auto_regenerate=False
    )

    with open(ruta_pdf, "wb") as archivo:
        writer.write(archivo)



def determinar_precursor_auxiliar(datos):

    horas = datos["Horas de servicio"]
    tipo = datos["TIPO"]

    if pd.isna(horas):
        return False

    if tipo == "REG":
        return False

    return True


# =========================
# CALCULAR TOTAL DE HORAS
# =========================

def calcular_total_horas(ruta_pdf):

    reader = PdfReader(ruta_pdf)

    campos = reader.get_fields()

    total = 0

    for indice in range(20, 32):

        nombre_campo = f"904_{indice}_S21_Value"

        valor = campos.get(nombre_campo, {}).get("/V")

        if valor not in (None, ""):

            try:
                total += float(valor)
            except (ValueError, TypeError):
                pass

    return total

# =========================
# ACTUALIZAR TOTAL DE HORAS
# =========================

def escribir_total_horas(ruta_pdf, total):

    reader = PdfReader(ruta_pdf)

    writer = PdfWriter()

    writer.clone_document_from_reader(reader)

    campos = {
        "904_32_S21_Value": str(int(total))
    }

    writer.update_page_form_field_values(
        writer.pages[0],
        campos
    )

    with open(ruta_pdf, "wb") as archivo:
        writer.write(archivo)