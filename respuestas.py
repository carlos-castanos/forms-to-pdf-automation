# =========================
# Leer un excel generado por el formulario de Google Forms 
# y convertirlo en un diccionario organizado por ID de publicador
# =========================


import pandas as pd


def leer_respuestas(archivo):

    df = pd.read_excel(archivo)

    respuestas = {}

    for columna in df.columns:

        if columna == "Marca temporal":
            continue

        partes = columna.split(" - ")

        id_publicador = partes[0]
        campo = partes[1]

        if id_publicador not in respuestas:
            respuestas[id_publicador] = {}

        valor = df.loc[0, columna]

        respuestas[id_publicador][campo] = valor

    return respuestas