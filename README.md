# Automatización de formularios y documentos PDF

Este proyecto surgió de una tarea administrativa repetitiva: reunir respuestas de formularios, compararlas con una lista de referencia y actualizar varios documentos PDF. En lugar de hacer esos pasos manualmente, organicé el proceso en varios módulos de Python.

La idea es que cada parte tenga una responsabilidad clara: leer los archivos de Excel, combinar la información mediante identificadores y actualizar las copias de los PDF correspondientes.

## ¿Qué hace?

- Lee archivos de Excel exportados desde formularios.
- Lee una hoja de referencia con los datos de cada registro.
- Relaciona ambas fuentes mediante un identificador único.
- Prepara los valores que se escribirán en cada formulario PDF.
- Actualiza campos de participación, cursos, horas y notas.
- Calcula el total de horas registrado en el documento.
- Prepara copias de los formularios para un nuevo periodo.
- Guarda los PDF procesados en una carpeta separada para conservar los originales.

## Flujo de trabajo

1. **Entrada:** se reciben los archivos de respuestas y la hoja de referencia en formato Excel.
2. **Lectura:** `pandas` lee las hojas y organiza la información en estructuras de Python.
3. **Integración:** el programa cruza los registros mediante sus identificadores.
4. **Preparación:** se convierten los valores al formato que esperan los campos del PDF.
5. **Actualización:** `pypdf` escribe los datos en una copia del documento.
6. **Cálculo:** se suman las horas registradas y se actualiza el campo de total.
7. **Salida:** los documentos procesados se guardan en `output/`.

## Archivos del proyecto

| Archivo | Para qué sirve |
|---|---|
| `main.py` | Coordina el proceso completo y contiene la configuración del periodo y los grupos. |
| `respuestas.py` | Lee el Excel de respuestas y organiza los valores por identificador. |
| `lista_maestra.py` | Lee la hoja de referencia. |
| `datos_publicadores.py` | Combina los datos de las dos fuentes. |
| `pdf.py` | Localiza los PDF, prepara los valores, actualiza los campos y calcula las horas. |
| `limpiar_tarjetas.py` | Crea copias de los formularios y limpia los campos de un nuevo periodo. |

## Herramientas utilizadas

- Python
- pandas
- openpyxl
- pypdf
- Excel
- Formularios PDF interactivos

## Instalación

Se necesita Python 3.10 o posterior.

Crea un entorno virtual:

```bash
python -m venv .venv
```

Actívalo en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Archivos de entrada que necesita

El programa original está organizado para trabajar con esta estructura:

```text
proyecto/
├── datos/
│   ├── Lista maestra publicadores.xlsx
│   └── 2026-09/
│       ├── GRUPO 1 SEPTIEMBRE.xlsx
│       ├── GRUPO 2 SEPTIEMBRE.xlsx
│       ├── GRUPO 3 SEPTIEMBRE.xlsx
│       ├── GRUPO 4 SEPTIEMBRE.xlsx
│       └── GRUPO 5 SEPTIEMBRE.xlsx
├── pdfs/
│   └── formularios originales
├── pdfs 2027/
├── output/
└── archivos Python
```

Los nombres de carpeta y archivos del ejemplo corresponden a la configuración actual de `main.py`. Para otro periodo hay que ajustar las constantes de mes y año dentro de ese archivo.

La hoja de referencia debe incluir las columnas que utiliza `lista_maestra.py`: `ID`, `NOMBRE`, `PRIVILEGIO`, `PUB. / PREC.`, `GRUPO`, `ARCHIVO_PDF` y `ESTADO`.

En el archivo de respuestas, los encabezados se organizan como `ID - nombre del campo`. La función actual ignora la columna `Marca temporal` y lee la primera fila de respuestas de cada archivo.

## Cómo ejecutar el proceso

Primero, coloca los formularios originales en `pdfs/`. Después ejecuta:

```bash
python limpiar_tarjetas.py
```

Este paso crea las copias preparadas para el nuevo periodo en `pdfs 2027/`.

Luego coloca los archivos de respuestas y la hoja de referencia en las carpetas indicadas y ejecuta:

```bash
python main.py
```

Los PDF actualizados se guardan en `output/`. El código actual utiliza septiembre de 2026, cinco grupos y la carpeta `pdfs 2027`; esos valores están definidos dentro de `main.py`.

## Consideraciones antes de ejecutarlo

- Los identificadores de las respuestas deben existir en la hoja de referencia.
- Los nombres de los archivos PDF deben coincidir con los indicados en la columna `ARCHIVO_PDF`.
- Los Excel y PDF deben respetar la estructura de columnas y campos que espera el código.
- La lectura de respuestas está implementada actualmente para la primera fila de cada archivo.
- Si los encabezados, identificadores o campos PDF no coinciden con los esperados, será necesario adaptar el código.
- El programa está pensado para el formato específico de los formularios utilizados en el proyecto; no es un lector universal de cualquier PDF.

## Privacidad

Por privacidad, este repositorio contiene únicamente código y documentación. No se incluyen las hojas de cálculo ni los formularios originales, ya que pueden contener datos personales. Para compartir o probar el proyecto, utiliza archivos ficticios o anonimizados.

## Estado del proyecto

Proyecto funcional basado en un flujo de trabajo real. La lógica principal está separada por módulos y documentada; todavía se pueden ampliar las pruebas, la configuración y la validación de archivos de entrada.
