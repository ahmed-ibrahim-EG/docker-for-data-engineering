# Docker Fundamentals for Data Engineering

A comprehensive, hands-on repository covering core Docker fundamentals, container lifecycles, and essential CLI commands tailored for modern Data Engineering and backend workflows.

---

## 📌 Repository Overview

This repository documents practical labs, core architectural concepts, and terminal command workflows used to containerize applications, manage data services (like Redis and PostgreSQL), and troubleshoot container environments.

### Key Concepts Covered
* **Container vs. Virtual Machine:** Process isolation on a shared Linux Kernel vs. full hardware virtualization.
* **The "One Process per Container" Rule:** Architectural best practices separating database layers, caching layers, and pipeline jobs.
* **Image vs. Container:** Immutable blueprint templates vs. active runtime instances.
* **Command Syntax & Flags:** Mastery of `-d`, `--name`, `-p`, `-v`, `-e`, `--rm`, and `-it`.
* **Exit Codes:** Diagnosing `Exited (0)` vs. `Exited (137)`.

---

## 📂 Repository Structure

```text
docker-fundamentals/
├── README.md                          # Main repository reference guide (this file)
└── 01-container-lifecycle/
    └── README.md                      # Task 01: Container Lifecycle & Management Lab
```

---

## ⚡ Core CLI Cheat Sheet

### 1. Container Management
```bash
# Run a container in detached mode with a custom name
docker run -d --name <container_name> <image_name>

# List running containers
docker ps

# List all containers (running and stopped)
docker ps -a

# Stop an active container
docker stop <container_name_or_id>

# Remove a stopped container
docker rm <container_name_or_id>

# Execute a command inside a running container
docker exec <container_name_or_id> <command>
```

### 2. Image Management
```bash
# List local images
docker images

# Pull an image from Docker Hub without running it
docker pull <image_name>

# Remove a local image (dependent containers must be removed first)
docker rmi <image_name_or_id>
```

---

## 🛠️ Data Engineering Lab Recipes

### Run PostgreSQL with Persistent Storage & Custom Credentials
```bash
docker run -d \
  --name de_postgres \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=analytics \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15
```

### Run an Ephemeral Python Pipeline (Auto-Cleaned)
```bash
docker run --rm \
  -v $(pwd):/app \
  -w /app \
  python:3.10-slim \
  python pipeline.py
```