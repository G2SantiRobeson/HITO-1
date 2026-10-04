"""Proyecciones en ejes (detector, ángulo), theta en grados, campo completo."""
import numpy as np
from skimage.transform import radon

from .validation import finite_array, positive_integer


def projection_angles(num_angles):
    return np.linspace(0, 180, positive_integer(num_angles, "num_angles"), endpoint=False)


def generate_sinogram(image, theta, *, circle=False):
    image, theta = finite_array(image, ndim=2), finite_array(theta, ndim=1)
    if image.shape[0] != image.shape[1]:
        raise ValueError("Se requiere un corte cuadrado; no se remuestrea implícitamente.")
    return radon(image, theta=theta, circle=circle, preserve_range=True)

