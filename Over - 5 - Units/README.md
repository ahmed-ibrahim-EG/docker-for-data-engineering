<div align="center">

# ⚡ DataFlow: Containerized Ingestion & Telemetry Stack

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask_3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

<p align="center">
  <b>A production-grade, local Data Engineering micro-pipeline environment featuring automated container coordination, resilient health-checks, synthetic telemetry streaming, and a real-time web monitor.</b>
</p>

---

[Key Highlights](#-key-highlights) •
[System Architecture](#-system-architecture) •
[Network & Storage](#-network--storage-topology) •
[Project Structure](#-project-structure) •
[Runbook](#-command-runbook) •
[Engineering Principles](#-core-engineering-patterns)

---

</div>

## 🌟 Key Highlights

- **Zero-Crash Orchestration:** Uses `service_healthy` conditional startup to eliminate database race conditions and connection drops (`ConnectionRefusedError`).
- **Optimized Layer Caching:** Dockerfile engineered to invalidate dependencies independently from source code changes.
- **Dynamic CMD Overrides:** Configured using an immutable `ENTRYPOINT` with flexible runtime arguments for ad-hoc execution.
- **Automatic Internal Discovery:** Multi-container private bridge networking with integrated DNS resolving (`db:5432`).
- **Stateful Persistence:** Named Docker volume integration ensures data longevity across container lifecycles.

---

## 🏛️ System Architecture

```text
       +-----------------------------------------------------------------------------+
       |                         USER HOST MACHINE (Localhost)                       |
       +-----------------------------------------------------------------------------+
               | (Port 5000)                                           | (Port 5432)
               v                                                       v
       +-----------------------------------------------------------------------------+
       |                      ISOLATED DOCKER BRIDGE NETWORK                         |
       |                                                                             |
       |  +------------------------------+       Internal DNS       +-------------+  |
       |  |  analytics_web_container     |       "host: db"         | analytics_  |  |
       |  |  (Flask + Ingestion App)     | -----------------------> | db_container|  |
       |  |                              |       Port: 5432         | (PostgreSQL)|  |
       |  +------------------------------+                          +-------------+  |
       |                 ^                                                 |         |
       |                 | (Wait for Healthcheck Pass)                     v         |
       |                 +======================================== [ Volume: pgdata ]|
       +-----------------------------------------------------------------------------+
```

---

## 📊 Network & Storage Topology

### Services & Port Mappings

| Service Name | Container Name | Image Source | Host Port | Internal Port | Status Indicator |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **`db`** | `analytics_db_container` | `postgres:15-alpine` | `5432` | `5432` | `pg_isready` (Healthy) |
| **`web`** | `analytics_web_container` | Local Build (`Dockerfile`) | `5000` | `5000` | HTTP 200 OK |

### Environment Variables

| Variable | Default Value | Target Service | Purpose |
| :--- | :--- | :---: | :--- |
| `POSTGRES_USER` | `analytics_user` | `db` | Database superuser account |
| `POSTGRES_PASSWORD` | `change_me_please` | `db` | Database user authentication |
| `POSTGRES_DB` | `analytics_db` | `db` | Target warehouse database |
| `DB_HOST` | `db` | `web` | Internal Docker DNS address for Postgres |
| `DB_PORT` | `5432` | `web` | Database listening port |

---

## 📁 Project Structure

```text
docker-data-pipeline/
├── 📄 app.py                 # Telemetry generator, Postgres connection pool & UI
├── 📄 requirements.txt       # Frozen application dependencies
├── 🐳 Dockerfile             # Multi-layer Docker recipe
├── 🐙 docker-compose.yml     # Multi-container declaration & health constraints
└── 📘 README.md              # Documentation and execution manual
```

---

## 📜 Configuration Code

<details>
<summary><b>🔍 View Dockerfile</b></summary>

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Cache dependencies layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .

# Base binary definition with default argument
ENTRYPOINT ["python"]
CMD ["app.py"]
```
</details>

<details>
<summary><b>🔍 View docker-compose.yml</b></summary>

```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: analytics_db_container
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER:-analytics_user}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-change_me_please}
      POSTGRES_DB: analytics_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s

  web:
    build: .
    container_name: analytics_web_container
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: analytics_db
      DB_USER: ${DB_USER:-analytics_user}
      DB_PASSWORD: ${DB_PASSWORD:-change_me_please}
    ports:
      - "5000:5000"

volumes:
  pgdata:
```
</details>

---

## 🚀 Command Runbook

### 1. Build and Boot Stack
Launch the environment in detached mode while enforcing a clean image rebuild:
```bash
docker compose up -d --build
```

### 2. Verify Health Status
Inspect service runtimes and confirm the `(healthy)` indicator on the database:
```bash
docker compose ps
```

### 3. Generate & Ingest Telemetry
* Access the interactive dashboard: **[http://localhost:5000](http://localhost:5000)**
* Click **`+ Generate 50 New Rows (Ingest ETL)`** to trigger data generation.

### 4. Query Data Directly via CLI
Inspect the internal database state using `docker exec` without needing an external SQL client:
```bash
docker exec -it analytics_db_container psql -U analytics_user -d analytics_db -c "SELECT COUNT(*) FROM sensor_telemetry;"
```

### 5. Execute Ad-hoc Python Tasks (Overriding `CMD`)
Run a transient task using the image's pre-configured `ENTRYPOINT`:
```bash
docker compose run --rm web -c "print('Custom ETL task executed inside the container!')"
```

### 6. Inspect Live Logs
Follow application standard output streams:
```bash
docker compose logs -f web
```

### 7. Teardown & Clean Up
Stop containers and safely tear down the dedicated bridge network:
```bash
# Keep database volume data safe:
docker compose down

# Optional: Wipe persistent database volume completely:
docker compose down -v
```

---

## 🧠 Core Engineering Patterns

### 1. Robust Healthcheck Sequencing
Standard `depends_on` only checks if the dependency container has started, which causes premature connections to fail while Postgres finishes initializing. Combining `healthcheck` with `condition: service_healthy` ensures zero race conditions.

### 2. Layer Caching Hierarchy
Dependency definitions (`requirements.txt`) are copied and installed prior to transferring application code (`app.py`). Any routine logic change in `app.py` builds in fractions of a second because image layers are retrieved directly from Docker's build cache.

### 3. The `ENTRYPOINT` vs `CMD` Contract
The container is configured as a purpose-built Python executable. The entrypoint `["python"]` guarantees execution consistency, while `CMD ["app.py"]` serves as the swappable parameter for flexible ETL task execution.

---

<div align="center">
  <b>Built for resilient local data development.</b>
</div>
