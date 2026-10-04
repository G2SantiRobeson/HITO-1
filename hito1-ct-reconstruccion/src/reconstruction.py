"""FBP pública y retroproyección explícita extraída del experimento DFT/FFT."""
import numpy as np
from skimage.transform import iradon

from .validation import finite_array, positive_integer


def reconstruct_fbp(sinogram, theta, *, output_size, filter_name="ramp", circle=False):
    sinogram, theta = finite_array(sinogram, ndim=2), finite_array(theta, ndim=1)
    if sinogram.shape[1] != theta.size:
        raise ValueError("El segundo eje del sinograma debe coincidir con theta.")
    return iradon(sinogram, theta=theta, output_size=positive_integer(output_size, "output_size"),
                  filter_name=filter_name, interpolation="linear", circle=circle, preserve_range=True)


def backproject(filtered_sinogram, theta, output_size):
    """Entrada ya filtrada; no filtra de nuevo. circle=False y π/(2*n_angles)."""
    sino, theta = finite_array(filtered_sinogram, ndim=2), finite_array(theta, ndim=1)
    size = positive_integer(output_size, "output_size")
    if sino.shape[1] != theta.size:
        raise ValueError("Eje angular incompatible.")
    xpr, ypr = np.mgrid[:size, :size] - size // 2
    detectors = np.arange(sino.shape[0]) - sino.shape[0] // 2
    result = np.zeros((size, size), dtype=np.float64)
    for projection, angle in zip(sino.T, np.deg2rad(theta)):
        t = ypr * np.cos(angle) - xpr * np.sin(angle)
        result += np.interp(t, detectors, projection, left=0, right=0)
    return result * np.pi / (2 * theta.size)

