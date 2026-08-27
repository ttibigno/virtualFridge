# virtualFridge

## Second Project for the course "Fondamenti di Amministrazione del Sistema" at UniTrento

## Overview

The project consists of the creation of a virtual shared fridge, where each user can keep track of the items they store in a real-world fridge and remotely check their expiration dates and the fridge's contents.

The project also includes a mocked receipt scanner that estimates the category and expiration date of each item.

The entire stack is deployed using Docker on a single node, with the services connected through a Docker Compose network.

## Requirements

- Docker Engine and Docker Compose (or Docker Desktop on Windows and macOS)
- Make (optional)
- Bash (optional)

## Installation

Once all the requirements are met, you can install the entire stack with:
```shell 
make install
```
After installation, the frontend is available at `localhost:8000`, while Grafana is available at `localhost:3000`.

If Make is not installed on the system, you can use:
```shell
bash ./scripts/setup.sh
```
which runs:
```shel
docker compose up --build -d
```

If Bash is not installed either, you will have to manually create an `.env` file containing all the required values. Alternatively, you can copy `.env.example` and rename it to `.env`.

## Running and Stopping the Stack

You can stop and start the stack again with:
```shell
make stop
make run
```
Alternatively, you can use:
```shell
docker compose down
docker compose up -d
```
These commands do not remove the existing Docker volumes, so no persistent data will be lost.

## Uninstalling and Cleanup

You can remove all containers, images, and volumes associated with the project using:
```shell 
make uninstall
```

Alternatively: `docker compose down --remove-orphans --rmi all -v`
You can also completely clean up the Docker environment with:
```shell
make cleanup
```
which is equivalent to: `docker system prune -af`
**Warning:** `docker system prune -af` removes unused Docker resources from the entire Docker environment, not only those belonging to this project.

## Mocking the Scanner and Stress Testing

The mocked scanner can be used with:
```shell
make populate
```

By default, this generates 50 "scanned" items. A custom number can be specified using `N=`:
```shell
make populate N=100
```
The backend can also be stress-tested using:
```shell
make stress
```

The number of requests and the error rate can be customized using `N=` and `ERROR=`. By default, 50 requests are sent with an error rate of 0%:
```shell
make stress N=100 ERROR=10
```

## Architecture

The main services are:
- `backend`: hosts the FastAPI server and serves the frontend on port `:8000`. It handles requests from users and the mocked scanner.
- `postgres`: the PostgreSQL database directly connected to the backend.
- `prometheus`: collects and stores metrics exposed by the backend.
- `promtail`: collects container logs and ships them to Loki.
- `loki`: aggregates and stores logs collected by Promtail.
- `grafana`: provides dashboards for accessing data from Prometheus and Loki. It is exposed on port `:3000`.

All services run on the same Docker host. However, only the `backend` and `grafana` services are accessible from outside Docker. The remaining services are accessible only through the Docker Compose network.
Some security measures have therefore been implemented, including authentication for Grafana and a custom non-root user for the backend container.
When the stack is started with `make install`, the `backend` image is built using a custom Dockerfile, while all other services use publicly available Docker images.
The `backend` depends on the `postgres` service being healthy through the `service_healthy` condition, so it cannot start without a working database.
Similarly, the `scripts` service requires the `backend` to be running, while `grafana` depends on both `loki` and `prometheus`.

## CI and Route Testing

The project includes a CI pipeline based on GitHub Actions and FastAPI's `TestClient`.
On every pull request and push, a GitHub Actions job runs the test suite using the custom `tests` Dockerfile and:
```shell
make test
```
The CI pipeline then verifies that the backend can be successfully built using the current custom Dockerfile.

## Project Structure

```bash
virtualFridge/
├── .github/
│   └── workflows/
│       └── tests.yaml          # GitHub Actions workflow
├── backend/
│   ├── api.yaml               # API specification
│   ├── database.py            # Database setup and sessions
│   ├── frontend/              # Basic frontend
│   ├── helpers/               # Helpers for backend queries
│   ├── middleware/            # Logging and metrics middleware
│   ├── pyproject.toml         # Python/uv requirements
│   ├── routers/               # Backend routers
│   ├── schemas/               # Pydantic schemas
│   ├── server.py              # Backend entrypoint
│   ├── Dockerfile             # Backend Dockerfile
│   ├── tables/                # SQLAlchemy tables and database population
│   └── tests/                 # Test suite and test Dockerfile
├── observability/
│   ├── grafana/               # Grafana dashboards and provisioning
│   ├── loki/                  # Loki configuration
│   ├── prometheus/            # Prometheus configuration
│   └── promtail/              # Promtail configuration
├── scripts/                   # Setup, scanner mocking, and stress tests
├── .env.example               # Example environment variables
├── .gitignore
├── compose.test.yaml          # Docker Compose configuration for tests
├── compose.yaml               # Docker Compose configuration
├── LICENSE
└── Makefile
```