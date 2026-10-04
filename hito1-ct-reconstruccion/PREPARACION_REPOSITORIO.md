# Preparación del repositorio independiente

Date: 2026-10-04. Fuente: G2SantiRobeson/tesis-modelos-difusion, carpeta hito1-mini-tesis.
Commit de origen: `3ff02911620c8aaca0f6c3d7ac97dedf9f266465`.

## Cambios de portabilidad

- Rutas de entrada a data/sdct y data/ldct, relativas al JSON.
- Notebooks que localizan la raíz por src/config.py y config/default.json, sin exigir un nombre de carpeta.
- Instrucciones de instalación y publicación desde la raíz del repositorio nuevo.
- Ejecución alternativa de las mismas celdas, con un proceso Python nuevo por notebook, sin sockets Jupyter.
- Validación portable separada de la comparación literal de las 36 cifras publicadas.
- Referencias tabulares originales preservadas y procedencia registrada.
- Ningún cambio en los cálculos científicos, filtros, semillas ni tolerancias publicadas.

## Verificación en esta preparación

- Entorno nuevo Python 3.12.14, instalado desde requirements.txt sin cambiar versiones.
- Nueve notebooks ejecutados; 23 figuras; once pruebas numéricas aprobadas.
- Las 20 referencias RMSE por filtro y las 12 métricas Ramp coinciden con el informe a la precisión publicada.
- Los tres controles Fourier pasan: sinogramas filtrados, reconstrucciones y FFT contra el pipeline iradon.
- Los dos hashes DICOM coinciden con las entradas utilizadas anteriormente.
- La validación estricta devuelve código de salida 1 porque las cuatro cifras Fourier no coinciden literalmente.
- Los DICOM están en el paquete local pero git check-ignore confirma que se excluyen de git add .

El ejecutor original reproduce.py no pudo arrancar sus kernels en este entorno porque no se permite enlazar sockets TCP/IPC. Los notebooks sí se ejecutaron íntegramente mediante reproduce_without_jupyter.py, usando sus mismas celdas en procesos separados. Esto no es una validación nueva del modo con kernels externos ni una ejecución en Windows.

## Diferencias Fourier

| Etapa | Métrica | Informe | Esta ejecución | Unidad |
|---|---|---:|---:|---|
| reconstrucciones_HU | maximo | 3.342e-11 | 3.3082869777e-11 | HU |
| reconstrucciones_HU | media | 7.289e-13 | 7.23604336172e-13 | HU |
| reconstrucciones_HU | rmse | 9.590e-13 | 9.4879407656e-13 | HU |
| sinogramas_filtrados | maximo | 8.69e-13 | 8.58049742369e-13 | Suma Radon |

La ejecución original y esta preparación no producen exactamente las mismas cifras de redondeo. El entorno numérico es una explicación posible; esta comparación no aísla qué componente concreta origina la variación. Los archivos de referencia conservan las cifras originales y no se presentan los cuatro fallos estrictos como aprobados.

## Ejecución de notebooks

| Notebook | Estado | Tiempo en segundos |
|---|---|---:|
| 01_ct_images_and_data.ipynb | passed | 2.3 |
| 02_radon_and_sinograms.ipynb | passed | 9.3 |
| 03_backprojection_and_fbp.ipynb | passed | 8.1 |
| 04_sdct_ldct_photon_simulation.ipynb | passed | 10.9 |
| 05_gaussian_noise_analysis.ipynb | passed | 12.1 |
| 06_sdct_ldct_sinogram_comparison.ipynb | passed | 19.5 |
| 07_fbp_filter_comparison.ipynb | passed | 34.9 |
| 08_fourier_dft_vs_fft.ipynb | passed | 10.6 |
| 09_metrics_and_report_figures.ipynb | passed | 15.6 |

Resultados detallados: outputs/tables/portable_validation.json, standalone_recompute.json y report_reference_validation.json. Referencias originales: reference_outputs/tables. Versiones del entorno: requirements-validated-linux.txt.

## Publicación

El paquete no contiene la historia Git ni las demás carpetas del repositorio original. README.md contiene los comandos para crear el repositorio nuevo. No se ha creado ni publicado ningún repositorio remoto en esta tarea.
