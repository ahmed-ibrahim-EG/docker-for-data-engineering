# 📊 Containerized Data Pipeline Telemetry Service

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Microsoft SQL Server](https://img.shields.io/badge/SQL%20Server-2022-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11--slim-3776AB?style=for-the-badge&logo=python&logoColor=white)

A containerized microservice built for Data Engineering workflows. It exposes pipeline health status, ingestion metrics, and run statistics backed by **Microsoft SQL Server 2022** and orchestrated via **Docker Compose**.

---

## 🏗️ Architecture Overview

The application runs as a multi-container architecture inside an isolated bridge network managed by Docker Compose:

```
                  ┌────────────────────────────────────────┐
                  │          Docker Host Machine           │
                  │                                        │
                  │   [Browser / Client] ──:5000           │
                  │          │                             │
                  │          ▼                             │
┌─────────────────┼──────────────────────────────┐         │
│ Docker Network  │   ┌──────────────────────┐   │         │
│                 │   │     metrics_api      │   │         │
│                 │   │  (Flask Application) │   │         │
│                 │   └──────────┬───────────┘   │         │
│                 │              │ (DNS: sqlserver:1433)   │
│                 │              ▼               │         │
│                 │   ┌──────────────────────┐   │         │
│                 │   │      sqlserver       │   │         │
│                 │   │ (MSSQL Server 2022)  │   │         │
│                 │   └──────────┬───────────┘   │         │
└─────────────────┼──────────────┼───────────────┘         │
                  │              ▼                         │
                  │     [Named Volume: mssql_data]         │
                  └────────────────────────────────────────┘
```

- **`metrics_api`**: Lightweight Flask microservice exposing telemetry endpoints.
- **`sqlserver`**: Microsoft SQL Server 2022 maintaining metadata and pipeline telemetry.
- **`mssql_data` (Volume)**: Named volume providing data persistence across container restarts.
- **Docker Compose Healthchecks**: Ensures Flask does not start querying until SQL Server is completely ready.

---

## 🚀 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Service overview, container ID, and timestamp. |
| `/health` | `GET` | Real-time database connectivity check (`SELECT 1`). |
| `/metrics` | `GET` | Fetches the latest pipeline telemetry records from SQL Server. |

---

## 🛠️ Getting Started

### 1. Prerequisites
- Docker Engine & Docker Compose installed.
- Git.

### 2. Configure Environment
Copy the example environment file or create your `.env`:
```bash
cp .env.example .env
```
Ensure your `.env` contains strong credentials (MSSQL requires complex passwords):
```env
DB_HOST=sqlserver
DB_PORT=1433
DB_NAME=master
DB_USER=sa
DB_PASSWORD=StrongPass@2026
```

### 3. Spin Up the Stack
Run Docker Compose in detached mode with an automatic image build:
```bash
docker compose up -d --build
```

### 4. Verify Services
Check running containers and health checks:
```bash
docker compose ps
```
Wait until `telemetry_mssql` marks `healthy` and `telemetry_flask` is running.

### 5. Access the API
- Test connectivity: `curl http://localhost:5000/health`
- Fetch telemetry: `curl http://localhost:5000/metrics`

---

## 📋 Docker CLI & Compose Workflow Practiced

| Command | Purpose |
| :--- | :--- |
| `docker compose up -d --build` | Builds images, setups network & volumes, and starts containers in detached mode. |
| `docker compose ps` | Displays service status, port mappings, and container health states. |
| `docker compose logs -f <service>` | Streams real-time logs for debugging (e.g., `docker compose logs -f metrics_api`). |
| `docker compose exec <service> sh` | Enters an active container shell for live inspection. |
| `docker compose down` | Stops and removes containers and internal networks (preserves volumes). |
| `docker compose down -v` | Stops containers and deletes all persistent named volumes. |