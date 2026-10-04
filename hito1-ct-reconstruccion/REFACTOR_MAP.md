# Auditoría y trazabilidad del Hito 1 actualizado

## Alcance y materiales revisados

Refactor realizado el 01-10-2026, íntegramente dentro de `hito1-mini-tesis/`.
Se recorrieron los archivos del repositorio, incluidos ocultos e ignorados,
excluyendo dependencias instaladas (`.venv`, `node_modules`), `.git`, cachés Python/
pytest y metadatos de instalación. El inventario conserva **1137 archivos**:
**46 scripts Python, 21 notebooks (incluidos históricos/checkpoints), 952 DICOM**
y documentos/resultados. Se identificaron funciones con AST y se inspeccionaron
las celdas de los notebooks y los modelos numéricos relevantes.

Los detalles por archivo, funciones y líneas están en
[audit_inventory.csv](outputs/tables/audit_inventory.csv). El manifiesto
[original_manifest.json](outputs/tables/original_manifest.json) conserva los
SHA-256 anteriores a crear código; incluye también datos y resultados originales.
Once directorios temporales de pytest/pip rechazaron lectura; sus rutas constan
en el manifiesto. No se afirma haber inspeccionado su contenido. No contienen
entradas de ejecución identificadas en los imports/documentación del proyecto.

Materiales que determinan el alcance:

| Evidencia | Uso en la auditoría |
|---|---|
| `Hito-1/README.md`, `hito_1.ipynb`, `reproducir.py`, configuración y métricas | Reproducción verificable de una versión anterior: dos figuras y doce métricas de cuatro ramas Ramp. |
| `results/informe_hito1/overleaf/secciones_5_6.tex`, LEEME y ZIP | Secciones disponibles de imágenes y métricas; no constituyen toda la mini-tesis actual. |
| `results/informe_hito1/overleaf/metricas/*` | Resultados de filtros, sinogramas y DFT/FFT conservados como respaldo. |
| `results/presentacion_tcia/entrega/Resultados_TCIA.pptx` | Presentación de veinte diapositivas: sinogramas/porcentajes (3–11), cinco filtros (12–16), DFT/FFT (17–20). |
| `sdct_ldct_sinograma_gaussiano.ipynb` y `tcia_comparacion_filtros_fbp.ipynb` | Cálculos y parámetros que produjeron el recorrido ampliado en C095/1-250. |
| `results/fourier_vs_fft_tcia/comparar_fourier_tcia.py`, README y resultados | Definición explícita DFT/inversa, Ramp discreto, padding, retroproyección y control contra pipeline. |
| `try_the_algorithm.ipynb`, núcleo `ldct/` y documentación de cambios | Antecedente de simulación por fotones, separado del ruido gaussiano post-Radon. |
| `tmp/audit/original/*`, `tmp/audit/report.txt` | Copias previas y texto extraído del informe de Camila Figueroa, Dosis 8, diciembre de 2025. Contexto histórico; no es la mini-tesis del autor. |
| README raíz, COMO_EJECUTAR, `docs/CHANGES.md`, NOTA-AGENTE-ESCALA-DIFERENCIAS y documentos LoDoPaB | Contratos, modificaciones previas, problemas de escala y límites de otras etapas. |
| Aclaración del autor durante esta tarea | La mini-tesis actual incluye cinco filtros y DFT directa/FFT. El README anterior no delimita el Hito 1 actual. |
| Cifras explícitas del informe actual proporcionadas por el autor | Referencia independiente del repositorio: 20 RMSE por filtro, 12 métricas Ramp y 4 diferencias DFT/FFT, conservadas en `config/report_reference.json`. |

No se encontró un archivo de bitácora independiente ni la mini-tesis ampliada
completa. No se inventó un calendario experimental para suplirlos.

## Reconstrucción temporal y orden conceptual

El texto Dosis 8 está fechado diciembre de 2025. `docs/CHANGES.md` documenta
una auditoría previa el 14-09-2026; LoDoPaB tiene un diagnóstico del 21-09-2026;
la guía de ejecución está revisada el 28-09-2026. El Git actual contiene:

- `91a6d48`, 21-09-2026, `Initial commit`.
- `8a6c33c`, 21-09-2026, `Code-22-09`.
- `7ac7e58`, 28-09-2026, `few changes`, incorpora material Hito-1, filtros,
  Fourier, presentación e informe disponible.

Los README antiguos dicen que no existía `.git` en sus copias; hoy sí existe.
Es una diferencia de estado histórico, no una razón para ignorar el Git actual.
La incorporación conjunta de varios resultados no permite ordenar sus días de
ejecución. El orden nuevo sigue sus dependencias conceptuales: lectura → proyección
→ BP/FBP → antecedente de dosis → gaussiana principal → comparación → filtros
→ Fourier → métricas/figuras. El notebook 04 se rotula antecedente y se puede omitir.

## Correspondencia de notebooks

Abreviatura `DESARROLLO`:
`codigo-camila-bluemili/ldct_simulation-main/ldct_simulation-main/`.
Los números de celda indicados son índices JSON empezando en cero.

| Nuevo archivo | Origen concreto | Cambio realizado |
|---|---|---|
| `notebooks/01_ct_images_and_data.ipynb` | `DESARROLLO/sdct_ldct_sinograma_gaussiano.ipynb`, celdas 8–14; `Hito-1/reproducir.py: leer_hu/calcular` | Lectura/validación y escala compartida aisladas; parámetros/rutas centralizados. |
| `notebooks/02_radon_and_sinograms.ipynb` | Mismo notebook, celda 16; `ldct/sinogram.py: generate_sinogram` | Proyección aislada y lectura de perfiles del mismo array; no se cambia adquisición. |
| `notebooks/03_backprojection_and_fbp.ipynb` | `comparar_fourier_tcia.py: retroproyectar`; `Hito-1/reproducir.py: calcular` | Descomposición didáctica BP/FBP y contraste con `iradon(None)`; la BP sin filtro no es una figura publicada atribuida al informe. |
| `notebooks/04_sdct_ldct_photon_simulation.ipynb` | `DESARROLLO/try_the_algorithm.ipynb`, celdas 1–7; `ldct/pipeline.py` | Antecedente completo con Poisson y Poisson+Gaussiano, mismos parámetros y comparación real. Su pertenencia a resultados publicados actuales no está confirmada. |
| `notebooks/05_gaussian_noise_analysis.ipynb` | `sdct_ldct_sinograma_gaussiano.ipynb`, celda 18; `noise/gaussian.py`; utilidades históricas de histograma | Ruido aislado y estadísticas de las mismas muestras; curva normal teórica para verificar la distribución, sin cambiarla. |
| `notebooks/06_sdct_ldct_sinogram_comparison.ipynb` | Mismo notebook, celdas 24 y 31; presentación, diapositivas 3–11 | Comparaciones absolutas y relativas aisladas; denominador fijo, umbral 1 % y límite visual 20 % preservados. |
| `notebooks/07_fbp_filter_comparison.ipynb` | `DESARROLLO/tcia_comparacion_filtros_fbp.ipynb`, celdas 8–14; presentación 12–16 | Veinte reconstrucciones y cuatro figuras; sinogramas/ruido generados una vez por condición. |
| `notebooks/08_fourier_dft_vs_fft.ipynb` | `results/fourier_vs_fft_tcia/comparar_fourier_tcia.py`; presentación 17–20 | Experimento completo en Jupyter; comparación por etapas y control público. Se añade diagnóstico de tiempo por tamaños usando una proyección existente. |
| `notebooks/09_metrics_and_report_figures.ipynb` | `Hito-1/hito_1.ipynb`, `reproducir.py`; `secciones_5_6.tex` | Figuras y doce cifras de referencia; CSV/NPZ, hashes/versiones y aclaración del alcance ampliado. |

## Correspondencia de módulos y archivos auxiliares

| Nuevo archivo | Origen | Cambio realizado |
|---|---|---|
| `src/__init__.py` | Nuevo | Paquete local sencillo, sin dependencia histórica. |
| `src/config.py`, `config/default.json` | Parámetros de los notebooks gaussianos, filtros, Fourier y fotones; `Hito-1/config.json` | Rutas relativas al JSON, parámetros centralizados y salidas acotadas al Hito 1. |
| `src/validation.py` | `DESARROLLO/ldct/validation.py` | Contratos finitos; se rechaza bool como entero positivo. |
| `src/io.py` | `ldct/io/dicom.py: read_ct/modality_values`; `Hito-1/reproducir.py: leer_hu/guardar`; `ldct/io/results.py` | Solo lectura CT y exportación simple; sin exportación DICOM, afines ni datos de identificación. |
| `src/normalization.py` | `ldct/normalization.py`; normalización LDCT del notebook gaussiano | Inversa con extremos originales; función explícita de escala compartida; sin clipping. |
| `src/radon.py` | `ldct/sinogram.py: generate_sinogram` | circle=False explícito en el recorrido principal; mismo theta y orientación. |
| `src/reconstruction.py` | `ldct/reconstruction.py: reconstruct_fbp`; `comparar_fourier_tcia.py: retroproyectar` | Parámetros principales Ramp/campo completo; la rama fotones pasa Hann y circle de su configuración original. Interpolación lineal explícita. |
| `src/noise.py` | `ldct/noise/{poisson,gaussian,__init__}.py`, `config.py`, `dose.py`, `sinogram.py`, `pipeline.py` | Modelos Gaussian post-Radon y Poisson(+Gaussian) en conteos separados; ecuaciones/constantes/calibraciones preservadas. Se exponen intermedios para lectura didáctica. |
| `src/filters.py` | Lista de filtros de `tcia_comparacion_filtros_fbp.ipynb`; `comparar_fourier_tcia.py: ramp_compartido` | Solo cinco filtros originales; Ramp discreto calculado con DFT explícita, sin API privada. |
| `src/fourier.py` | `comparar_fourier_tcia.py: matriz_dft/dft_directa/idft_directa/ejecutar` | Extracción del cálculo, mismas dos ramas; benchmark auxiliar explícitamente añadido. |
| `src/metrics.py` | `Hito-1/reproducir.py: metricas`; `comparar_fourier_tcia.py: medidas`; celda 31 gaussiana | Métricas imágenes, espectros complejos y diferencias relativas; unidades declaradas. |
| `src/visualization.py` | `Hito-1/reproducir.py: dibujar`; figuras de notebooks filtros/sinogramas y script Fourier | Ventanas compartidas, barras por fila, ×5 gráfico, cierre de figuras y tablas HTML sin pandas. |
| `src/experiments.py` | `Hito-1/reproducir.py: calcular`; celdas 16–20 gaussianas y 8–10 filtros | Preparación y cuatro condiciones comunes; evita funciones grandes/duplicadas en notebooks. |
| `config/reference_metrics.csv` | `Hito-1/metricas_informe.csv` | Doce valores iguales; columna `caso` renombrada `case`. |
| `config/report_reference.json` | Cifras del informe actual proporcionadas por el autor | Conserva cadenas, ceros finales y exponentes para contrastar la precisión publicada sin depender de los CSV históricos. |
| `src/report_validation.py`, `VALIDATION_REPORT.md`, `outputs/tables/report_reference_validation.json` | Validación nueva de la referencia explícita | Compara 36 cifras guardadas y 36 recalculadas desde DICOM, con diferencias, tolerancias, unidades y procedencia. Registra discrepancias antes de devolver error; no calibra resultados. |
| `tests/test_report_validation.py` | Contratos nuevos de validación | Precisión publicada, valores ausentes/no finitos, diferencias Fourier pequeñas y selección explícita de Ramp aunque se configure otro filtro. |
| `requirements*.txt` | Entorno Python 3.12 existente y dependencias realmente importadas | Versiones verificadas; interfaz JupyterLab separada. |
| `reproduce.py` | Nuevo soporte de reproducción con nbclient | Un kernel limpio por notebook, mismo intérprete y cachés bajo outputs; sin registrar kernels globales. |
| `validate.py`, `tests/test_numerical_contracts.py` | Valores publicados, CSV filtros, pipeline activo y controles numéricos independientes | Verificación de fidelidad e integridad; no nuevos experimentos clínicos. |
| `outputs/tables/audit_inventory.csv`, `original_manifest.json` | Auditoría antes de implementar | Inventario, símbolos, salidas con errores y hashes; no copia de datasets. |

Las nuevas salidas se vinculan por prefijo al notebook que las genera (01–09).
`notebooks_execution.json` registra ejecución; `validation.json` registra los
contrastes. No se incorporaron resultados de terceros como si fueran nuevos.

## Código excluido del nuevo recorrido y duplicaciones

Aquí «excluido» significa **no incorporado al refactor**. Ningún archivo original
fue borrado, movido o sobrescrito.

| Archivo/familia original | Decisión y fundamento |
|---|---|
| `tmp/audit/original/*` | Copias históricas con duplicación de simulación, imports y rutas; usadas para comparar decisiones antiguas, no como núcleo activo. |
| `algorithm/sim_functions.py`, `algorithm/utils_functions.py` | Adaptadores de compatibilidad que delegan a `ldct`; no son modelos alternativos. Evitar una segunda capa en el nuevo código. |
| `save_colorectal_ldct.py`, `ldct/cli.py`, `workflows.py: simulate_dataset` | Exportación por lotes y DICOM derivados ajena a las figuras del Hito 1; se conserva el modelo de un corte sin migrar CLI/exportación. |
| `solution_noise_sim.ipynb`, `metrics_simulation_phan`, ROIs/SNR/CNR | Antecedente Dosis 8 de otro informe; faltan series y selección de cortes. No fabricar un fantoma sustituto ni atribuir sus tablas al Hito 1 actual. |
| `calculate_seg_tumor.ipynb`, `extra_files/tumor_sizes.ipynb`, `segmentation.py`, `measurements.py` | Segmentación, modelos externos y medición tumoral; sin evidencia de uso en este Hito 1. |
| `ldct/io/nifti.py`, geometrías de series | No necesarias para experimentos 2D ni para su reproducción. |
| `lodopab_npy_test/*` | Adaptación posterior con ODL, dominios físicos y convenciones distintas. No mezclar sinogramas 1000×513 con los 725×512 de C095. |
| `tmp/documentar_notebook.py`, `agregar_comparacion_tcia.py`, `crear_notebook_hito1.py`, `audit/migrate_notebooks.py`, `.build/*` | Generadores temporales de notebooks/informe/presentación; el nuevo recorrido entrega artefactos y runner directo. |
| `.ipynb_checkpoints/*` | Seis copias automáticas; algunas difieren de su notebook activo. No tratarlas como evidencia de un experimento independiente. |
| `Hito-1/hito_1.ipynb` y `reproducir.py` | Implementación mínima anterior del mismo recorrido gaussiano; unificar la lógica preservando sus doce valores publicados. |
| `resultados/comparacion_filtros_tcia/metricas_filtros.csv` y `results/informe_hito1/overleaf/metricas/filtros.csv` | Duplicados **idénticos por SHA-256**; uno se utiliza como referencia independiente. |
| `results/fourier_vs_fft_tcia/metricas.csv` y `results/informe_hito1/overleaf/metricas/dft_fft.csv` | Duplicados **idénticos por SHA-256**; documentar ambos sin duplicar cálculos. |
| Prints de rutas, celdas vacías y contador `i` reutilizado en presentación de métricas | Retirados de la versión nueva; tablas HTML legibles. No cambian arrays. |
| Entrenamiento/difusión | No se identificó un entrenamiento activo entre estos scripts. No se agregaron redes ni librerías de etapas futuras. |

Los 21 notebooks auditados incluyen once entradas activas, cuatro históricos y
seis checkpoints. Se detectó una salida de error guardada en
`lodopab_sinogramas_formato_anterior.ipynb` y dos en el notebook histórico
`calculate_seg_tumor.ipynb`. Son señales de recorridos históricos incompletos;
no se presentaron como ejecuciones correctas del nuevo Hito 1.

## Problemas científicos y matemáticos: tratamiento explícito

| Archivo/función aproximada | Comportamiento encontrado | Problema o límite | Tratamiento / solución propuesta |
|---|---|---|---|
| `tmp/audit/original/sim_functions.py: apply_ld_sinogram_full`, líneas 77–86 | `gaussian_noise=True` usa solo Poisson; False añade gaussiana | Indicador invertido; nombres de estrategias no identifican de forma fiable las tablas históricas | No reintroducir el defecto. Preservar el núcleo activo ya corregido con nombres `poisson`/`poisson_gaussian`; registrar que no reproduce ciegamente la versión antigua. |
| Misma función, líneas 89–90 | Logaritmo antes de tratar conteos no positivos; posteriormente proyección=0 | Ceros se convierten en transmisión sin atenuación; posible NaN/inf | Mantener el piso **pre-log de 1 fotón del núcleo activo**, contar las muestras limitadas. Es una corrección histórica, no una nueva alteración silenciosa. |
| `tmp/audit/original/save_colorectal_ldct.py: save_lowdose_dicom` | Renormaliza la reconstrucción y multiplica por 4095 | Destruye escala original y presupone codificación | Nuevo recorrido no escribe DICOM; conserva inversa min–max de la imagen fuente y overshoot. |
| `tmp/audit/original/sim_functions.py`, líneas 42–52 | Inventa 200 mAs y pitch 0.7 si faltan metadatos | Hipótesis no justificadas y posible doble corrección de pitch | Leer mA×ms/1000 del antecedente C095 como hace `try_the_algorithm`; fallar si falta. No aplicar pitch implícito. |
| `ldct/config.py`, `dose.py`, `sinogram.py` | Constantes 0.015, 0.1002, 1000, escala 500 y gaussiana 0.05√λ; variante C095 con 2630/mAs | Modelo empírico, no conversión universal de min–max a atenuación física | Preservar las dos rutas, declarar cuál se usa y evitar extrapolarlas automáticamente a otros protocolos. |
| `tmp/audit/report.txt`, tablas 4/7/10; `metrics_simulation_phan` antiguo | σ rotulado como «varianza» y escalas simulada/real distintas | Sigma es desviación estándar; comparaciones numéricas inconmensurables | Documentar el problema. No recalcular ni «arreglar» tablas ajenas sin datos y protocolo. |
| Texto Dosis 8, pág. 3 frente a `ldct/sinogram.py` | Describe horizontal detector/vertical ángulo; array activo detector×ángulo | Convención de visualización diferente | Conservar ejes activos: horizontal ángulo/vertical índice de detector; rotularlos. No transponer silenciosamente. |
| `ldct/config.py: circle=True` predeterminado y `try_the_algorithm` | Campo circular predeterminado; C095 pasa explícitamente False | Puede descartarse camilla/esquinas en llamadas implícitas | Principal False; antecedente usa su configuración original explícita. Sin remuestrear ni enmascarar. |
| `try_the_algorithm.ipynb`, celda 3 | Verifica posición/orientación pero no PixelSpacing | Un nombre/posición coincidente no prueba igual malla | Añadir comprobación de PixelSpacing usada por el experimento principal. No cambia el par C095 válido; solo rechaza entradas incompatibles. |
| `sdct_ldct_sinograma_gaussiano.ipynb`, celda de métricas | Contador `i` reutilizado en bucle interior | Defecto de formato de encabezados/espacios | Sustituir por tablas; ningún cambio científico. |
| Mismo notebook, celda 31 | Cociente absoluto sobre abs(SDCT) con umbral 1 %, límite visual 20 % | El porcentaje amplifica zonas de señal pequeña; no mide por sí solo ruido Poisson | Preservar denominador/máscara/límite. Reportar porcentaje evaluado y conservar NaN fuera de máscara. |
| `comparar_fourier_tcia.py: ramp_compartido` | DFT del kernel discreto del Ramp, padding al final y orden nativo | Cambiar a 2*abs(f), desplazar espectros o filtrar dos veces alteraría el experimento | Preservar cálculo compartido, factor 1/N solo en inversa, recorte y retroproyección π/(2A); contrastar con `iradon` público. |
| Mismo script, mapas de diferencia | Autoescala de diferencias microscópicas, panel ×5 | Una estructura visible puede confundirse con discrepancia física importante | Conservar barras HU, máximo real y aviso de autoescala; métricas siempre sin amplificación. |
| Mismo script, tiempos de una ejecución | Un tiempo por rama incluyendo filtrado, sin benchmark por tamaños | No prueba crecimiento asintótico ni generaliza rendimiento | Conservar tiempos del experimento completo; añadir mediana de cinco repeticiones por N de una proyección, con construcción de matriz informada aparte. Es diagnóstico nuevo declarado. |

Cambios de robustez nuevos que no alteran el significado experimental: errores
claros por datos ausentes, arrays finitos, formas y metadatos compatibles, rechazo
de bool para tamaños, rutas independientes del directorio de terminal y salida
limitada al nuevo árbol. No se cambiaron semillas, distribuciones, geometría,
dimensiones ni filtros para conseguir coincidencias artificiales.

## Diferencias entre código y documentos

1. La versión disponible de `secciones_5_6.tex` y `Hito-1/README.md` publica solo
   Ramp/gaussiana. El autor confirmó que la mini-tesis actual también incluye
   cinco filtros y DFT/FFT. Se incorporan como parte del Hito 1 actualizado.
2. El código/presentación tiene comparaciones relativas y de sinogramas que no
   aparecen en esas dos páginas del informe breve. Quedan reproducibles en 06
   con sus unidades y denominador originales.
3. La simulación por fotones usa Hann y ruido en conteos pre-log. El recorrido
   principal usa Ramp u otros cuatro filtros y gaussiana en proyecciones
   post-Radon. No son experimentos intercambiables ni una única dosis calibrada.
4. Dosis 8 tiene otro autor, datos y ROIs. Se conserva como antecedente documental
   de los modelos; no se atribuye su SNR/CNR al Hito 1 del autor actual.
5. FFT es el algoritmo eficiente de la misma DFT. El nuevo texto y notebook
   conservan esa distinción y los controles de equivalencia.

## Validación y reproducción

Desde esta carpeta: `python -B reproduce.py` y
`python -B validate.py --reference --originals` (usar el Python del entorno).
El README detalla instalación, datos y ejecuciones individuales. Los resultados
de la ejecución completa constan en `outputs/tables/notebooks_execution.json`
y `outputs/tables/validation.json`. La validación compara las 36 cifras actuales,
sesenta valores de filtros históricos, las dos ramas activas por fotones y
todos los hashes del manifiesto. Las nuevas figuras y arrays se conservan dentro
de este árbol para revisión.

Resultado de la validación realizada: 9/9 notebooks ejecutados, 23 PNG, 11/11 pruebas
numéricas y de validación, 36/36 cifras actuales guardadas y 36/36 recalculadas,
60/60 valores de filtros, paridad exacta para
los dos modelos activos por fotones y ocho arrays Fourier históricos dentro de
tolerancia. La diferencia máxima DFT–FFT es 3.342393029015511e-11 HU. Los 1137
hashes originales auditados coinciden. La ejecución de kernels en Windows
necesitó salir del sandbox para que Jupyter asignara los permisos de su archivo
local de conexión; se usó el entorno existente, sin instalar paquetes ni modificar
su configuración. Las salidas/cachés se dirigieron al nuevo árbol. La revisión
visual confirmó barras, ventanas compartidas, rótulos y ausencia de recortes de
las figuras revisadas.

La ampliación de la validación usa las cifras explícitas del informe actual como
referencia independiente. Se verificaron **72/72 comparaciones** con tolerancia
relativa cero y media unidad del último decimal publicado: 0.0005 HU para las
métricas de imágenes, 5e-15 HU para el máximo DFT/FFT, 5e-17 HU para su media/RMSE
y 5e-16 en suma Radon para el máximo entre sinogramas filtrados. Las tolerancias
generales de equivalencia Fourier se mantienen separadas. No se modificó el
modelo científico ni se ajustaron parámetros o semillas para obtener coincidencias.

Desde esta carpeta, usando el entorno existente:
`& ..\.venv\Scripts\python.exe -B validate.py --reference --recompute-reference --originals`.
Las tablas de cada comparación y la procedencia del recálculo están en
[VALIDATION_REPORT.md](VALIDATION_REPORT.md).

