# vgmcharts
Explore trending video game music

## First things first: create a .env file

Find the terminal command appropriate for your operating system below and copy the
example `.env-example` into a local `.env` you can then edit with the credentials we
provide. Contact us for the deets!

Unix / macOS (bash / zsh):

```sh
cp .env-example .env
# edit .env with your editor by typing `code .env`, `vim .env`, etc.
```

PowerShell (Windows):
```powershell
Copy-Item .env-example .env
# then edit .env with Notepad or your preferred editor
```

The gitignore in this project is already set up to never commit your `.env` file; please
keep secrets out of version control (aka git).

## Running the app

Some useful commands for building, running, and shutting down the Docker environment:

```sh
# Build all containers
docker compose build

# Rebuild and run all services
docker compose up --build

# Shut down all services
docker compose down

# Shut down all services and remove named volumes (object store and database)
docker compose down -v
```

For more useful Docker commands, visit [docker.how](https://docker.how/).

Note that containers should *always* be run in Docker because they depend on the
environment variables in `.env`.
