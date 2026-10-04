"""Ejecuta los notebooks en kernels nuevos usando este mismo intérprete Python."""
import argparse
import os
from pathlib import Path
import sys
from time import perf_counter

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
for name, folder in (("JUPYTER_RUNTIME_DIR", ".jupyter"), ("IPYTHONDIR", ".ipython"),
                     ("MPLCONFIGDIR", ".matplotlib")):
    os.environ[name] = str(ROOT / "outputs" / folder)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import nbformat
from nbclient import NotebookClient
from src.io import save_json


def execute_notebooks(names=None, config=None, timeout=600):
    if config:
        os.environ["HITO1_CONFIG"] = str(Path(config).resolve())
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if names:
        notebooks = [p for p in notebooks if p.name[:2] in names]
        if len(notebooks) != len(set(names)):
            raise ValueError("Selecciona números existentes, por ejemplo --only 01 09.")
    records = []
    for path in notebooks:
        print(f"Ejecutando {path.name}", flush=True)
        notebook = nbformat.read(path, as_version=4)
        # Un kernel nuevo por notebook; ninguna variable de otro notebook se hereda.
        client = NotebookClient(notebook, timeout=timeout, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT / "notebooks")}})
        manager = client.create_kernel_manager()
        # Cambio en memoria: no instala kernels ni modifica el entorno histórico.
        manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
        client.km = manager
        start = perf_counter()
        try:
            client.execute()
        except Exception:
            nbformat.write(notebook, path)
            records.append(dict(notebook=path.name, status="failed", seconds=perf_counter() - start))
            save_json(records, ROOT / "outputs/tables/notebooks_execution.json")
            raise
        nbformat.write(notebook, path)
        records.append(dict(notebook=path.name, status="passed", seconds=perf_counter() - start,
                            code_cells=sum(c.cell_type == "code" for c in notebook.cells)))
        save_json(records, ROOT / "outputs/tables/notebooks_execution.json")
        print(f"Completado en {records[-1]['seconds']:.1f} s", flush=True)
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="JSON alternativo; rutas relativas a ese JSON.")
    parser.add_argument("--only", nargs="+", help="Números de notebooks, por ejemplo 07 08.")
    parser.add_argument("--timeout", type=int, default=600, help="Tiempo máximo por celda, en segundos.")
    args = parser.parse_args()
    execute_notebooks(args.only, args.config, args.timeout)

