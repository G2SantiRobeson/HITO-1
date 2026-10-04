"""Lectura de CT clásico y exportación de tablas/arrays, sin escribir DICOM."""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import pydicom
from pydicom.uid import CTImageStorage

from .validation import finite_array


def read_ct(path):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Falta el DICOM {path}. Configura config/default.json o HITO1_CONFIG.")
    ds = pydicom.dcmread(path)
    if (str(ds.SOPClassUID) != str(CTImageStorage)
            or int(getattr(ds, "NumberOfFrames", 1)) != 1
            or int(ds.SamplesPerPixel) != 1
            or ds.PhotometricInterpretation != "MONOCHROME2"):
        raise ValueError("Se requiere CT clásico de un corte, MONOCHROME2.")
    return ds


def modality_values(ds, pixels=None):
    if "ModalityLUTSequence" in ds:
        raise ValueError("Este recorrido no admite ModalityLUTSequence.")
    values = finite_array(ds.pixel_array if pixels is None else pixels)
    return finite_array(values * float(getattr(ds, "RescaleSlope", 1))
                        + float(getattr(ds, "RescaleIntercept", 0)))


def load_ct_pair(sdct_path, ldct_path):
    sd, ld = read_ct(sdct_path), read_ct(ldct_path)
    a, b = modality_values(sd), modality_values(ld)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or a.shape != b.shape:
        raise ValueError("Los cortes deben ser cuadrados y tener las mismas dimensiones.")
    for key in ("ImagePositionPatient", "ImageOrientationPatient", "PixelSpacing"):
        if not hasattr(sd, key) or not hasattr(ld, key):
            raise ValueError(f"Falta {key}; no se puede verificar el par.")
        x, y = np.asarray(getattr(sd, key), dtype=float), np.asarray(getattr(ld, key), dtype=float)
        if not np.isfinite(x).all() or x.shape != y.shape or not np.allclose(x, y, rtol=0, atol=1e-4):
            raise ValueError(f"SDCT y LDCT no coinciden en {key}.")
    return sd, ld, a, b


def file_hash(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save_table(rows, path):
    rows = list(rows)
    if not rows:
        raise ValueError("No hay filas para exportar.")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_table(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def save_json(value, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")

