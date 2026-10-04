"""Contratos numéricos compartidos del código histórico ldct/validation.py."""
import numpy as np


def finite_array(value, *, ndim=None):
    array = np.asarray(value, dtype=np.float64)
    if not array.size or (ndim is not None and array.ndim != ndim):
        raise ValueError(f"Se requiere un array no vacío de {ndim or 'N'} dimensiones.")
    if not np.isfinite(array).all():
        raise ValueError("El array contiene NaN o infinito.")
    return array


def positive(value, name="valor"):
    value = float(value)
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} debe ser finito y positivo.")
    return value


def positive_integer(value, name="valor"):
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < 1:
        raise ValueError(f"{name} debe ser un entero positivo.")
    return int(value)

