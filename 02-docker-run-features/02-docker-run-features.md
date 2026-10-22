# Lab 02: Docker Run Features

## Project Overview

This lab documents core Docker container-running features relevant to Data Engineering workflows: detached mode, port mapping, resource constraints, inspection, logs, and container lifecycle management.

> **Execution status:** Commands in this README are documented for practice. They have not been executed or verified on a Docker installation.

## Scenario

Run an Nginx web server and a long-running Python container to practice Docker configuration and troubleshooting.

## Task 1 — Run a Container in the Background

**Objective:** Run Nginx in detached mode with a clear container name.

```bash
docker run -d --name de-monitor nginx
```

**What it does**
- `docker run`: creates and starts a container.
- `-d`: runs it in the background (detached mode).
- `--name de-monitor`: assigns the container name.
- `nginx`: specifies the image.

**Verification command**

```bash
docker ps
```

## Task 2 — Port Mapping

**Objective:** Make Nginx available at `http://localhost:8088` by mapping host port `8088` to container port `80`.

```bash
docker run -d --name de-monitor-web -p 8088:80 nginx
```

**Port mapping format:** `HOST_PORT:CONTAINER_PORT`

- `8088`: port on the host machine.
- `80`: port inside the container, where Nginx listens.

**Verification**
1. Check the container is running:

   ```bash
   docker ps
   ```

2. Open `http://localhost:8088` in a browser.

> If port `8088` is already in use, choose another available host port and update the URL accordingly.

## Task 3 — Resource Constraints

**Objective:** Run a Python container with a memory limit of 512 MB and a CPU limit of 1 CPU.

```bash
docker run -d --name etl-limited --memory=512m --cpus=1 python:3.12-slim sleep infinity
```

**What the options mean**
- `--memory=512m`: sets the container memory limit to 512 MB (Docker's `m` suffix means megabytes).
- `--cpus=1`: limits the container to a CPU capacity equivalent to one CPU.
- `python:3.12-slim`: the Python image.
- `sleep infinity`: keeps the container running for inspection; it is a placeholder, not an ETL job.

**Verification**

```bash
docker ps
docker inspect etl-limited
```

`docker inspect` returns detailed JSON configuration. Look for the configured memory and CPU limits in the container's host configuration.

## Task 4 — Inspect Configuration and Logs

**Objective:** Inspect a container and review its logs.

```bash
docker inspect etl-limited
docker logs etl-limited
```

- `docker inspect`: shows detailed container configuration and state.
- `docker logs`: shows output written to the container's standard output and standard error.

> The `sleep infinity` process may produce no meaningful logs. An empty log output is not necessarily an error.

## Task 5 — Stop and Restart a Container

**Objective:** Stop and restart the same existing container.

```bash
docker stop etl-limited
docker ps -a
docker start etl-limited
docker ps
```

- `docker stop`: stops the running container.
- `docker ps -a`: lists running and stopped containers.
- `docker start`: starts the existing stopped container; it does not create a new container.
- `docker ps`: lists currently running containers.

## Key Learnings

- Detached mode with `-d`
- Container naming with `--name`
- Port mapping with `-p HOST_PORT:CONTAINER_PORT`
- Memory and CPU limits with `--memory` and `--cpus`
- Configuration inspection with `docker inspect`
- Logs with `docker logs`
- Container lifecycle management with `docker stop`, `docker start`, and `docker ps -a`

## Notes

- These commands are documentation examples and have not been run or verified in this environment.
- The two Nginx examples use different container names so they can coexist, but they are separate containers. If you run both, stop or remove any existing container with the same name first.
- To fully validate this lab, install Docker Desktop (Windows/macOS) or Docker Engine (Linux), then run the commands and record the actual results here.
