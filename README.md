# vgmcharts
Explore trending video game music

## Data pipelines

Our data pipelines are written in Python, and we use [`uv`](https://docs.astral.sh/uv/) as our Python build tool.

It is recommended that all Python programs and `uv` commands be run from the repository root.

To set up a virtual environment in `uv`, run the following commands from the repository root:

```sh
uv venv
uv pip install -r pyproject.toml
```

(Note: `uv pip install --project .` does not work.)

Pipelines should be run via `uv`:

```sh
uv run ./pipelines/pokemon/get_ost_albums_basic_info.py
```
