"""Verifica el informe actual, cifras históricas y la integridad de los originales."""
import argparse
import json
import sys
import unittest

sys.dont_write_bytecode = True
import numpy as np
import nbformat
from src.config import ROOT, load_config
from src.io import file_hash, load_table, save_json
from src.report_validation import load_report_reference, compare_rounded_value, validate_current_report


def verify_published_metrics(rows):
    expected = load_report_reference()["ramp_metrics_hu"]
    by_case = {row["case"]: row for row in rows}
    for case, metrics in expected.items():
        for metric, reported in metrics.items():
            check = compare_rounded_value(reported, by_case.get(case, {}).get(metric))
            if check["status"] != "passed":
                raise AssertionError(f"No coincide con el informe actual: {case} {metric}: {check}")
    return 12


def verify_original_integrity():
    manifest_path = ROOT / "outputs/tables/original_manifest.json"
    if not manifest_path.is_file():
        return dict(status="unavailable", reason="No hay manifiesto de la auditoría inicial.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    changed = []
    for entry in manifest["files"]:
        path = ROOT.parent / entry["path"]
        if not path.is_file() or file_hash(path) != entry["sha256"]:
            changed.append(entry["path"])
    if changed:
        raise AssertionError("Originales modificados o ausentes: " + ", ".join(changed))
    return dict(status="passed", checked_files=len(manifest["files"]),
                inaccessible_folders=len(manifest["inaccessible"]),
                excluded=".git, entornos virtuales, node_modules, cachés Python/pytest y egg-info")


def verify_historical_filters():
    original = ROOT.parent / "codigo-camila-bluemili/ldct_simulation-main/ldct_simulation-main/resultados/comparacion_filtros_tcia/metricas_filtros.csv"
    if not original.is_file():
        return dict(status="unavailable", reason="CSV histórico ausente.")
    expected = load_table(original)
    actual = {(r["case"], r["filter"]): r for r in load_table(ROOT / "outputs/tables/07_filters.csv")}
    for row in expected:
        for metric in ("MAE_HU", "RMSE_HU", "MAX_HU"):
            np.testing.assert_allclose(float(actual[row["caso"], row["filtro"]][metric]), float(row[metric]),
                                       atol=1e-9, rtol=1e-12)
    return dict(status="passed", rows=len(expected), values=3 * len(expected))


def verify_historical_photons():
    historical = ROOT.parent / "codigo-camila-bluemili/ldct_simulation-main/ldct_simulation-main"
    if not (historical / "ldct/pipeline.py").is_file():
        return dict(status="unavailable", reason="Núcleo histórico ausente.")
    sys.path.insert(0, str(historical))
    from ldct import SimulationConfig, simulate_slice
    from src.io import read_ct
    config = load_config()
    ds = read_ct(config["sdct"])
    from src.noise import tube_current_time_mas
    source = tube_current_time_mas(ds)
    target = source * config["photon_simulation"]["low_dose_fraction"]
    settings = SimulationConfig(**config["photon_simulation"]["config"])
    saved = np.load(ROOT / "outputs/reconstructed_images/04_photons.npz")
    for name in ("poisson", "poisson_gaussian"):
        result = simulate_slice(ds.pixel_array, source, target, noise=name, config=settings, rng=config["seed"])
        np.testing.assert_array_equal(saved[name + "_sinogram"], result.sinogram)
        np.testing.assert_array_equal(saved[name + "_reconstruction"], result.reconstruction_normalized)
    return dict(status="passed", models=["poisson", "poisson_gaussian"], parity="exact")


def verify_historical_fourier():
    original = ROOT.parent / "results/fourier_vs_fft_tcia/arrays_dft_fft.npz"
    if not original.is_file():
        return dict(status="unavailable", reason="Arrays Fourier históricos ausentes.")
    keys = {"dft_hu": "reconstruccion_dft_hu", "fft_hu": "reconstruccion_fft_hu",
            "filtered_dft": "filtrado_dft", "filtered_fft": "filtrado_fft",
            "sinogram": "sinograma", "ramp": "filtro_ramp", "frequencies": "frecuencias", "theta": "theta"}
    with np.load(original) as expected, np.load(ROOT / "outputs/reconstructed_images/08_dft_fft.npz") as actual:
        for new_key, old_key in keys.items():
            np.testing.assert_allclose(actual[new_key], expected[old_key], atol=1e-9, rtol=1e-12)
    return dict(status="passed", arrays=len(keys), atol=1e-9, rtol=1e-12)


def verify_notebooks():
    rows = []
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        code = [c for c in nb.cells if c.cell_type == "code"]
        if any(c.execution_count is None for c in code):
            raise AssertionError(f"Notebook pendiente de ejecución: {path.name}")
        errors = [o for c in code for o in c.outputs if o.output_type == "error"]
        if errors:
            raise AssertionError(f"Errores en {path.name}")
        figures = sum("image/png" in o.get("data", {}) for c in code for o in c.outputs)
        if not figures:
            raise AssertionError(f"No se visualizaron figuras en {path.name}")
        rows.append(dict(notebook=path.name, code_cells=len(code), inline_figures=figures))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", action="store_true", help="Contrasta las 36 cifras del informe actual y las referencias históricas; requiere C095/1-250.")
    parser.add_argument("--recompute-reference", action="store_true", help="Con --reference, recalcula filtros, Ramp y DFT/FFT desde los DICOM sin reemplazar salidas científicas.")
    parser.add_argument("--originals", action="store_true", help="Contrasta todos los hashes de la auditoría.")
    args = parser.parse_args()
    if args.recompute_reference and not args.reference:
        parser.error("--recompute-reference requiere --reference.")
    current_report = validate_current_report(recompute=args.recompute_reference) if args.reference else None
    if current_report and current_report["status"] != "passed":
        save_json({"current_report": current_report}, ROOT / "outputs/tables/validation.json")
        print("Discrepancias registradas en VALIDATION_REPORT.md; no se ajustaron los cálculos.")
        raise SystemExit(1)
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    report = dict(numerical_tests=result.testsRun, notebooks=verify_notebooks())
    fourier = json.loads((ROOT / "outputs/tables/08_fourier.json").read_text(encoding="utf-8"))
    if not all(fourier["checks"].values()):
        raise AssertionError("Falló la equivalencia DFT/FFT o su control contra iradon.")
    report["fourier_checks"] = fourier["checks"]
    report["exported_figures"] = len(list((ROOT / "outputs/figures").glob("*.png")))
    if args.reference:
        report["current_report"] = current_report
        report["published_values"] = verify_published_metrics(load_table(ROOT / "outputs/tables/09_report_metrics.csv"))
        report["historical_filters"] = verify_historical_filters()
        report["historical_photons"] = verify_historical_photons()
        report["historical_fourier"] = verify_historical_fourier()
    if args.originals:
        report["original_integrity"] = verify_original_integrity()
    save_json(report, ROOT / "outputs/tables/validation.json")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

