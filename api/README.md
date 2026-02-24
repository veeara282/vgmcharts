# API

Go server using the [Echo](https://echo.labstack.com/) framework. Serves the backend API for the app.

## Prerequisites

- Go 1.22+

## Running

```sh
go run .
```

The server starts on port **1337**. Verify with:

```sh
curl http://localhost:1337/health
```

TODO: make healthcheck dependent on the API querying the db
