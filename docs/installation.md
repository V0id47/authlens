# Installation and packaging

The README contains Linux/macOS and Windows setup commands. Python 3.11+ is required for standard-library TOML and UTC support. A virtual environment is recommended; no administrator rights or runtime services are needed. Source install: `python -m pip install .`. Editable development install: `python -m pip install -e .`.

Build distributions with `python -m build`. This produces a wheel and source archive under `dist/`. Install the wheel in a separate environment to verify package data and entrypoints. Do not run `pip install authlens` expecting this repository unless its distribution has actually been published and verified.

```sh
python -m venv .smoke-venv
# Linux/macOS
.smoke-venv/bin/python -m pip install --no-deps dist/authlens-0.1.0-py3-none-any.whl
.smoke-venv/bin/authlens analyze examples/events.jsonl --lang ru --format json
```

Windows: replace `.smoke-venv/bin/python` with `.smoke-venv\Scripts\python.exe` and `bin/authlens` with `Scripts\authlens.exe`. For fully offline installation, prepare the built wheel beforehand and use `--no-index --no-deps`. Runtime has no third-party dependencies; building from source can need downloaded build tooling.

No Docker/Homebrew/Winget packaging is added because it would not improve this single-file offline workflow. A universal Python wheel is sufficient. Build tools and Python are still part of the supply chain.
