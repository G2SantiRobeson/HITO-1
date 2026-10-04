"""DFT directa y FFT calculan la misma transformada, con el mismo filtro."""
from time import perf_counter
import numpy as np

from .filters import discrete_ramp
from .metrics import numerical_difference
from .reconstruction import backproject, reconstruct_fbp
from .validation import finite_array, positive_integer


def dft_matrix(n):
    n = positive_integer(n, "n")
    indices = np.arange(n, dtype=np.int64)
    phase = (indices[:, None] * indices[None, :]) % n
    return np.exp((-2j * np.pi / n) * phase)


def direct_dft(data, matrix):
    return matrix @ data


def direct_idft(spectrum, matrix):
    return (matrix.conj() @ spectrum) / matrix.shape[0]


def compare_fbp_transforms(sinogram, theta, output_size, *, atol=1e-9, rtol=1e-10):
    sinogram = finite_array(sinogram, ndim=2)
    detectors = sinogram.shape[0]
    n = max(64, int(2 ** np.ceil(np.log2(2 * detectors))))
    padded = np.pad(sinogram, ((0, n - detectors), (0, 0)))
    times = {}
    start = perf_counter()
    matrix = dft_matrix(n)
    ramp = discrete_ramp(n, matrix)
    times["matriz_y_filtro_comun_s"] = perf_counter() - start
    start = perf_counter()
    dft = direct_dft(padded, matrix)
    inverse_dft = direct_idft(dft * ramp, matrix)
    times["filtrado_dft_s"] = perf_counter() - start
    start = perf_counter()
    fft = np.fft.fft(padded, axis=0, norm="backward")
    inverse_fft = np.fft.ifft(fft * ramp, axis=0, norm="backward")
    times["filtrado_fft_s"] = perf_counter() - start
    filtered_dft, filtered_fft = inverse_dft.real[:detectors], inverse_fft.real[:detectors]
    start = perf_counter()
    reconstruction_dft = backproject(filtered_dft, theta, output_size)
    times["retroproyeccion_dft_s"] = perf_counter() - start
    start = perf_counter()
    reconstruction_fft = backproject(filtered_fft, theta, output_size)
    times["retroproyeccion_fft_s"] = perf_counter() - start
    reference = reconstruct_fbp(sinogram, theta, output_size=output_size, filter_name="ramp")
    measurements = {
        "espectros_complejos": numerical_difference(dft, fft),
        "sinogramas_filtrados": numerical_difference(filtered_dft, filtered_fft),
        "reconstrucciones_normalizadas": numerical_difference(reconstruction_dft, reconstruction_fft),
        "fft_vs_pipeline_normalizado": numerical_difference(reconstruction_fft, reference),
    }
    checks = {
        "filtrado_equivalente": bool(np.allclose(filtered_dft, filtered_fft, atol=atol, rtol=rtol)),
        "reconstruccion_equivalente": bool(np.allclose(reconstruction_dft, reconstruction_fft, atol=atol, rtol=rtol)),
        "geometria_y_filtro_equivalentes_al_pipeline": bool(np.allclose(reconstruction_fft, reference, atol=atol, rtol=rtol)),
    }
    return dict(reconstruction_dft=reconstruction_dft, reconstruction_fft=reconstruction_fft,
                filtered_dft=filtered_dft, filtered_fft=filtered_fft, ramp=ramp,
                frequencies=np.fft.fftfreq(n), padding_n=n, times=times, metrics=measurements,
                checks=checks, atol=atol, rtol=rtol,
                imaginary_residual={"dft": float(np.abs(inverse_dft.imag).max()),
                                    "fft": float(np.abs(inverse_fft.imag).max())})


def benchmark_projection(projection, sizes=(64, 128, 256, 512, 1024, 2048), repeats=5):
    """Diagnóstico de coste añadido al refactor: prefijos de una proyección real.

    Misma entrada por tamaño; mediana tras calentamiento. Construir la matriz
    queda fuera de la DFT medida y se informa aparte. No mide FBP completa.
    """
    projection = finite_array(projection, ndim=1)
    positive_integer(repeats, "repeats")
    rows = []
    for n in sizes:
        n = positive_integer(n, "n")
        data = np.pad(projection[:n], (0, max(0, n - projection.size)))
        start = perf_counter()
        matrix = dft_matrix(n)
        matrix_time = perf_counter() - start
        direct_dft(data, matrix)
        np.fft.fft(data)
        direct_times, fft_times = [], []
        for _ in range(repeats):
            start = perf_counter()
            result = direct_dft(data, matrix)
            direct_times.append(perf_counter() - start)
            start = perf_counter()
            fast_result = np.fft.fft(data)
            fft_times.append(perf_counter() - start)
        rows.append(dict(n=n, dft_median_s=float(np.median(direct_times)),
                         fft_median_s=float(np.median(fft_times)), matrix_s=matrix_time,
                         max_error=float(np.abs(result - fast_result).max()), repeats=repeats))
    return rows

