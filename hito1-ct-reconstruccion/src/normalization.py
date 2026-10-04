"""Min–max invertible; conserva la escala original y el overshoot de FBP."""
from dataclasses import dataclass
import numpy as np

from .validation import finite_array


@dataclass(frozen=True)
class NormalizationInfo:
    minimum: float
    maximum: float

    def __post_init__(self):
        if not np.isfinite([self.minimum, self.maximum]).all() or self.maximum < self.minimum:
            raise ValueError("Límites de normalización inválidos.")

    @property
    def range(self):
        return self.maximum - self.minimum


def normalize_image(image):
    image = finite_array(image)
    info = NormalizationInfo(float(image.min()), float(image.max()))
    return ((image - info.minimum) / info.range if info.range else np.zeros_like(image)), info


def normalize_with_reference(image, info):
    if info.range == 0:
        raise ValueError("La referencia es constante; no permite una escala compartida.")
    return (finite_array(image) - info.minimum) / info.range


def denormalize_image(image, info):
    return finite_array(image) * info.range + info.minimum

