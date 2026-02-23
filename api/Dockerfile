# Build
FROM golang:1.25 AS build

# Set the working directory 
WORKDIR /container

# Copy dependency files + download modules
COPY go.mod go.sum ./
RUN go mod download

COPY . .
# CGO_ENABLED=0 produces a fully static binary with no C runtime dependency, required to run on the minimal Alpine image below.
RUN CGO_ENABLED=0 GOOS=linux go build -o api .

# Runtime
FROM alpine:latest

WORKDIR /container

COPY --from=build /container/api .

EXPOSE ${API_PORT}

CMD ["./api"]
