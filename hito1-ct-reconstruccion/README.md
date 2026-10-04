# Hito 1: reconstrucción tomográfica con FBP

Copia independiente de `hito1-mini-tesis/`. Compara cinco filtros FBP con y
sin ruido gaussiano adicional y DFT directa frente a FFT, sobre el par C095 /
1-250 del dataset TCIA LDCT-and-Projection-Data. No entrena modelos de difusión.
Los cálculos, parámetros, semillas y referencias publicadas se conservan.

## Ejecución en Windows (PowerShell)

Desde la carpeta que contiene este README:

```powershell
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -B reproduce_without_jupyter.py --only 07 08 09
& .\.venv\Scripts\python.exe -B validate_portable.py
```

07, 08 y 09 generan los resultados principales del informe. Para ejecutar los
nueve notebooks, omite `--only 07 08 09`. El ejecutor alternativo usa las mismas
celdas en un proceso Python nuevo por notebook, sin abrir sockets Jupyter.
`reproduce.py` conserva la alternativa original con kernels Jupyter.

En Linux/macOS crea el entorno con `python3.12 -m venv .venv` y usa
`.venv/bin/python` en lugar de `.\.venv\Scripts\python.exe`.

Para trabajar interactivamente:

```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements-notebook.txt
& .\.venv\Scripts\python.exe -m jupyter lab notebooks
```

Python probado: 3.12.14. Las versiones numéricas originales están fijadas en
`requirements.txt`. `requirements-validated-linux.txt` registra además todas
las dependencias del entorno de esta preparación.

## Datos

El paquete local incluye las dos entradas comprobadas. Git ignora los DICOM:
quien clone GitHub debe proporcionar estos archivos de nuevo o ajustar sus rutas:

```text
data/sdct/1-250.dcm
data/ldct/1-250.dcm
```

Son Full Dose Images y Low Dose Images del mismo corte C095. `data/README.md`
contiene sus SHA-256. Las rutas de `config/default.json` son relativas a
`config/`, no a la terminal. No hacen falta otras carpetas del proyecto original.
Los notebooks pueden ejecutarse aunque se cambie el nombre del repositorio.

## Validación

| Comando | Alcance |
|---|---|
| `validate_portable.py` | Once pruebas, notebooks ejecutados, tres controles de equivalencia Fourier y 32 métricas del informe. Informa las cuatro coincidencias literales Fourier por separado. |
| `validate.py --reference` | Exige las 36 cifras publicadas en las salidas guardadas. |
| `validate.py --reference --recompute-reference` | También recalcula las 36 cifras desde los DICOM sin reemplazar salidas científicas. |
| `validate.py --originals` | Auditoría histórica que necesita el repositorio antiguo; no usar para esta copia independiente. |

El informe final utiliza las cuatro cifras de residuos DFT–FFT del cálculo
Linux: `3.308e-11 HU`, `7.236e-13 HU`, `9.488e-13 HU` y `8.58e-13` en el
sinograma filtrado. Estas referencias coinciden con las salidas guardadas en
`outputs/`; las otras 32 métricas de filtros y Ramp se conservan. No se
modifican los cálculos ni las tolerancias. En otro entorno, los residuos pueden
variar ligeramente y la validación estricta puede devolver código de salida 1
aunque se cumplan los tres controles de equivalencia Fourier.

Las tablas originales están en `reference_outputs/tables/`.
`config/report_reference.json` conserva las cifras publicadas en el informe final. Los resultados
actuales están en `outputs/` y el detalle de esta preparación en
`PREPARACION_REPOSITORIO.md`. Una ejecución reemplaza sus salidas y notebooks,
sin escribir en los DICOM ni en las referencias publicadas.

## Estructura

`config/`: parámetros y referencias; `notebooks/`: nueve experimentos;
`src/`: funciones científicas; `tests/`: contratos numéricos;
`outputs/`: figuras, métricas y arrays; `reference_outputs/`: tablas originales;
`data/`: instrucciones y entradas locales ignoradas por Git.

El notebook 04 mantiene el antecedente de simulación por fotones y el 08 incluye
un diagnóstico de tiempos por tamaño. Se conservan porque ya estaban en la
carpeta original; el informe actual se centra en ruido gaussiano y concordancia
DFT–FFT. Los documentos históricos de auditoría describen verificaciones previas;
no representan verificaciones nuevas de carpetas externas ausentes.

## Publicar como repositorio nuevo

1. Crea un repositorio vacío en GitHub, por ejemplo `hito1-ct-reconstruccion`,
   sin generar README, licencia ni .gitignore automáticamente.
2. Descomprime el paquete. Abre PowerShell dentro de la carpeta que contiene
   este README: estos archivos deben quedar en la raíz del repositorio nuevo.
3. Sustituye NOMBRE_DEL_REPOSITORIO por el nombre elegido:

```powershell
git init
git branch -M main
git add .
git status
git commit -m "Publicar experimento reproducible del Hito 1"
git remote add origin https://github.com/G2SantiRobeson/NOMBRE_DEL_REPOSITORIO.git
git push -u origin main
```

Revisa `git status` antes del commit. Los DICOM, .venv y cachés se ignoran.
El historial empieza de nuevo y el repositorio original se conserva.
Tras publicar y verificar, registra el commit o una etiqueta estable para
citar el código asociado al informe.

## Límites científicos

Las imágenes ya están reconstruidas y sus sinogramas se recalculan.
Cada reconstrucción se compara con su propia entrada, usando toda la matriz.
Se conserva la escala común SDCT (-1024 a 1616 HU), 512 ángulos, circle=False,
interpolación lineal, sigma 1 y SeedSequence(42).spawn(2).
El ruido gaussiano adicional no se calibra a una dosis física y las entradas
conservan el ruido del dataset. Un único corte no permite generalizar resultados
clínicos. La amplificación visual no se aplica a las métricas.
