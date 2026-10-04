"""Valida las métricas del informe y la equivalencia Fourier en este entorno.

La coincidencia literal de las cuatro diferencias de redondeo Fourier se
informa separadamente; no se presenta como una coincidencia con el informe.
Para exigir las 36 cifras publicadas, usar validate.py --reference.
"""
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def main():
    # Conserva los contratos numéricos y las verificaciones de los notebooks.
    subprocess.run([sys.executable, "-B", str(ROOT / "validate.py")], cwd=ROOT, check=True)
    from src.io import save_json
    from src.report_validation import evaluate_report_values, read_saved_results
    checks = evaluate_report_values(*read_saved_results())
    required = [c for c in checks if c["group"] != "fourier"]
    residuals = [c for c in checks if c["group"] == "fourier"]
    status = "passed" if len(required) == 32 and all(c["status"] == "passed" for c in required) else "failed"
    report = dict(status=status, published_metrics_passed=sum(c["status"] == "passed" for c in required),
                  published_metrics_total=32, metric_checks=required,
                  fourier_literal_checks=residuals,
                  note="La equivalencia Fourier se validó con validate.py. Las cuatro coincidencias literales se informan por separado y no se cuentan como aprobadas.")
    save_json(report, ROOT / "outputs/tables/portable_validation.json")
    print(f"Métricas publicadas: {report['published_metrics_passed']}/32; estado: {status}.")
    print(f"Coincidencias literales Fourier: {sum(c['status'] == 'passed' for c in residuals)}/4.")
    if status != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
