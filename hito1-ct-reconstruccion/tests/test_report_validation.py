"""La precisión publicada y los fallos no deben perderse por tolerancias genéricas."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from src.report_validation import compare_rounded_value, evaluate_report_values, load_report_reference, recompute_results, validate_current_report


class ReportValidation(unittest.TestCase):
    def test_published_precision_preserves_trailing_zeroes(self):
        self.assertEqual(compare_rounded_value("31.890", 31.8905)["status"], "passed")
        self.assertEqual(compare_rounded_value("31.890", 31.890500001)["status"], "failed")
        self.assertEqual(compare_rounded_value("9.590e-13", 9.58998284218388e-13)["atol"], 5e-17)
        self.assertEqual(compare_rounded_value("8.69e-13", 8.693046282814976e-13)["atol"], 5e-16)

    def test_zero_fourier_difference_does_not_match_nonzero_published_value(self):
        # np.allclose con su atol por defecto aceptaría cero; aquí debe fallar.
        for entry in load_report_reference()["fourier"]:
            self.assertEqual(compare_rounded_value(entry["reported"], 0)["status"], "failed")
        for value in (None, float("nan"), float("inf")):
            self.assertEqual(compare_rounded_value("31.890", value)["status"], "failed")

    def test_missing_results_are_all_reported_before_failure(self):
        checks = evaluate_report_values([], [], {})
        self.assertEqual(len(checks), 36)
        self.assertTrue(all(check["status"] == "failed" for check in checks))
        with patch("src.report_validation.read_saved_results", side_effect=FileNotFoundError("resultado ausente")), \
                patch("src.report_validation.save_json") as save, \
                patch("src.report_validation.write_validation_report") as write:
            summary = validate_current_report()
        self.assertEqual(summary["status"], "failed")
        self.assertEqual(summary["failed"], 36)
        save.assert_called_once()
        write.assert_called_once()
        self.assertIn("resultado ausente", write.call_args.args[0]["batches"][0]["error"])

    def test_ramp_reference_keeps_its_filter_when_another_filter_is_configured(self):
        array = np.zeros((2, 2))
        pair = dict(sdct=array, theta=np.zeros(2), scale=SimpleNamespace(minimum=0, maximum=1))
        config = dict(sdct="sdct.dcm", ldct="ldct.dcm", filter_name="cosine",
                      fourier_atol=1e-9, fourier_rtol=1e-10)

        def reconstruct(pair, conditions, filter_name):
            value = 1.0 if filter_name == "ramp" else 99.0
            return [dict(case="sdct_sin_ruido", MAE_HU=value, RMSE_HU=value, MAX_HU=value)]

        fourier = dict(metrics={}, reconstruction_dft=array, reconstruction_fft=array,
                       padding_n=4, checks={})
        with patch("src.experiments.prepare_pair", return_value=pair), \
                patch("src.experiments.gaussian_conditions", return_value=[dict(sinogram=array)]), \
                patch("src.experiments.reconstruct_conditions", side_effect=reconstruct), \
                patch("src.fourier.compare_fbp_transforms", return_value=fourier), \
                patch("src.normalization.denormalize_image", side_effect=lambda image, scale: image), \
                patch("src.report_validation.file_hash", return_value="hash de prueba"):
            (filters, ramp, _), provenance = recompute_results(config)
        self.assertEqual(ramp[0]["RMSE_HU"], 1.0)
        self.assertEqual(next(row for row in filters if row["filter"] == "cosine")["RMSE_HU"], 99.0)
        self.assertEqual(provenance["ramp_validation_filter"], "ramp")


if __name__ == "__main__":
    unittest.main()
