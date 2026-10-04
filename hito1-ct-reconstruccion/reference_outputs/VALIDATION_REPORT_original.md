# Validación contra los resultados del informe actual

**Referencia:** Resultados numéricos del informe actual proporcionados explícitamente por el autor en esta conversación; independientes de los CSV históricos del repositorio.

Valores proporcionados por el autor el 2026-10-01. Las cadenas publicadas se conservan en `config/report_reference.json`.

## Criterio de coincidencia

Cada cifra se compara sin redondear el resultado calculado, usando tolerancia relativa cero y tolerancia absoluta igual a media unidad del último decimal publicado. Esto reconoce la precisión del informe; no supone igualdad con sus valores redondeados.

- Métricas HU a tres decimales: 0.0005 HU.
- Máximo entre reconstrucciones 3.342e-11: 5e-15 HU.
- Media 7.289e-13 y RMSE 9.590e-13: 5e-17 HU.
- Máximo entre sinogramas filtrados 8.69e-13: 5e-16 en suma Radon, **no HU**.

Los umbrales anteriores son independientes de las tolerancias generales predeterminadas de equivalencia DFT/FFT (atol=1e-9, rtol=1e-10) del experimento. Esos umbrales generales no se usan para aprobar coincidencia con estas cifras publicadas.

El orden de condiciones es SDCT sin ruido / LDCT sin ruido / SDCT con ruido / LDCT con ruido. Aquí ‘sin ruido’ significa sin ruido añadido y conserva el ruido del dataset.

## Salidas guardadas de los notebooks 07, 08 y 09

**Resultado: 36/36 coincidencias.**

### RMSE por filtro

| Condición / etapa | Filtro | Métrica | Informe | Calculado | Diferencia calculado − informe | Tolerancia absoluta | Unidad | Estado |
|---|---|---|---:|---:|---:|---:|---|---|
| SDCT sin ruido añadido | ramp | RMSE_HU | 31.890 | 31.8897236016 | -0.0002763984195 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | ramp | RMSE_HU | 68.899 | 68.8988501961 | -0.0001498038992 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | ramp | RMSE_HU | 78.906 | 78.9061103016 | 0.00011030157264 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | ramp | RMSE_HU | 99.700 | 99.7000405016 | 4.050161012e-05 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | shepp-logan | RMSE_HU | 36.093 | 36.0934251852 | 0.000425185209405 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | shepp-logan | RMSE_HU | 75.494 | 75.494045097 | 4.509696207e-05 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | shepp-logan | RMSE_HU | 68.648 | 68.6479591976 | -4.080236727e-05 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | shepp-logan | RMSE_HU | 95.403 | 95.4030583273 | 5.83273026e-05 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | cosine | RMSE_HU | 45.174 | 45.1744091433 | 0.00040914334709 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | cosine | RMSE_HU | 90.579 | 90.5786991133 | -0.00030088673302 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | cosine | RMSE_HU | 58.673 | 58.6732133816 | 0.00021338156539 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | cosine | RMSE_HU | 98.020 | 98.0204728025 | 0.00047280248594 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | hamming | RMSE_HU | 52.658 | 52.6583602626 | 0.00036026264943 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | hamming | RMSE_HU | 99.666 | 99.6658749447 | -0.00012505529067 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | hamming | RMSE_HU | 60.278 | 60.2776096624 | -0.00039033755678 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | hamming | RMSE_HU | 103.902 | 103.902482831 | 0.0004828313828 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | hann | RMSE_HU | 54.638 | 54.6384227712 | 0.0004227711734 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | hann | RMSE_HU | 102.789 | 102.789295278 | 0.00029527782884 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | hann | RMSE_HU | 60.983 | 60.9834217876 | 0.0004217876187 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | hann | RMSE_HU | 106.312 | 106.31161056 | -0.00038943965437 | 0.0005 | HU | Coincide |

### MAE, RMSE y máximo con Ramp

| Condición / etapa | Filtro | Métrica | Informe | Calculado | Diferencia calculado − informe | Tolerancia absoluta | Unidad | Estado |
|---|---|---|---:|---:|---:|---:|---|---|
| SDCT sin ruido añadido | ramp | MAE_HU | 22.925 | 22.9247765386 | -0.00022346135785 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | ramp | RMSE_HU | 31.890 | 31.8897236016 | -0.0002763984195 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | ramp | MAX_HU | 355.433 | 355.433019643 | 1.964288213e-05 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | ramp | MAE_HU | 53.304 | 53.304137207 | 0.00013720695414 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | ramp | RMSE_HU | 68.899 | 68.8988501961 | -0.0001498038992 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | ramp | MAX_HU | 446.964 | 446.964431308 | 0.00043130790243 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | ramp | MAE_HU | 62.676 | 62.6759609668 | -3.9033154214e-05 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | ramp | RMSE_HU | 78.906 | 78.9061103016 | 0.00011030157264 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | ramp | MAX_HU | 435.844 | 435.843698318 | -0.0003016819419 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | ramp | MAE_HU | 79.012 | 79.0119184418 | -8.155824312e-05 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | ramp | RMSE_HU | 99.700 | 99.7000405016 | 4.050161012e-05 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | ramp | MAX_HU | 612.323 | 612.322683946 | -0.0003160535344 | 0.0005 | HU | Coincide |

### DFT directa frente a FFT

| Condición / etapa | Filtro | Métrica | Informe | Calculado | Diferencia calculado − informe | Tolerancia absoluta | Unidad | Estado |
|---|---|---|---:|---:|---:|---:|---|---|
| reconstrucciones_HU | ramp | maximo | 3.342e-11 | 3.34239302902e-11 | 3.93029015511e-15 | 5e-15 | HU | Coincide |
| reconstrucciones_HU | ramp | media | 7.289e-13 | 7.28859680943e-13 | -4.03190570607e-17 | 5e-17 | HU | Coincide |
| reconstrucciones_HU | ramp | rmse | 9.590e-13 | 9.58998284218e-13 | -1.715781612e-18 | 5e-17 | HU | Coincide |
| sinogramas_filtrados | ramp | maximo | 8.69e-13 | 8.69304628281e-13 | 3.04628281498e-16 | 5e-16 | Suma Radon | Coincide |

## Recálculo independiente desde los DICOM

**Resultado: 36/36 coincidencias.**

### RMSE por filtro

| Condición / etapa | Filtro | Métrica | Informe | Calculado | Diferencia calculado − informe | Tolerancia absoluta | Unidad | Estado |
|---|---|---|---:|---:|---:|---:|---|---|
| SDCT sin ruido añadido | ramp | RMSE_HU | 31.890 | 31.8897236016 | -0.0002763984195 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | ramp | RMSE_HU | 68.899 | 68.8988501961 | -0.0001498038992 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | ramp | RMSE_HU | 78.906 | 78.9061103016 | 0.00011030157264 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | ramp | RMSE_HU | 99.700 | 99.7000405016 | 4.050161012e-05 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | shepp-logan | RMSE_HU | 36.093 | 36.0934251852 | 0.000425185209405 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | shepp-logan | RMSE_HU | 75.494 | 75.494045097 | 4.509696207e-05 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | shepp-logan | RMSE_HU | 68.648 | 68.6479591976 | -4.080236727e-05 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | shepp-logan | RMSE_HU | 95.403 | 95.4030583273 | 5.83273026e-05 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | cosine | RMSE_HU | 45.174 | 45.1744091433 | 0.00040914334709 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | cosine | RMSE_HU | 90.579 | 90.5786991133 | -0.00030088673302 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | cosine | RMSE_HU | 58.673 | 58.6732133816 | 0.00021338156539 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | cosine | RMSE_HU | 98.020 | 98.0204728025 | 0.00047280248594 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | hamming | RMSE_HU | 52.658 | 52.6583602626 | 0.00036026264943 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | hamming | RMSE_HU | 99.666 | 99.6658749447 | -0.00012505529067 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | hamming | RMSE_HU | 60.278 | 60.2776096624 | -0.00039033755678 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | hamming | RMSE_HU | 103.902 | 103.902482831 | 0.0004828313828 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | hann | RMSE_HU | 54.638 | 54.6384227712 | 0.0004227711734 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | hann | RMSE_HU | 102.789 | 102.789295278 | 0.00029527782884 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | hann | RMSE_HU | 60.983 | 60.9834217876 | 0.0004217876187 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | hann | RMSE_HU | 106.312 | 106.31161056 | -0.00038943965437 | 0.0005 | HU | Coincide |

### MAE, RMSE y máximo con Ramp

| Condición / etapa | Filtro | Métrica | Informe | Calculado | Diferencia calculado − informe | Tolerancia absoluta | Unidad | Estado |
|---|---|---|---:|---:|---:|---:|---|---|
| SDCT sin ruido añadido | ramp | MAE_HU | 22.925 | 22.9247765386 | -0.00022346135785 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | ramp | RMSE_HU | 31.890 | 31.8897236016 | -0.0002763984195 | 0.0005 | HU | Coincide |
| SDCT sin ruido añadido | ramp | MAX_HU | 355.433 | 355.433019643 | 1.964288213e-05 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | ramp | MAE_HU | 53.304 | 53.304137207 | 0.00013720695414 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | ramp | RMSE_HU | 68.899 | 68.8988501961 | -0.0001498038992 | 0.0005 | HU | Coincide |
| LDCT sin ruido añadido | ramp | MAX_HU | 446.964 | 446.964431308 | 0.00043130790243 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | ramp | MAE_HU | 62.676 | 62.6759609668 | -3.9033154214e-05 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | ramp | RMSE_HU | 78.906 | 78.9061103016 | 0.00011030157264 | 0.0005 | HU | Coincide |
| SDCT con ruido añadido | ramp | MAX_HU | 435.844 | 435.843698318 | -0.0003016819419 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | ramp | MAE_HU | 79.012 | 79.0119184418 | -8.155824312e-05 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | ramp | RMSE_HU | 99.700 | 99.7000405016 | 4.050161012e-05 | 0.0005 | HU | Coincide |
| LDCT con ruido añadido | ramp | MAX_HU | 612.323 | 612.322683946 | -0.0003160535344 | 0.0005 | HU | Coincide |

### DFT directa frente a FFT

| Condición / etapa | Filtro | Métrica | Informe | Calculado | Diferencia calculado − informe | Tolerancia absoluta | Unidad | Estado |
|---|---|---|---:|---:|---:|---:|---|---|
| reconstrucciones_HU | ramp | maximo | 3.342e-11 | 3.34239302902e-11 | 3.93029015511e-15 | 5e-15 | HU | Coincide |
| reconstrucciones_HU | ramp | media | 7.289e-13 | 7.28859680943e-13 | -4.03190570607e-17 | 5e-17 | HU | Coincide |
| reconstrucciones_HU | ramp | rmse | 9.590e-13 | 9.58998284218e-13 | -1.715781612e-18 | 5e-17 | HU | Coincide |
| sinogramas_filtrados | ramp | maximo | 8.69e-13 | 8.69304628281e-13 | 3.04628281498e-16 | 5e-16 | Suma Radon | Coincide |

Procedencia del recálculo (parámetros efectivos y hashes de entrada):

```json
{
  "parameters": {
    "num_angles": 512,
    "sigma_gaussian": 1.0,
    "seed": 42,
    "filter_name": "ramp",
    "visual_amplification": 5.0,
    "relative_threshold_fraction": 0.01,
    "relative_display_max_pct": 20.0,
    "fourier_atol": 1e-09,
    "fourier_rtol": 1e-10,
    "benchmark_sizes": [
      64,
      128,
      256,
      512,
      1024,
      2048
    ],
    "benchmark_repeats": 5,
    "photon_simulation": {
      "low_dose_fraction": 0.1,
      "config": {
        "calibration_a": 0.015,
        "calibration_b": 0.1002,
        "flux_per_mas": 1000.0,
        "incident_photons_per_mas": 2630.0,
        "projection_scale": 500.0,
        "gaussian_scale": 0.05,
        "count_floor": 1.0,
        "filter_name": "hann",
        "circle": false,
        "num_angles": null
      }
    }
  },
  "input_sha256": {
    "sdct": "86196a8ae87a0860c327542c47dfe756781f3b9346438c0a364e1fa54fa34013",
    "ldct": "0463186a016e9bddfd86617d56a435ae4fbb1655b8af9ccfea9b371db0259779"
  },
  "normalization_hu": [
    -1024.0,
    1616.0
  ],
  "image_shape": [
    512,
    512
  ],
  "padding_n": 2048,
  "ramp_validation_filter": "ramp",
  "equivalence_checks": {
    "filtrado_equivalente": true,
    "reconstruccion_equivalente": true,
    "geometria_y_filtro_equivalentes_al_pipeline": true
  }
}
```

## Discrepancias y causas

No se detectaron discrepancias fuera de la precisión publicada. Las diferencias con las cifras impresas corresponden al redondeo del informe. No se modificaron los cálculos científicos, parámetros, semillas ni resultados guardados para obtener coincidencias.

## Reproducción

Desde `hito1-mini-tesis/`:

```powershell
& ..\.venv\Scripts\python.exe -B validate.py --reference --recompute-reference --originals
```

Datos detallados: `outputs/tables/report_reference_validation.json`. La validación devuelve código de salida 1 si alguna cifra no coincide, después de guardar este informe.

