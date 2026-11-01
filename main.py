# =========================
# Este programa unicamente llama a las funciones de los otros archivos
# para leer, combinar y procesar la información.
# =========================

# =========================
# CONFIGURACIÓN DEL PROCESO
# =========================

import shutil
from pathlib import Path

MES = "SEPTIEMBRE"
AÑO = 2026

GRUPOS = [1, 2, 3, 4, 5]

# Store processed PDFs separately to preserve the originals.
CARPETA_SALIDA = Path("output")
CARPETA_SALIDA.mkdir(parents=True, exist_ok=True)


# =========================
# IMPORTAR FUNCIONES
# =========================

from respuestas import leer_respuestas
from lista_maestra import leer_lista_maestra
from datos_publicadores import combinar_publicador

from pdf import (
    localizar_pdf,
    obtener_campos_mes,
    preparar_datos_pdf,
    normalizar_valores_pdf,
    escribir_campos_pdf,
    calcular_total_horas,
    escribir_total_horas
)


# =========================
# CONFIGURACIÓN DEL MES
# =========================

NUMERO_MESES = {
    "ENERO": 1,
    "FEBRERO": 2,
    "MARZO": 3,
    "ABRIL": 4,
    "MAYO": 5,
    "JUNIO": 6,
    "JULIO": 7,
    "AGOSTO": 8,
    "SEPTIEMBRE": 9,
    "OCTUBRE": 10,
    "NOVIEMBRE": 11,
    "DICIEMBRE": 12
}

numero_mes = NUMERO_MESES[MES]

carpeta_mes = f"datos/{AÑO}-{numero_mes:02d}"


# =========================
# LEER LISTA MAESTRA
# =========================

archivo_maestra = "datos/Lista maestra publicadores.xlsx"

publicadores = leer_lista_maestra(
    archivo_maestra
)


# =========================
# OBTENER CAMPOS DEL MES
# =========================

campos_mes = obtener_campos_mes(MES)


# =========================
# CONTADORES GENERALES
# =========================

actualizados = 0
errores = 0
pdf_no_encontrados = 0


# =========================
# PROCESAR LOS 5 GRUPOS
# =========================

for grupo in GRUPOS:

    print()
    print("========================================")
    print(f"PROCESANDO GRUPO {grupo}")
    print("========================================")

    archivo_respuestas = (
        f"{carpeta_mes}/GRUPO {grupo} {MES}.xlsx"
    )

    try:

        # -------------------------
        # LEER RESPUESTAS
        # -------------------------

        respuestas = leer_respuestas(
            archivo_respuestas
        )

        # -------------------------
        # COMBINAR INFORMACIÓN
        # -------------------------

        datos_completos = combinar_publicador(
            respuestas,
            publicadores
        )

        print(
            "Publicadores encontrados:",
            len(datos_completos)
        )

        # -------------------------
        # PROCESAR PUBLICADORES
        # -------------------------

        for id_publicador in datos_completos:

            print()
            print("Procesando:", id_publicador)

            try:

                datos = datos_completos[
                    id_publicador
                ]

                # 1. Localizar PDF

                ruta_pdf = localizar_pdf(
                    datos,
                    "pdfs 2027"
                )

                if ruta_pdf is None:

                    print("❌ PDF no encontrado")

                    pdf_no_encontrados += 1

                    continue

                # Crear una copia funcional  para que los PDFs originales se mantengan sin cambios.
                ruta_pdf_salida = CARPETA_SALIDA / Path(ruta_pdf).name
                shutil.copy2(ruta_pdf, ruta_pdf_salida)


                # 2. Preparar valores

                valores_mes = preparar_datos_pdf(
                    datos,
                    campos_mes
                )


                # 3. Normalizar valores

                valores_normalizados = (
                    normalizar_valores_pdf(
                        valores_mes
                    )
                )


                # 4. Escribir PDF

                escribir_campos_pdf(
                    ruta_pdf_salida,
                    valores_normalizados
                )

                total_horas = calcular_total_horas(ruta_pdf_salida)

                escribir_total_horas(
                    ruta_pdf_salida,
                    total_horas
                )

                actualizados += 1

                print("✓ PDF actualizado")


            except Exception as e:

                errores += 1

                print(
                    "❌ ERROR:",
                    e
                )


    except Exception as e:

        errores += 1

        print(
            "❌ ERROR AL PROCESAR EL GRUPO:",
            e
        )


# =========================
# RESUMEN FINAL
# =========================

print()
print("========================================")
print("PROCESO TERMINADO")
print("========================================")

print("Mes:", MES)
print("Año:", AÑO)
print("Grupos procesados:", len(GRUPOS))

print()
print("PDF actualizados:", actualizados)
print("PDF no encontrados:", pdf_no_encontrados)
print("Errores:", errores)

print("========================================")



