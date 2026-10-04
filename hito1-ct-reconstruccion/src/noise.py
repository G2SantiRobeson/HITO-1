"""Dos modelos históricos distintos: gaussiana post-Radon y ruido en conteos."""
from dataclasses import dataclass
import numpy as np

from .normalization import normalize_image, denormalize_image
from .radon import generate_sinogram, projection_angles
from .reconstruction import reconstruct_fbp
from .validation import finite_array, positive


def add_gaussian_noise(signal, sigma, rng):
    signal, sigma = finite_array(signal), finite_array(sigma)
    if (sigma < 0).any():
        raise ValueError("sigma debe ser no negativo.")
    return signal + rng.normal(0, np.broadcast_to(sigma, signal.shape), size=signal.shape)


def add_poisson_noise(expected_counts, rng):
    expected = finite_array(expected_counts)
    if (expected < 0).any():
        raise ValueError("Las medias Poisson deben ser no negativas.")
    return rng.poisson(expected).astype(np.float64)


@dataclass(frozen=True)
class SimulationConfig:
    """Valores originales de ldct/config.py; la calibración C095 es opcional."""
    calibration_a: float = 0.015
    calibration_b: float = 0.1002
    flux_per_mas: float = 1000.0
    incident_photons_per_mas: float | None = None
    projection_scale: float = 500.0
    gaussian_scale: float = 0.05
    count_floor: float = 1.0
    filter_name: str = "hann"
    circle: bool = True
    num_angles: int | None = None

    def __post_init__(self):
        for key in ("flux_per_mas", "projection_scale", "count_floor"):
            positive(getattr(self, key), key)
        if self.incident_photons_per_mas is not None:
            positive(self.incident_photons_per_mas, "incident_photons_per_mas")
        for key in ("calibration_a", "calibration_b", "gaussian_scale"):
            value = getattr(self, key)
            if not np.isfinite(value) or value < 0:
                raise ValueError(f"{key} debe ser finito y no negativo.")
        if self.filter_name not in ("ramp", "shepp-logan", "cosine", "hamming", "hann"):
            raise ValueError("Filtro desconocido.")
        if self.num_angles is not None:
            from .validation import positive_integer
            positive_integer(self.num_angles, "num_angles")


def tube_current_time_mas(ds):
    """mA × ExposureTime(ms)/1000; convención explícita de try_the_algorithm."""
    current, time = getattr(ds, "XRayTubeCurrent", None), getattr(ds, "ExposureTime", None)
    if current is None or time is None:
        raise ValueError("Faltan corriente o tiempo; no se inventa exposición.")
    return positive(current, "XRayTubeCurrent") * positive(time, "ExposureTime") / 1000


def incident_photon_count(source_mas, target_mas, config):
    source, target = positive(source_mas, "source_mas"), positive(target_mas, "target_mas")
    if target > source:
        raise ValueError("La exposición objetivo no puede superar la fuente.")
    if config.incident_photons_per_mas is not None:
        return positive(config.incident_photons_per_mas * target, "I0")
    return positive((config.calibration_a * target + config.calibration_b)
                    * source * config.flux_per_mas, "I0")


def transmitted_counts(projections, incident_count, projection_scale=500.0):
    return positive(incident_count) * np.exp(-finite_array(projections, ndim=2)
                                            / positive(projection_scale))


def counts_to_sinogram(counts, incident_count, projection_scale=500.0, count_floor=1.0):
    counts = finite_array(counts, ndim=2)
    floor = positive(count_floor)
    floored = int(np.count_nonzero(counts < floor))
    projections = -np.log(np.maximum(counts, floor) / positive(incident_count))
    return projections * positive(projection_scale), floored


def simulate_slice(image, source_mas, target_mas, *, noise="poisson", config=None, rng=None):
    """Reproduce ldct/pipeline.py, exponiendo además las etapas intermedias."""
    config = config or SimulationConfig()
    generator = np.random.default_rng(rng)
    normalized, info = normalize_image(image)
    theta = projection_angles(config.num_angles or max(normalized.shape))
    projections = generate_sinogram(normalized, theta, circle=config.circle)
    i0 = incident_photon_count(source_mas, target_mas, config)
    expected = transmitted_counts(projections, i0, config.projection_scale)
    counts = add_poisson_noise(expected, generator)
    if noise == "poisson_gaussian":
        counts = add_gaussian_noise(counts, np.sqrt(expected) * config.gaussian_scale, generator)
    elif noise != "poisson":
        raise ValueError("noise debe ser poisson o poisson_gaussian.")
    sino, floored = counts_to_sinogram(counts, i0, config.projection_scale, config.count_floor)
    reconstruction = reconstruct_fbp(sino, theta, output_size=normalized.shape[0],
                                     filter_name=config.filter_name, circle=config.circle)
    return dict(original_normalized=normalized, reconstruction_normalized=reconstruction,
                reconstruction=denormalize_image(reconstruction, info), normalization=info,
                sinogram=sino, theta=theta, incident_count=i0, floored_counts=floored,
                original_sinogram=projections, expected_counts=expected, noisy_counts=counts)

