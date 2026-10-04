"""Figuras con ventanas compartidas; gráficos reutilizados por los notebooks."""
import html
import numpy as np
import matplotlib.pyplot as plt

from .filters import FILTER_LABELS


def show_table(rows, digits=6):
    """Tabla legible en Jupyter sin añadir pandas a las dependencias."""
    from IPython.display import HTML, display
    rows = list(rows)
    if not rows:
        return
    columns = list(rows[0])
    header = "".join(f"<th>{html.escape(k)}</th>" for k in columns)
    body = []
    for row in rows:
        values = [f"{row[k]:.{digits}g}" if isinstance(row[k], (float, np.floating)) else str(row[k])
                  for k in columns]
        body.append("<tr>" + "".join(f"<td>{html.escape(v)}</td>" for v in values) + "</tr>")
    display(HTML("<table><thead><tr>" + header + "</tr></thead><tbody>" + "".join(body) + "</tbody></table>"))


def image_panels(images, labels, *, limits=(0, 1), unit="Normalizado", title=""):
    fig, axes = plt.subplots(1, len(images), figsize=(5 * len(images), 5), layout="constrained", squeeze=False)
    for ax, image, label in zip(axes[0], images, labels):
        im = ax.imshow(image, cmap="gray", vmin=limits[0], vmax=limits[1], interpolation="nearest")
        ax.set_title(label)
        ax.axis("off")
    fig.colorbar(im, ax=axes[0].tolist(), shrink=0.8, label=unit)
    fig.suptitle(title)
    return fig


def plot_sinograms(sinograms, labels):
    limits = (min(float(s.min()) for s in sinograms), max(float(s.max()) for s in sinograms))
    fig, axes = plt.subplots(1, len(sinograms), figsize=(7 * len(sinograms), 5), layout="constrained", squeeze=False)
    for ax, sino, label in zip(axes[0], sinograms, labels):
        im = ax.imshow(sino, cmap="gray", vmin=limits[0], vmax=limits[1], aspect="auto",
                       extent=(0, 180, sino.shape[0], 0), interpolation="nearest")
        ax.set(title=label, xlabel="Ángulo (grados)", ylabel="Índice de detector")
    fig.colorbar(im, ax=axes[0].tolist(), shrink=0.8, label="Suma Radon")
    return fig


def plot_report(cases, sigma=1.0, amplification=5.0):
    limits = (min(float(c["sinogram"].min()) for c in cases),
              max(float(c["sinogram"].max()) for c in cases))
    figures = []
    for title, group in (("Sin ruido añadido (σ = 0)", cases[:2]),
                         (f"Con ruido gaussiano añadido (σ = {sigma:g})", cases[2:])):
        fig, axes = plt.subplots(2, 4, figsize=(19, 9), layout="constrained")
        for row, case in enumerate(group):
            image, sino, reconstruction = case["input"], case["sinogram"], case["reconstruction"]
            axes[row, 0].imshow(image, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
            axes[row, 0].set_title(case["label"] + "\nEntrada", fontsize=11)
            im = axes[row, 1].imshow(sino, cmap="gray", vmin=limits[0], vmax=limits[1], aspect="auto",
                                    extent=(0, 180, sino.shape[0], 0), interpolation="nearest")
            axes[row, 1].set(title="Sinograma utilizado", xlabel="Ángulo (grados)", ylabel="Índice de detector")
            fig.colorbar(im, ax=axes[row, 1], shrink=0.8, pad=0.02, label="Suma Radon")
            axes[row, 2].imshow(reconstruction, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
            axes[row, 2].set_title("Reconstrucción FBP · " + case["filter_name"])
            diff = axes[row, 3].imshow(np.abs(image - reconstruction), cmap="gray", vmin=0,
                                      vmax=1 / amplification, interpolation="nearest")
            axes[row, 3].set_title(f"|Entrada − reconstrucción| ×{amplification:g}")
            fig.colorbar(diff, ax=axes[row, 3], shrink=0.8, pad=0.02, label="Diferencia normalizada")
            for column in (0, 2, 3):
                axes[row, column].axis("off")
        fig.suptitle("Proyección y reconstrucción · " + title, fontsize=16)
        figures.append(fig)
    return figures


def plot_filter_comparison(cases, scale, amplification=5.0):
    fig, axes = plt.subplots(2, len(cases), figsize=(22, 9), layout="constrained", squeeze=False)
    for column, case in enumerate(cases):
        reconstruction = case["reconstruction"] * scale.range + scale.minimum
        error = np.abs(case["input"] - case["reconstruction"]) * scale.range
        im = axes[0, column].imshow(reconstruction, cmap="gray", vmin=scale.minimum, vmax=scale.maximum)
        axes[0, column].set_title(FILTER_LABELS[case["filter_name"]])
        diff = axes[1, column].imshow(error, cmap="gray", vmin=0, vmax=scale.range / amplification)
        axes[1, column].set_title(f"|Entrada − reconstrucción| ×{amplification:g}")
        for row in (0, 1):
            axes[row, column].axis("off")
    fig.colorbar(im, ax=axes[0].tolist(), shrink=0.8, pad=0.01, label="Reconstrucción (HU)")
    fig.colorbar(diff, ax=axes[1].tolist(), shrink=0.8, pad=0.01, label="Diferencia absoluta (HU)", extend="max")
    fig.suptitle("TCIA · " + cases[0]["label"] + " · Filtros FBP", fontsize=17)
    return fig


def plot_sinogram_comparison(a, b, labels, limits, *, amplification=5.0, relative=None, relative_max=20.0):
    fig, axes = plt.subplots(1, 3, figsize=(20, 5), layout="constrained")
    for ax, sino, label in zip(axes[:2], (a, b), labels):
        im = ax.imshow(sino, cmap="gray", vmin=limits[0], vmax=limits[1], aspect="auto",
                       extent=(0, 180, sino.shape[0], 0), interpolation="nearest")
        ax.set_title(label)
    fig.colorbar(im, ax=axes[:2].tolist(), shrink=0.8, label="Suma Radon")
    if relative is None:
        image, vmax, label = np.abs(a - b), (limits[1] - limits[0]) / amplification, "Diferencia (suma Radon)"
        cmap = "gray"
        axes[2].set_title(f"Diferencia absoluta ×{amplification:g}")
    else:
        from matplotlib.patches import Patch
        image, vmax, label = np.ma.masked_invalid(relative), relative_max, "Diferencia / |SDCT| (%)"
        cmap = plt.get_cmap("gray").copy()
        cmap.set_bad("#4c78a8")
        axes[2].set_title("Diferencia relativa respecto de SDCT (%)")
        axes[2].legend(handles=[Patch(color="#4c78a8", label="Referencia próxima a cero: excluida")],
                       loc="lower center", fontsize=8)
    diff = axes[2].imshow(image, cmap=cmap, vmin=0, vmax=max(vmax, np.finfo(float).eps),
                          aspect="auto", extent=(0, 180, a.shape[0], 0), interpolation="nearest")
    fig.colorbar(diff, ax=axes[2], shrink=0.8, label=label, extend="max")
    for ax in axes:
        ax.set(xlabel="Ángulo (grados)", ylabel="Índice de detector")
    return fig


def plot_fourier(original_hu, sinogram, dft_hu, fft_hu, scale):
    difference = np.abs(dft_hu - fft_hu)
    limit = max(float(difference.max()), np.finfo(float).eps)
    fig, axes = plt.subplots(2, 3, figsize=(18, 11), layout="constrained")
    axes = axes.ravel()
    for index, image, title in ((0, original_hu, "TCIA original"), (2, dft_hu, "FBP · DFT directa O(N²)"),
                                 (3, fft_hu, "FBP · FFT NumPy")):
        im = axes[index].imshow(image, cmap="gray", vmin=scale.minimum, vmax=scale.maximum)
        axes[index].set_title(title)
        axes[index].axis("off")
        fig.colorbar(im, ax=axes[index], shrink=0.8, label="HU")
    im = axes[1].imshow(sinogram, cmap="gray", aspect="auto", extent=(0, 180, sinogram.shape[0], 0))
    axes[1].set(title="Sinograma compartido", xlabel="Ángulo (grados)", ylabel="Índice de detector")
    fig.colorbar(im, ax=axes[1], shrink=0.8, label="Suma Radon")
    for index, factor in ((4, 1), (5, 5)):
        im = axes[index].imshow(factor * difference, cmap="gray", vmin=0, vmax=limit)
        axes[index].set_title("Diferencia absoluta DFT–FFT" + (" ×5 (solo visual)" if factor == 5 else ""))
        axes[index].axis("off")
        fig.colorbar(im, ax=axes[index], shrink=0.8, label="HU" if factor == 1 else "5 × diferencia (HU)")
    fig.suptitle(f"TCIA · Ramp · DFT directa frente a FFT\nMáxima diferencia real: {limit:.3e} HU; mapas autoescalados", fontsize=14)
    return fig


def save_figure(fig, path, *, dpi=180):
    fig.savefig(path, dpi=dpi, bbox_inches="tight")


def finish_figure(fig, path):
    """Exporta, muestra en Jupyter y libera memoria en ejecuciones sucesivas."""
    save_figure(fig, path)
    plt.show()
    plt.close(fig)

