"""Métricas del informe; nunca usan amplificación ni recorte de contraste."""
import numpy as np

from .validation import finite_array


def error_metrics(reference, reconstruction, *, suffix=""):
    a, b = finite_array(reference), finite_array(reconstruction)
    if a.shape != b.shape:
        raise ValueError("Las formas deben coincidir.")
    error = a - b
    return {"MAE" + suffix: float(np.abs(error).mean()),
            "RMSE" + suffix: float(np.sqrt(np.mean(error ** 2))),
            "MAX" + suffix: float(np.abs(error).max())}


def numerical_difference(a, b):
    """Admite espectros complejos; se mide la magnitud de su diferencia."""
    a, b = np.asarray(a), np.asarray(b)
    if a.shape != b.shape or not a.size or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("Arrays incompatibles o no finitos.")
    error = np.abs(a - b)
    return dict(maximo=float(error.max()), media=float(error.mean()),
                rmse=float(np.sqrt(np.mean(error ** 2))))


def relative_sinogram_difference(a, b, reference, threshold_fraction=0.01):
    """Denominador SDCT fijo; NaN en señal <=1 % del máximo, como el notebook."""
    a, b, reference = (finite_array(x, ndim=2) for x in (a, b, reference))
    if a.shape != b.shape or a.shape != reference.shape:
        raise ValueError("Formas incompatibles.")
    if not 0 < threshold_fraction < 1:
        raise ValueError("El umbral debe estar entre 0 y 1.")
    reference = np.abs(reference)
    mask = reference > threshold_fraction * reference.max()
    if not mask.any():
        raise ValueError("No hay señal evaluable.")
    relative = np.full(reference.shape, np.nan)
    np.divide(100 * np.abs(a - b), reference, out=relative, where=mask)
    values = relative[mask]
    return relative, dict(media_pct=float(values.mean()), mediana_pct=float(np.median(values)),
                          maximo_pct=float(values.max()), evaluado_pct=float(100 * mask.mean()))

