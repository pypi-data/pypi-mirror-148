"""Automatically install dependencies into venv and run script.

In presence of a requirements.txt file, this module locates or creates
a virtual environment, installs the dependencies and passes all other
arguments to the python interpreter of the virtual environment.

Assumptions:
- There is requirements.txt at the root of the project.
- The virtual environment shall be called ".venv" and reside next to the
  requirements.txt.
- The script to execute is at the root or inside the project.
- We want to use the same Python interpreter that is used for executing
  peeve (this script) itself.
- The first command line argument is the path to the script to execute.

"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import platform
import runpy
import subprocess
import site
import sys
import venv
from contextlib import contextmanager
from pathlib import Path

__all__ = ["cli", "bootstrap"]  # noqa: F822 # pylint: disable=undefined-all-variable

log = logging.getLogger("peeve")


def cli():
    """Command line interface to launch scripts.

    For execution as script, module, or entry point:
        python peeve.py <script>
        python -m peeve <script>
        peeve <script>
        pv <script>

    Other modes of the Python interpreter, for example
    interactive usage, module invocation, or code execution (-c),
    are currently not supported.
    """
    with ensure_logging():
        # Remove peeve itself from argument list
        sys.argv = sys.argv[1:]

        script_path = get_script_path(sys.argv)
        if script_path is None:
            log.error("Please specify the path to a valid script.")
            sys.exit(1)

        ensure_venv(script_path.parent)

    run_script(script_path)


def __getattr__(name: str) -> Path | None:
    """Programmatic usage on import.

    Example::
        from peeve import bootstrap
    """
    if name == "bootstrap":
        # TODO: return early if already ensured venv in same process?
        with ensure_logging():
            script_path = get_script_path(sys.argv)
            if not script_path:
                log.error("Could not find location of script")
                sys.exit(1)
            return ensure_venv(script_path.parent)

    raise AttributeError(f"Module peeve has no attribute {name}")


@contextmanager
def ensure_logging(level: int = logging.INFO):
    """Ensure logging handler and restore configuration eventually."""
    root = logging.getLogger()
    num_orig_handlers = len(root.handlers)
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)-8s [%(name)s] %(message)s"
    )
    try:
        yield
    finally:
        for handler in root.handlers[num_orig_handlers:]:
            root.removeHandler(handler)


def ensure_venv(start_dir: Path | None = None) -> Path | None:
    """Ensure updated virtual environment is active."""
    start_dir = start_dir or Path.cwd()
    requirements_file = find_requirements_file(start_dir)
    if not requirements_file:
        log.info("No requirements file found, not using venv.")
        return None

    project_dir = requirements_file.parent
    venv_dir = project_dir / ".venv"
    hash_file = venv_dir / "peeve.json"

    if not venv_dir.exists():
        create_venv(venv_dir)

    checksum = hash_requirements(requirements_file)
    if is_update_required(hash_file, checksum):
        remove_hash(hash_file)
        update_venv(venv_dir, requirements_file)
        update_hash(hash_file, checksum)

    if not is_active(venv_dir):
        activate(venv_dir)

    return venv_dir


def run_script(path: Path) -> None:
    """Run script."""
    runpy.run_path(str(path))


def get_script_path(argv: list[str]) -> Path | None:
    """Get path to Python script from argument list."""
    if len(argv) < 1:
        log.error("Missing argument specifying Python script to run.")
        return None
    script_path = Path(argv[0])
    if not script_path.is_file() or not script_path.suffix == ".py":
        log.error(f"First argument '{script_path}' is not a valid file.")
        return None
    return script_path.resolve()


def create_venv(venv_dir: Path) -> None:
    """Create new virtual environment."""
    log.info(f"Creating virtual environment at {venv_dir}...")
    venv.create(venv_dir, clear=True, with_pip=True, prompt=venv_dir.parent.name)


def hash_requirements(requirements_file: Path) -> str:
    """Hash contents of requirements file."""
    return hashlib.md5(requirements_file.read_bytes()).hexdigest()


def is_update_required(hash_file: Path, checksum: str) -> bool:
    """Check if virtual environment needs an update."""
    if not hash_file.exists():
        return True
    data = json.loads(hash_file.read_text())
    return data.get("md5") != checksum


def remove_hash(hash_file: Path) -> None:
    """Remove hash file."""
    try:
        hash_file.unlink()
    except FileNotFoundError:
        pass


def update_hash(hash_file: Path, checksum: str) -> None:
    """Save current requirements hash in file."""
    data = {"format": "1.0", "md5": checksum}
    hash_file.write_text(json.dumps(data))


def update_venv(venv_dir: Path, requirements_file: Path) -> None:
    """Update virtual environment by upgrading packages.

    Upgrade Pip first to have latest features.
    """
    python = venv_dir / get_bin_dir_name() / "python"

    log.info("Updating pip...")
    pip_install(python, "pip")

    log.info(f"Installing dependencies from {requirements_file}...")
    pip_install(python, "-r", str(requirements_file))


def pip_install(python: Path, *args: str) -> None:
    """Install packages with Pip.

    Args:
        python: Path to Python interpreter.
        *args: Additional arguments to pip call, e.g. package names.
    """
    commands = [str(python), "-m", "pip", "install", "--upgrade", *args]
    process = subprocess.run(commands)
    if process.returncode != 0:
        log.error(f"Could not install {args}!")
        sys.exit(process.returncode)


def find_requirements_file(
    start_dir: Path,
    search_parents: bool = True,
) -> Path | None:
    """Locate requirements.txt.

    For now, only requirements.txt is supported.

    Returns:
        Path to requirements file, or None if not found.

    """
    for parent in (start_dir, *start_dir.parents):
        requirements_file = parent / "requirements.txt"
        if requirements_file.is_file():
            return requirements_file
        if not search_parents:
            break
    return None


def is_active(venv_dir: Path) -> bool:
    """Check if we are in the right virtual environment.

    Any environment not located in the project directory returns false.

    The virtual environment can be activated, or used by calling
    the interpreter directly.

    Works for venv and virtualenv (>= 20).
    """
    if sys.prefix == sys.base_prefix:
        log.debug("Not running in any venv.")
        return False
    if Path(sys.prefix) != venv_dir:
        log.debug(f"Running in incorrect venv {sys.prefix}.")
        return False
    return True


def activate(venv_dir: Path) -> None:
    """Activate virtual environment in process.

    See activate_this.py from virtualenv for reference.
    """
    bin_dir = venv_dir / get_bin_dir_name()
    lib_dir = venv_dir / get_lib_dir_name()

    # prepend bin to PATH (this file is inside the bin directory)
    os.environ["PATH"] = os.pathsep.join([str(bin_dir), os.environ.get("PATH", "")])
    os.environ["VIRTUAL_ENV"] = str(venv_dir)

    site.addsitedir(str(lib_dir))
    site.addsitedir(str(lib_dir / "site-packages"))

    sys.base_prefix = sys.prefix
    sys.prefix = str(venv_dir)


def get_bin_dir_name() -> str:
    """Get path to director with binaries."""
    return "Scripts" if platform.system() == "Windows" else "bin"


def get_lib_dir_name() -> str:
    """Get path to director with binaries."""
    major, minor, *_ = sys.version_info
    return "Lib" if platform.system() == "Windows" else f"lib/python{major}.{minor}"


if __name__ == "__main__":
    cli()
