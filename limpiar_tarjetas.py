
from pathlib import Path
from pypdf import PdfReader, PdfWriter

# =========================
# CONFIGURACIÓN
# =========================

CARPETA_ORIGEN = Path("pdfs")
CARPETA_DESTINO = Path("pdfs 2027")

CARPETA_DESTINO.mkdir(exist_ok=True)

# =========================
# CAMPOS QUE SE DEBEN LIMPIAR
# =========================

def obtener_campos_para_limpiar():

    campos = {}

    for indice in range(20, 32):

        campos[f"901_{indice}_CheckBox"] = "/Off"
        campos[f"902_{indice}_Text_C_SanSerif"] = ""
        campos[f"903_{indice}_CheckBox"] = "/Off"
        campos[f"904_{indice}_S21_Value"] = ""
        campos[f"905_{indice}_Text_SanSerif"] = ""

    campos["904_32_S21_Value"] = ""

    # Actualizar el año de servicio
    campos["900_13_Text_C_SanSerif"] = "2027"

    return campos

# =========================
# LIMPIAR UN PDF
# =========================

def limpiar_pdf(ruta_origen, ruta_destino):

    reader = PdfReader(ruta_origen)
    campos_pdf = reader.get_fields() or {}

    campos_limpieza = obtener_campos_para_limpiar()

    faltantes = [
        nombre
        for nombre in campos_limpieza
        if nombre not in campos_pdf
    ]

    if faltantes:
        raise ValueError(
            f"Faltan {len(faltantes)} campos esperados. "
            f"Ejemplo: {faltantes[0]}"
        )

    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    for pagina in writer.pages:
        writer.update_page_form_field_values(
            pagina,
            campos_limpieza,
            auto_regenerate=False
        )

    with open(ruta_destino, "wb") as archivo:
        writer.write(archivo)

# =========================
# PROCESAR TODAS LAS TARJETAS
# =========================

def main():

    archivos_pdf = list(CARPETA_ORIGEN.glob("*.pdf"))

    if not archivos_pdf:
        print("No se encontraron archivos PDF en la carpeta de origen.")
        return

    procesados = 0
    errores = 0

    for ruta_origen in archivos_pdf:

        ruta_destino = CARPETA_DESTINO / ruta_origen.name

        try:
            limpiar_pdf(ruta_origen, ruta_destino)
            procesados += 1
            print(f"✓ Tarjeta limpia: {ruta_origen.name}")

        except Exception as error:
            errores += 1
            print(f"✗ Error en {ruta_origen.name}: {error}")

    print("\n========== RESUMEN ==========")
    print(f"Tarjetas procesadas: {procesados}")
    print(f"Errores: {errores}")
    print(f"Destino: {CARPETA_DESTINO.resolve()}")

if __name__ == "__main__":
    main()