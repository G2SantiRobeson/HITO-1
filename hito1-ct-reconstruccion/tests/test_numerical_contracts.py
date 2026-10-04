"""Contrastes científicos independientes; unittest evita dependencias de test."""
import unittest
from dataclasses import replace
import numpy as np
from skimage.transform import iradon

from src.filters import discrete_ramp
from src.fourier import dft_matrix, direct_dft, direct_idft
from src.noise import SimulationConfig, counts_to_sinogram, incident_photon_count, simulate_slice
from src.normalization import normalize_image, denormalize_image
from src.radon import generate_sinogram, projection_angles
from src.reconstruction import backproject
from src.metrics import relative_sinogram_difference


class NumericalContracts(unittest.TestCase):
    def test_dft_complex_signal_and_inverse(self):
        rng = np.random.default_rng(31)
        data = rng.normal(size=(64, 3)) + 1j * rng.normal(size=(64, 3))
        matrix = dft_matrix(64)
        np.testing.assert_allclose(direct_dft(data, matrix), np.fft.fft(data, axis=0), atol=1e-12)
        np.testing.assert_allclose(direct_idft(direct_dft(data, matrix), matrix), data, atol=1e-12)

    def test_explicit_filter_and_backprojection_against_public_iradon(self):
        # Imagen asimétrica: detecta inversiones de ejes/centros que un disco ocultaría.
        image = np.zeros((40, 40)); image[9:17, 23:31] = 0.7; image[25:28, 10:22] = 1
        theta = projection_angles(57)
        sinogram = generate_sinogram(image, theta)
        n = max(64, int(2 ** np.ceil(np.log2(2 * sinogram.shape[0]))))
        padded = np.pad(sinogram, ((0, n - sinogram.shape[0]), (0, 0)))
        filtered = np.fft.ifft(np.fft.fft(padded, axis=0) * discrete_ramp(n, dft_matrix(n)), axis=0).real
        actual = backproject(filtered[:sinogram.shape[0]], theta, 40)
        expected = iradon(sinogram, theta=theta, output_size=40, filter_name="ramp", circle=False)
        np.testing.assert_allclose(actual, expected, atol=1e-12)

    def test_count_floor_precedes_logarithm_and_keeps_negative_projections(self):
        with np.errstate(all="raise"):
            sinogram, floored = counts_to_sinogram([[0, -2, 100, 110]], 100)
        self.assertEqual(floored, 2)
        self.assertGreater(sinogram[0, 0], 0)
        self.assertEqual(sinogram[0, 2], 0)
        self.assertLess(sinogram[0, 3], 0)

    def test_two_calibration_paths_remain_distinct(self):
        empirical = SimulationConfig()
        calibrated = replace(empirical, incident_photons_per_mas=2630)
        self.assertAlmostEqual(incident_photon_count(51.87, 5.187, empirical),
                               (0.015 * 5.187 + 0.1002) * 51.87 * 1000)
        self.assertAlmostEqual(incident_photon_count(51.87, 5.187, calibrated), 2630 * 5.187)

    def test_poisson_gaussian_zero_scale_and_original_intensity_restoration(self):
        image = np.arange(1024).reshape(32, 32) + 100
        config = SimulationConfig(circle=False, gaussian_scale=0)
        poisson = simulate_slice(image, 50, 5, config=config, rng=42)
        combined = simulate_slice(image, 50, 5, config=config, rng=42, noise="poisson_gaussian")
        np.testing.assert_array_equal(poisson["sinogram"], combined["sinogram"])
        np.testing.assert_allclose(poisson["reconstruction"],
                                   poisson["reconstruction_normalized"] * 1023 + 100)

    def test_normalization_preserves_overshoot_and_constant_source(self):
        normalized, scale = normalize_image([[100, 200]])
        np.testing.assert_array_equal(normalized, [[0, 1]])
        np.testing.assert_array_equal(denormalize_image([[-0.2, 1.2]], scale), [[80, 220]])
        normalized, scale = normalize_image(np.full((3, 3), 7))
        np.testing.assert_array_equal(denormalize_image(normalized, scale), np.full((3, 3), 7))

    def test_relative_difference_excludes_zero_reference(self):
        relative, stats = relative_sinogram_difference([[0, 4]], [[1, 6]], [[0, 4]])
        self.assertTrue(np.isnan(relative[0, 0]))
        self.assertEqual(relative[0, 1], 50)
        self.assertEqual(stats["evaluado_pct"], 50)


if __name__ == "__main__":
    unittest.main()

