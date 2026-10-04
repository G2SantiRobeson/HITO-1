"""Ejecuta las celdas en procesos Python independientes, sin servidor Jupyter.

Usa las mismas celdas y funciones científicas que reproduce.py. Es útil en
entornos donde no se permite abrir los sockets de un kernel Jupyter.
"""
import argparse
import os
from pathlib import Path
import subprocess
import sys
from time import perf_counter

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def execute_one(path):
    import nbformat
    from IPython.core.interactiveshell import InteractiveShell
    from IPython.utils.capture import capture_output
    from matplotlib_inline.backend_inline import configure_inline_support

    path = path.resolve()
    if path.parent != ROOT / "notebooks":
        raise ValueError("El notebook debe estar en la carpeta notebooks.")
    os.chdir(path.parent)
    shell = InteractiveShell.instance()
    configure_inline_support(shell, "inline")
    notebook = nbformat.read(path, as_version=4)
    count = 0
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue
        count += 1
        with capture_output() as captured:
            result = shell.run_cell(cell.source, store_history=False)
        cell.execution_count = count
        outputs = []
        for name in ("stdout", "stderr"):
            value = getattr(captured, name)
            if value:
                outputs.append(nbformat.v4.new_output("stream", name=name, text=value))
        outputs.extend(nbformat.v4.new_output("display_data", data=o.data, metadata=o.metadata)
                       for o in captured.outputs)
        cell.outputs = outputs
        error = result.error_before_exec or result.error_in_exec
        if error:
            cell.outputs.append(nbformat.v4.new_output("error", ename=type(error).__name__,
                                                      evalue=str(error), traceback=[str(error)]))
            nbformat.write(notebook, path)
            raise error
    nbformat.validate(notebook)
    nbformat.write(notebook, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--only", nargs="+")
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    for name, folder in (("MPLCONFIGDIR", ".matplotlib"), ("IPYTHONDIR", ".ipython")):
        os.environ[name] = str(ROOT / "outputs" / folder)
    os.environ["MPLBACKEND"] = "module://matplotlib_inline.backend_inline"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    if args.config:
        os.environ["HITO1_CONFIG"] = str(args.config.resolve())
    if args.worker:
        execute_one(args.worker)
        return
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if args.only:
        notebooks = [p for p in notebooks if p.name[:2] in args.only]
        if len(notebooks) != len(set(args.only)):
            parser.error("Selecciona números existentes, por ejemplo --only 07 08 09.")
    from src.io import save_json
    records = []
    for path in notebooks:
        print(f"Ejecutando {path.name}", flush=True)
        start = perf_counter()
        process = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()),
                                  "--worker", str(path)], cwd=ROOT)
        records.append(dict(notebook=path.name, status="passed" if process.returncode == 0 else "failed",
                            seconds=perf_counter() - start, execution="independent Python process"))
        save_json(records, ROOT / "outputs/tables/notebooks_execution.json")
        if process.returncode:
            raise SystemExit(process.returncode)
        print(f"Completado en {records[-1]['seconds']:.1f} s", flush=True)


if __name__ == "__main__":
    main()
