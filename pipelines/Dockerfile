# Idea: Python 3.13 + uv setup, install dependencies and run thru uv

# This file is a derivative work of https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
# Portions copyright (c) 2025 Astral Software Inc.
# See https://github.com/astral-sh/uv-docker-example/blob/main/LICENSE-MIT
# and https://github.com/astral-sh/uv-docker-example/blob/main/LICENSE-APACHE for license info.

# Astral.sh provides official Docker images with uv built-in.
# This image comes with Python 3.13.
# More images available at https://github.com/astral-sh/uv/pkgs/container/uv/versions?filters%5Bversion_type%5D=tagged
FROM ghcr.io/astral-sh/uv:0.10.4-python3.13-trixie-slim

# Set up non-root user to run Python pipelines
RUN groupadd --system --gid 999 pipelines \
 && useradd --system --gid 999 --uid 999 --create-home pipelines

# Install the project into `/app`
WORKDIR /app

# Precompile `.pyc` files during installation, so container starts up faster
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Keep explicit entrypoint so `docker run image <args>` just works
ENTRYPOINT ["uv", "run"]

# Use the non-root user to run our application
USER pipelines

# Default job (currently the only pipeline)
# Pipeline filenames are relative to the `pipelines/` directory
# TODO: add support for other pipelines when added (preferably via `python -m <module>`)
CMD ["pokemon/get_ost_albums_basic_info.py"]
