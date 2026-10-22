<div align="center">

# 🐳 Docker for Data Engineering & Cloud Infrastructure

<p align="center">
  <strong>A production-ready, hands-on lab series mastering containerization, runtime mechanics, and multi-service orchestration.</strong>
</p>

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://www.kernel.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Status](https://img.shields.io/badge/Status-Active%20Learning-brightgreen?style=for-the-badge)](#-hands-on-curriculum--lab-tracker)

<br/>

[Overview](#-overview) •
[Directory Architecture](#-directory-architecture) •
[Lab Curriculum](#-hands-on-curriculum--lab-tracker) •
[CLI Quick Reference](#-cli-quick-reference) •
[Lab Standard Workflow](#-lab-execution-standard)

---

</div>

## 📌 Overview

This repository documents an end-to-end hands-on journey through the **Docker for Beginners** curriculum, specifically calibrated for **Data Engineering** pipelines, distributed storage, and containerized backend services.

Each module in the curriculum contains a dedicated practical lab directory featuring terminal workflows, real diagnostic tests, command breakdowns, and clean teardown scripts.

---

## 🗂️ Directory Architecture

```bash
docker-for-data-engineering/
├── 📄 README.md                           # Master Syllabus & Progress Tracker (Root)
│
├── 📁 01-basic-docker-commands/            # Lab 01: Container Lifecycle & CLI Mechanics
├── 📁 02-docker-run-features/              # Lab 02: Ports, Background Daemons & Resource Constraints
├── 📁 03-docker-images/                     # Lab 03: Dockerfile Layering, Caching & Tagging
├── 📁 04-environment-variables/             # Lab 04: Dynamic Runtime Config & Secrets
├── 📁 05-commands-vs-entrypoint/            # Lab 05: Startup Mechanics: Static vs Dynamic Arguments
├── 📁 06-docker-compose/                    # Lab 06: Multi-Container Orchestration (Voting App)
├── 📁 07-docker-storage/                    # Lab 07: Volumes, Bind Mounts & Persistence
├── 📁 08-docker-networking/                 # Lab 08: Bridge Networks & Internal DNS Discovery
├── 📁 09-docker-registry/                   # Lab 09: Image Tagging, Registries & Docker Hub
├── 📁 10-container-orchestration/           # Lab 10: Docker Swarm & Kubernetes Fundamentals
└── 📁 11-yaml-configuration/                # Lab 11: YAML Specifications for Infrastructure as Code
```

---

## 🗺️ Hands-on Curriculum & Lab Tracker

<div align="center">

| # | Module / Topic | Core Hands-on Focus | Status | Lab Directory |
| :-: | :--- | :--- | :-: | :-: |
| **01** | **Basic Docker Commands** | Lifecycle management (`run`, `ps`, `exec`, `stop`, `rm`, `rmi`), process isolation & exit code verification (`0` vs `137`). | ![Completed](https://img.shields.io/badge/Status-Completed-success?style=flat-square) | [📂 Open Lab 01](./01-container-lifecycle/README.md) |
| **02** | **Advanced Docker Run** | Terminal allocation (`-it`), port mapping (`-p host:container`), resource quotas (CPU/RAM), and background daemons (`-d`). | ![In Progress](https://img.shields.io/badge/Status-In%20Progress-blue?style=flat-square) | [📂 Open Lab 02](./02-docker-run-features/02-docker-run-features.md) |
| **03** | **Docker Images** | Writing production `Dockerfile`s, caching layers, multi-stage builds, and minimizing attack surfaces. | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 03-docker-images/` |
| **04** | **Environment Variables** | Runtime credential injection, config decoupling, `--env-file`, and secret isolation. | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 04-environment-variables/` |
| **05** | **Commands vs Entrypoint** | Container entry mechanics: deterministic entry (`ENTRYPOINT`) vs flexible default arguments (`CMD`). | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 05-commands-vs-entrypoint/` |
| **06** | **Docker Compose** | Multi-service orchestration via declarative YAML (Web, Redis Cache, Postgres DB, and Worker services). | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 06-docker-compose/` |
| **07** | **Docker Storage & Engine** | Stateful pipelines: Data persistence, Docker Volumes (`-v`), Bind Mounts, and Copy-on-Write (CoW). | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 07-docker-storage/` |
| **08** | **Docker Networking** | Container connectivity, bridge networks, custom subnets, embedded DNS resolution, and host mode. | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 08-docker-networking/` |
| **09** | **Docker Registry** | Image semantic versioning, pushing to public Docker Hub, and spinning up a local private registry. | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 09-docker-registry/` |
| **10** | **Container Orchestration** | High availability, self-healing services, clustering basics, Docker Swarm services, and Kubernetes architecture. | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 10-container-orchestration/` |
| **11** | **YAML for DevOps** | Syntax rules for Declarative Infrastructure: scalars, mappings, lists, and multi-doc streams. | ![Planned](https://img.shields.io/badge/Status-Planned-lightgrey?style=flat-square) | `📁 11-yaml-configuration/` |

</div>

---

## ⚡ CLI Quick Reference

```bash
# ---------------------------------------------
# 📦 Container Lifecycle Operations
# ---------------------------------------------
docker run -d --name <name> <image>      # Create and run in background (detached)
docker ps                                # List active running containers
docker ps -a                             # List all containers (including exited)
docker exec -it <name> <command>         # Execute command inside a live container
docker stop <name>                       # Gracefully terminate container process
docker rm <name>                         # Permanently delete stopped container

# ---------------------------------------------
# 🖼️ Image Management Operations
# ---------------------------------------------
docker images                            # View locally cached images
docker pull <image>:<tag>                # Pull specific image from registry
docker rmi <image>                       # Remove local image (must delete containers first)
docker build -t <tag> .                  # Build custom image using local Dockerfile
```

---

## 🔬 Lab Execution Standard

Every lab within this repository adheres to a strict four-step engineering standard:

```text
[ 1. Concept Anatomy ]  ──▶  [ 2. Terminal Run ]  ──▶  [ 3. Inspection & Telemetry ]  ──▶  [ 4. Teardown ]
```

1. **Concept Anatomy:** Theoretical foundation and Data Engineering rationale.
2. **Terminal Run:** Exact CLI commands executed with optimal parameters.
3. **Inspection & Telemetry:** Verification of runtime behavior, exit codes, logs, and network status.
4. **Teardown:** Clean decommissioning of containers, volumes, and images to prevent resource leaks.

---

<div align="center">
  <sub>Built with precision for Data Engineering and Cloud Infrastructure workflows.</sub>
</div>
