# HITO-1: reconstrucción tomográfica y experimentos numéricos

Código y resultados del primer hito de la tesis de Santiago Robeson sobre
reconstrucción de tomografía computarizada de baja dosis, en la Universidad de
los Andes (Chile).

El proyecto estudia el recorrido **imagen → sinograma → imagen reconstruida**
mediante la transformada de Radon y la retroproyección filtrada (FBP). Compara
cinco filtros, evalúa el efecto de añadir ruido gaussiano al sinograma y comprueba
la concordancia numérica entre el cálculo directo de la transformada discreta de
Fourier (DFT) y su cálculo mediante la transformada rápida de Fourier (FFT).
Este hito establece una base numérica para la investigación; no implementa ni
entrena modelos de difusión.

## Consultar los resultados

Los resultados guardados pueden revisarse sin instalar Python ni descargar los
datos de entrada:

| Contenido | Ubicación |
|---|---|
| Figuras de los experimentos | [outputs/figures](hito1-ct-reconstruccion/outputs/figures/) |
| Métricas de los cinco filtros | [07_filters.csv](hito1-ct-reconstruccion/outputs/tables/07_filters.csv) |
| Comparación DFT–FFT | [08_fourier.json](hito1-ct-reconstruccion/outputs/tables/08_fourier.json) |
| Métricas de las reconstrucciones con Ramp | [09_report_metrics.csv](hito1-ct-reconstruccion/outputs/tables/09_report_metrics.csv) |
| Parámetros y versiones de ejecución | [09_execution.json](hito1-ct-reconstruccion/outputs/tables/09_execution.json) |
| Verificación de las cifras del informe | [VALIDATION_REPORT.md](hito1-ct-reconstruccion/VALIDATION_REPORT.md) |

Los experimentos principales están en estos notebooks, que incluyen sus salidas:

- [07: comparación de filtros FBP](hito1-ct-reconstruccion/notebooks/07_fbp_filter_comparison.ipynb).
- [08: DFT directa frente a FFT](hito1-ct-reconstruccion/notebooks/08_fourier_dft_vs_fft.ipynb).
- [09: métricas y figuras del informe](hito1-ct-reconstruccion/notebooks/09_metrics_and_report_figures.ipynb).

## Datos y alcance del experimento

Se utilizan las imágenes de dosis estándar (SDCT) y baja dosis (LDCT) del caso
**C095**, corte de tórax **1-250.dcm**, del conjunto
[LDCT-and-Projection-Data de TCIA](https://doi.org/10.7937/9npb-2637).
Las imágenes ya están reconstruidas: los sinogramas se calculan a partir de ellas
y no corresponden a las proyecciones originales del escáner.

Las condiciones principales son:

| Parámetro | Valor |
|---|---|
| Geometría | Haces paralelos en dos dimensiones |
| Muestreo angular | 512 ángulos uniformes en `[0°, 180°)` |
| Proyección y reconstrucción | `circle=False`, interpolación lineal |
| Normalización común | Rango SDCT de −1024 a 1616 HU, sin recorte para las métricas |
| Filtros FBP | Ramp, Shepp–Logan, Cosine, Hamming y Hann |
| Ruido añadido | Gaussiano con desviación estándar 1 en unidades del sinograma |
| Generación del ruido | `SeedSequence(42).spawn(2)`: realizaciones independientes para SDCT y LDCT; la misma realización se reutiliza entre filtros de cada entrada |
| Comparación DFT–FFT | Entrada SDCT, filtro Ramp discreto común y longitud de cálculo `N = 2048` |
| Tolerancias de equivalencia DFT–FFT | `atol=1e-9`, `rtol=1e-10`, en la escala normalizada |

Cada reconstrucción se compara con **su propia imagen de entrada** mediante el
error absoluto medio, la raíz del error cuadrático medio y el error absoluto
máximo, expresados en unidades Hounsfield (HU). La condición sin ruido añadido
conserva el ruido presente en el dataset. El ruido gaussiano adicional no se
asocia a una dosis física determinada y los resultados de un único corte no
permiten establecer conclusiones clínicas generales.

## Preparar el entorno

Se ha verificado el proyecto con **Python 3.12.14**. Las versiones de las
dependencias están fijadas en
[requirements.txt](hito1-ct-reconstruccion/requirements.txt).

Clona el repositorio y entra en la carpeta de trabajo:

```bash
git clone https://github.com/G2SantiRobeson/HITO-1.git
cd HITO-1/hito1-ct-reconstruccion
```

Los siguientes comandos se ejecutan desde `hito1-ct-reconstruccion/`.

**Windows (PowerShell):**

```powershell
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Linux/macOS:**

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

### Incorporar las imágenes DICOM

Los DICOM no están incluidos en GitHub. Para reproducir las cifras del informe,
obtén las dos imágenes del dataset y colócalas en estas rutas dentro de la
carpeta de trabajo:

- `data/sdct/1-250.dcm`: imagen de dosis estándar.
- `data/ldct/1-250.dcm`: imagen de baja dosis.

[data/README.md](hito1-ct-reconstruccion/data/README.md) contiene los hashes
SHA-256 de las entradas utilizadas para comprobar que sean las mismas imágenes.
Las rutas pueden configurarse en
[config/default.json](hito1-ct-reconstruccion/config/default.json); son relativas
a la carpeta `config/`. Usar otro corte cambia los resultados y deja de reproducir
las cifras del informe.

## Reproducir y validar

Para ejecutar los tres notebooks principales y contrastar sus resultados con
las 36 cifras publicadas en el informe:

**Windows (PowerShell):**

```powershell
& .\.venv\Scripts\python.exe -B reproduce_without_jupyter.py --only 07 08 09
& .\.venv\Scripts\python.exe -B validate.py --reference
```

**Linux/macOS:**

```bash
.venv/bin/python -B reproduce_without_jupyter.py --only 07 08 09
.venv/bin/python -B validate.py --reference
```

El ejecutor utiliza las celdas de los notebooks en procesos Python independientes.
Actualiza sus salidas, figuras y tablas dentro del proyecto. Para ejecutar los
nueve notebooks, omite `--only 07 08 09`.

El validador comprueba las cifras del informe, ejecuta 11 pruebas numéricas,
revisa que los nueve notebooks guardados tengan salidas sin errores y comprueba
tres controles de equivalencia Fourier. Para recalcular además las cifras desde
los DICOM, añade `--recompute-reference` al comando de validación.

La última validación registrada obtuvo **36/36 coincidencias** tanto en las
salidas guardadas como en el recálculo desde los DICOM. La comparación de cifras
usa media unidad del último decimal publicado; es independiente de las
tolerancias de equivalencia DFT–FFT. Los residuos numéricos de Fourier pueden
variar ligeramente entre entornos aunque los controles de equivalencia pasen.
El detalle se guarda en `VALIDATION_REPORT.md` y
`outputs/tables/report_reference_validation.json` dentro de la carpeta de trabajo.

`validate_portable.py` ofrece una comprobación que exige las 32 métricas de
filtros y Ramp e informa por separado las cuatro coincidencias de cifras Fourier.

### Trabajar con Jupyter

También es posible abrir y ejecutar los notebooks de forma interactiva. En
PowerShell:

```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements-notebook.txt
& .\.venv\Scripts\python.exe -m jupyter lab notebooks
```

En Linux/macOS, utiliza `.venv/bin/python` en lugar de
`.\.venv\Scripts\python.exe`. `reproduce.py` permite ejecutar los notebooks
mediante kernels Jupyter como alternativa al ejecutor anterior.

## Organización del repositorio

El código y los resultados están en `hito1-ct-reconstruccion/`:

| Carpeta | Contenido |
|---|---|
| `config/` | Parámetros del experimento y cifras de referencia del informe final |
| `data/` | Instrucciones para las entradas DICOM; los archivos de imagen se mantienen localmente |
| `notebooks/` | Nueve experimentos, desde las imágenes y los sinogramas hasta los resultados del informe |
| `src/` | Funciones de procesamiento, reconstrucción, métricas y visualización |
| `tests/` | Pruebas de los contratos numéricos y de la validación |
| `outputs/` | Figuras, tablas, arrays y registros de las ejecuciones |
| `reference_outputs/` | Resultados históricos conservados para trazabilidad |

El notebook 04 incluye una simulación por fotones y el 08 un diagnóstico de
tiempos por tamaño. Son experimentos complementarios: el informe de este hito
se centra en ruido gaussiano, filtros FBP y concordancia numérica DFT–FFT.
