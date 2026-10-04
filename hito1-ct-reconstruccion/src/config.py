"""Configuración central; rutas relativas al JSON y salidas dentro del Hito 1."""
import json
import math
import os
from pathlib import Path

from .validation import positive, positive_integer

ROOT = Path(__file__).resolve().parents[1]


def load_config(path=None):
    path = Path(path or os.environ.get("HITO1_CONFIG", ROOT / "config/default.json")).resolve()
    config = json.loads(path.read_text(encoding="utf-8"))
    for key in ("sdct", "ldct"):
        value = Path(config[key])
        config[key] = value.resolve() if value.is_absolute() else (path.parent / value).resolve()
    positive_integer(config["num_angles"], "num_angles")
    positive(config["visual_amplification"], "visual_amplification")
    if config["sigma_gaussian"] < 0 or not math.isfinite(config["sigma_gaussian"]):
        raise ValueError("sigma_gaussian debe ser finito y no negativo.")
    seed = config["seed"]
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("seed debe ser un entero no negativo.")
    if config["filter_name"] not in ("ramp", "shepp-logan", "cosine", "hamming", "hann"):
        raise ValueError("Filtro desconocido.")
    return config


def output_path(kind, name):
    if kind not in ("figures", "tables", "reconstructed_images"):
        raise ValueError("Categoría de salida desconocida.")
    path = (ROOT / "outputs" / kind / name).resolve()
    if not path.is_relative_to(ROOT / "outputs" / kind):
        raise ValueError("La salida debe permanecer dentro de su carpeta del Hito 1.")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

