"""Contraste con las cifras del informe actual, independiente de sus archivos históricos."""
from decimal import Decimal
import json
import math

from .config import ROOT, load_config
from .io import file_hash, load_table, save_json


def load_report_reference():
    return json.loads((ROOT / "config/report_reference.json").read_text(encoding="utf-8"))


def compare_rounded_value(reported, observed):
    """Media unidad del último decimal publicado; tolerancia relativa cero.

    Se conservan ceros finales y exponentes: 9.590e-13 implica 5e-17,
    mientras que 8.69e-13 implica 5e-16. No se usa el atol de allclose.
    """
    reference = Decimal(reported)
    tolerance = Decimal(1).scaleb(reference.as_tuple().exponent) / 2
    result = dict(reported=reported, observed=None, delta=None, atol=float(tolerance),
                  rtol=0, status="failed")
    try:
        value = float(observed)
    except (TypeError, ValueError):
        result["reason"] = "Valor ausente o no numérico."
        return result
    if not math.isfinite(value):
        result["reason"] = "Valor no finito."
        return result
    difference = Decimal(str(value)) - reference
    result.update(observed=value, delta=float(difference),
                  status="passed" if abs(difference) <= tolerance else "failed")
    if result["status"] == "failed":
        result["reason"] = "La diferencia supera media unidad del último decimal publicado."
    return result


def evaluate_report_values(filters, ramp, fourier, reference=None):
    reference = reference or load_report_reference()
    filter_rows = {(r["case"], r["filter"]): r for r in filters}
    ramp_rows = {r["case"]: r for r in ramp}
    checks = []
    for filter_name, values in reference["filter_rmse_hu"].items():
        for case, reported in zip(reference["case_order"], values):
            observed = filter_rows.get((case, filter_name), {}).get("RMSE_HU")
            checks.append(dict(group="filters", case=case, filter=filter_name, metric="RMSE_HU", unit="HU",
                               **compare_rounded_value(reported, observed)))
    for case, values in reference["ramp_metrics_hu"].items():
        for metric, reported in values.items():
            observed = ramp_rows.get(case, {}).get(metric)
            checks.append(dict(group="ramp", case=case, filter="ramp", metric=metric, unit="HU",
                               **compare_rounded_value(reported, observed)))
    for entry in reference["fourier"]:
        observed = fourier.get(entry["stage"], {}).get(entry["metric"])
        checks.append(dict(group="fourier", case=entry["stage"], filter="ramp", metric=entry["metric"],
                           unit=entry["unit"], **compare_rounded_value(entry["reported"], observed)))
    return checks


def read_saved_results():
    fourier = json.loads((ROOT / "outputs/tables/08_fourier.json").read_text(encoding="utf-8"))
    return (load_table(ROOT / "outputs/tables/07_filters.csv"),
            load_table(ROOT / "outputs/tables/09_report_metrics.csv"), fourier["metrics"])


def recompute_results(config):
    """Recalcula desde DICOM sin modificar ecuaciones, parámetros ni salidas previas."""
    from .experiments import prepare_pair, gaussian_conditions, reconstruct_conditions
    from .filters import FILTERS
    from .fourier import compare_fbp_transforms
    from .metrics import numerical_difference
    from .normalization import denormalize_image

    pair = prepare_pair(config)
    conditions = gaussian_conditions(pair, config)
    filters, by_filter = [], {}
    for filter_name in FILTERS:
        print(f"Recalculando FBP · {filter_name}", flush=True)
        cases = reconstruct_conditions(pair, conditions, filter_name)
        by_filter[filter_name] = cases
        filters.extend(dict(case=c["case"], filter=filter_name,
                            **{k: c[k] for k in ("MAE_HU", "RMSE_HU", "MAX_HU")}) for c in cases)
    # Estas doce referencias corresponden a Ramp, aunque se configure otro filtro.
    cases = by_filter["ramp"]
    ramp = [dict(case=c["case"], **{k: c[k] for k in ("MAE_HU", "RMSE_HU", "MAX_HU")}) for c in cases]
    print("Recalculando DFT directa frente a FFT", flush=True)
    result = compare_fbp_transforms(conditions[0]["sinogram"], pair["theta"], pair["sdct"].shape[0],
                                    atol=config["fourier_atol"], rtol=config["fourier_rtol"])
    metrics = result["metrics"]
    metrics["reconstrucciones_HU"] = numerical_difference(
        denormalize_image(result["reconstruction_dft"], pair["scale"]),
        denormalize_image(result["reconstruction_fft"], pair["scale"]))
    provenance = dict(parameters={k: v for k, v in config.items() if k not in ("sdct", "ldct")},
                      input_sha256={k: file_hash(config[k]) for k in ("sdct", "ldct")},
                      normalization_hu=[pair["scale"].minimum, pair["scale"].maximum],
                      image_shape=list(pair["sdct"].shape), padding_n=result["padding_n"],
                      ramp_validation_filter="ramp",
                      equivalence_checks=result["checks"])
    return (filters, ramp, metrics), provenance


def _format(value):
    return "ausente" if value is None else f"{value:.12g}"


def write_validation_report(report):
    reference = report["reference"]
    lines = ["# Validación contra los resultados del informe actual", "",
             f"**Referencia:** {reference['source']}", "",
             f"Valores proporcionados por el autor el {reference['provided_date']}. "
             "Las cadenas publicadas se conservan en `config/report_reference.json`.", "",
             "## Criterio de coincidencia", "",
             "Cada cifra se compara sin redondear el resultado calculado, usando tolerancia relativa cero "
             "y tolerancia absoluta igual a media unidad del último decimal publicado. "
             "Esto reconoce la precisión del informe; no supone igualdad con sus valores redondeados.", "",
             "- Métricas HU a tres decimales: 0.0005 HU.",
             "- Máximo entre reconstrucciones 3.342e-11: 5e-15 HU.",
             "- Media 7.289e-13 y RMSE 9.590e-13: 5e-17 HU.",
             "- Máximo entre sinogramas filtrados 8.69e-13: 5e-16 en suma Radon, **no HU**.", "",
             "Los umbrales anteriores son independientes de las tolerancias generales predeterminadas de equivalencia "
             "DFT/FFT (atol=1e-9, rtol=1e-10) del experimento. Esos umbrales generales "
             "no se usan para aprobar coincidencia con estas cifras publicadas.", "",
             "El orden de condiciones es SDCT sin ruido / LDCT sin ruido / SDCT con ruido / LDCT con ruido. "
             "Aquí ‘sin ruido’ significa sin ruido añadido y conserva el ruido del dataset.", ""]
    for batch in report["batches"]:
        checks = batch["checks"]
        passed = sum(c["status"] == "passed" for c in checks)
        lines.extend([f"## {batch['label']}", "", f"**Resultado: {passed}/{len(checks)} coincidencias.**", ""])
        if batch.get("error"):
            lines.extend([f"Error de ejecución/lectura: `{batch['error']}`", ""])
        for group, title in (("filters", "RMSE por filtro"), ("ramp", "MAE, RMSE y máximo con Ramp"),
                             ("fourier", "DFT directa frente a FFT")):
            lines.extend([f"### {title}", "",
                          "| Condición / etapa | Filtro | Métrica | Informe | Calculado | Diferencia calculado − informe | Tolerancia absoluta | Unidad | Estado |",
                          "|---|---|---|---:|---:|---:|---:|---|---|"])
            for check in (c for c in checks if c["group"] == group):
                label = reference["case_labels"].get(check["case"], check["case"])
                lines.append(f"| {label} | {check['filter']} | {check['metric']} | {check['reported']} | "
                             f"{_format(check['observed'])} | {_format(check['delta'])} | "
                             f"{_format(check['atol'])} | {check['unit']} | "
                             f"{'Coincide' if check['status'] == 'passed' else 'DISCREPANCIA'} |")
            lines.append("")
        if batch.get("provenance"):
            lines.extend(["Procedencia del recálculo (parámetros efectivos y hashes de entrada):", "", "```json",
                          json.dumps(batch["provenance"], ensure_ascii=False, indent=2), "```", ""])
    failures = [(batch["label"], c) for batch in report["batches"] for c in batch["checks"] if c["status"] != "passed"]
    lines.extend(["## Discrepancias y causas", ""])
    if not failures:
        lines.append("No se detectaron discrepancias fuera de la precisión publicada. "
                     "Las diferencias con las cifras impresas corresponden al redondeo del informe. "
                     "No se modificaron los cálculos científicos, parámetros, semillas ni resultados guardados para obtener coincidencias.")
    else:
        for batch, check in failures:
            lines.append(f"- {batch}: {check['case']} / {check['filter']} / {check['metric']}: "
                         f"{check.get('reason', 'fuera de tolerancia')}")
        lines.extend(["", "No se ajusta el código para forzar coincidencias. Antes de cambiar el modelo se deben "
                      "contrastar hashes de entrada, normalización HU compartida, semilla y orden de generadores, "
                      "filtro, número de ángulos y geometría. Para Fourier también se deben revisar padding, "
                      "Ramp discreto, escala de la inversa, orden de frecuencias, versión NumPy/BLAS e interpolación. "
                      "El detalle disponible de lectura/recálculo y sus parámetros efectivos aparece arriba; "
                      "una diferencia numérica sola no demuestra cuál de estas causas produjo el fallo."])
    if len(report["batches"]) == 1:
        lines.extend(["", "Esta ejecución compara salidas guardadas. Usa `--recompute-reference` junto con "
                      "`--reference` para ejecutar también los cálculos desde los DICOM."])
    lines.extend(["", "## Reproducción", "", "Desde la raíz del repositorio:", "", "```powershell",
                  "& .\\.venv\\Scripts\\python.exe -B validate.py --reference --recompute-reference",
                  "```", "", "Datos detallados: `outputs/tables/report_reference_validation.json`. "
                  "La validación devuelve código de salida 1 si alguna cifra no coincide, después de guardar este informe.", ""])
    (ROOT / "VALIDATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def validate_current_report(*, recompute=False):
    reference = load_report_reference()
    batches = []
    for mode, label in (("saved", "Salidas guardadas de los notebooks 07, 08 y 09"),
                        ("recomputed", "Recálculo independiente desde los DICOM")):
        if mode == "recomputed" and not recompute:
            continue
        batch = dict(mode=mode, label=label)
        try:
            if mode == "saved":
                values = read_saved_results()
            else:
                values, batch["provenance"] = recompute_results(load_config())
            batch["checks"] = evaluate_report_values(*values, reference=reference)
        except (OSError, ValueError, KeyError, AssertionError) as error:
            batch["error"] = f"{type(error).__name__}: {error}"
            batch["checks"] = evaluate_report_values([], [], {}, reference=reference)
        batches.append(batch)
    checks = [check for batch in batches for check in batch["checks"]]
    summary = dict(status="passed" if all(c["status"] == "passed" for c in checks) else "failed",
                   reference_values=36, comparisons=len(checks),
                   passed=sum(c["status"] == "passed" for c in checks),
                   failed=sum(c["status"] != "passed" for c in checks),
                   sources=[batch["mode"] for batch in batches], report="VALIDATION_REPORT.md")
    report = dict(reference=reference, summary=summary, batches=batches)
    save_json(report, ROOT / "outputs/tables/report_reference_validation.json")
    write_validation_report(report)
    return summary

