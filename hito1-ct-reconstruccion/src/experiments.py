"""Recorridos pequeños compartidos por los notebooks; sin I/O de resultados."""
import numpy as np

from .io import load_ct_pair
from .metrics import error_metrics
from .noise import add_gaussian_noise
from .normalization import normalize_image, normalize_with_reference
from .radon import generate_sinogram, projection_angles
from .reconstruction import reconstruct_fbp


def prepare_pair(config):
    sd, ld, sd_hu, ld_hu = load_ct_pair(config["sdct"], config["ldct"])
    sdct, scale = normalize_image(sd_hu)
    ldct = normalize_with_reference(ld_hu, scale)
    return dict(sdct_dcm=sd, ldct_dcm=ld, sdct_hu=sd_hu, ldct_hu=ld_hu,
                sdct=sdct, ldct=ldct, scale=scale, theta=projection_angles(config["num_angles"]))


def gaussian_conditions(pair, config):
    """Preserva SeedSequence(seed).spawn(2), sus ejes y el orden de las ramas."""
    sd = generate_sinogram(pair["sdct"], pair["theta"])
    ld = generate_sinogram(pair["ldct"], pair["theta"])
    seeds = np.random.SeedSequence(config["seed"]).spawn(2)
    sd_noise = add_gaussian_noise(sd, config["sigma_gaussian"], np.random.default_rng(seeds[0]))
    ld_noise = add_gaussian_noise(ld, config["sigma_gaussian"], np.random.default_rng(seeds[1]))
    names = ("sdct_sin_ruido", "ldct_sin_ruido", "sdct_gaussiano", "ldct_gaussiano")
    labels = ("SDCT · sin ruido añadido", "LDCT dataset · sin ruido añadido",
              "SDCT · gaussiano añadido", "LDCT dataset · gaussiano añadido")
    return [dict(case=name, label=label, input=pair[key], sinogram=sino)
            for name, label, key, sino in zip(names, labels, ("sdct", "ldct", "sdct", "ldct"),
                                             (sd, ld, sd_noise, ld_noise))]


def reconstruct_conditions(pair, conditions, filter_name="ramp"):
    result = []
    for condition in conditions:
        reconstruction = reconstruct_fbp(condition["sinogram"], pair["theta"],
                                         output_size=pair["sdct"].shape[0], filter_name=filter_name)
        # Restar ANTES de volver a HU preserva exactamente Hito-1/reproducir.py.
        error_hu = (condition["input"] - reconstruction) * pair["scale"].range
        measurements = error_metrics(error_hu, np.zeros_like(error_hu), suffix="_HU")
        result.append(dict(condition, reconstruction=reconstruction, filter_name=filter_name,
                           **measurements))
    return result


def report_experiment(config):
    pair = prepare_pair(config)
    return pair, reconstruct_conditions(pair, gaussian_conditions(pair, config), config["filter_name"])


def sinogram_comparisons(conditions):
    sd, ld, sd_noise, ld_noise = (c["sinogram"] for c in conditions)
    return [("sdct_ldct_sin_ruido", sd, ld, "SDCT", "LDCT"),
            ("sdct_ldct_con_ruido", sd_noise, ld_noise, "SDCT + gaussiano", "LDCT + gaussiano"),
            ("sdct_sin_vs_con_ruido", sd, sd_noise, "SDCT", "SDCT + gaussiano"),
            ("ldct_sin_vs_con_ruido", ld, ld_noise, "LDCT", "LDCT + gaussiano")]

