# =========================
# Leer la informacion permanente de los publicadores desde un excel
# =========================


import pandas as pd


def leer_lista_maestra(archivo):

    df = pd.read_excel(archivo)

    publicadores = {}

    for _, fila in df.iterrows():

        id_publicador = fila["ID"]

        publicadores[id_publicador] = {
            "NOMBRE": fila["NOMBRE"],
            "PRIVILEGIO": fila["PRIVILEGIO"],
            "TIPO": fila["PUB. / PREC."],
            "GRUPO": fila["GRUPO"],
            "ARCHIVO_PDF": fila["ARCHIVO_PDF"],
            "ESTADO": fila["ESTADO"]
        }

    return publicadores