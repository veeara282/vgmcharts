# Data pipelines

Our data pipelines are written in Python, and we use [`uv`](https://docs.astral.sh/uv/) as our Python build tool.

It is recommended that all Python programs and `uv` commands be run from the `pipelines/` directory.

To set up a virtual environment in `uv`, run the following commands from this directory:

```sh
uv venv
uv pip install -r pyproject.toml
```

(Note: `uv pip install --project .` does not work.)

Pipelines should be run as modules via `uv`:

```sh
uv run python -m pokemon.get_ost_albums_basic_info
```

To run them from within the Docker container, pass command-line arguments to
`docker compose run`&mdash;these will be passed to `python`.
(Make sure to build the container first.) For example:

```sh
# Docker (standalone)
docker run -it vgmcharts-pipelines -m init.0_setup_data_lake --verbose

# Docker Compose
docker compose run pipelines -m init.0_setup_data_lake --verbose
```

Do not run directly in `docker run`, as it depends on the environment variables defined
in `docker-compose.yml`, particularly `S3_BUCKET`.
