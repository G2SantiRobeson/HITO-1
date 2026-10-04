"""Filtros efectivamente usados; Ramp discreto del experimento histórico."""
import numpy as np

FILTERS = ("ramp", "shepp-logan", "cosine", "hamming", "hann")
FILTER_LABELS = dict(zip(FILTERS, ("Ramp / Ram-Lak", "Shepp–Logan", "Cosine", "Hamming", "Hann")))


def discrete_ramp(n, dft_matrix):
    """DFT explícita del kernel discreto; no reemplazar por 2*abs(fftfreq)."""
    if n < 2 or n % 2 or dft_matrix.shape != (n, n):
        raise ValueError("El Ramp requiere tamaño par y matriz DFT compatible.")
    odd = np.concatenate((np.arange(1, n // 2 + 1, 2), np.arange(n // 2 - 1, 0, -2)))
    kernel = np.zeros(n, dtype=np.float64)
    kernel[0] = 0.25
    kernel[1::2] = -1 / (np.pi * odd) ** 2
    return 2 * np.real(dft_matrix @ kernel)[:, None]

