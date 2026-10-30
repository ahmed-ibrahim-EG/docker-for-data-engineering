# 🚀 Containerized Data Ingestion & Monitoring Stack

A production-ready, lightweight Data Engineering pipeline environment containerized using **Docker** and orchestrated via **Docker Compose**. 

This project integrates a **PostgreSQL** analytical database with a unified **Flask** service responsible for telemetry ingestion, synthetic data generation, and a real-time web dashboard.

---

## 🏗️ Architecture & Component Overview

```
                   +------------------------------------------------+
                   |            Docker Network (Bridge)             |
                   |                                                |
                   |   +------------------+                         |
                   |   |                  |                         |
                   |   |   analytics_db   | <----+                  |
                   |   |  (PostgreSQL 15) |      |                  |
                   |   |                  |      |                  |
                   |   +------------------+      | (Port 5432)      |
                   |                             |                  |
                   |                             | (DNS: db)        |
                   |                             |                  |
                   |   +------------------+      |                  |
[ Host Browser ] ----> |  analytics_web   | -----+                  |
 (Port 5000)       |   |  (Flask + ETL)   |                         |
                   |   +------------------+                         |
                   +------------------------------------------------+
```

### Key Components:
1. **Database Service (`db`)**:
   * **Engine:** `postgres:15-alpine`
   * **Role:** Persistent analytical data store for telemetry streams.
   * **Readiness:** Configured with an integrated `healthcheck` testing PostgreSQL availability via `pg_isready`.
2. **Web & ETL Service (`web`)**:
   * **Engine:** Python 3.11 Slim with Flask & Psycopg2.
   * **Role:** Executes schema initialization, on-demand batch data insertion, and real-time metric visualization.
   * **Dependency Management:** Waits for the database to reach a healthy state before starting (`condition: service_healthy`).

---

## 📁 Repository Structure

```text
docker-data-pipeline/
│
├── app.py                 # Unified Flask application (ETL generator + Web UI)
├── requirements.txt       # Python dependencies (Flask, Psycopg2-binary)
├── Dockerfile             # Multi-layer Docker build recipe
├── docker-compose.yml     # Multi-container orchestration & networking manifest
└── README.md              # Project documentation & operational runbook
```

---

## ⚙️ Configuration Files Reference

### 1. `Dockerfile`
Built with standard layer caching best practices:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Cache dependencies layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py .

# Immutable execution entry with default argument
ENTRYPOINT ["python"]
CMD ["app.py"]
```

### 2. `docker-compose.yml`
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

---

## 🛠️ Step-by-Step Command Runbook

All terminal commands executed during the build, execution, and verification phases:

### 1. Build & Start Stack in Background
Build the application image and spin up the complete infrastructure in detached mode:
```bash
docker compose up -d --build
```

### 2. Verify Container Health & Status
Check whether the PostgreSQL service passed its health check and the Flask web service is running:
```bash
docker compose ps
```

### 3. Access Web UI & Trigger ETL Ingestion
* Open your browser and navigate to:
  ```text
  http://localhost:5000
  ```
* Click **`+ Generate 50 New Rows (Ingest ETL)`** to trigger data generation into the database.

### 4. Query Database Interactively via CLI (`docker exec`)
Validate actual data persistence directly inside the running PostgreSQL container:
```bash
docker exec -it analytics_db_container psql -U analytics_user -d analytics_db -c "SELECT count(*) FROM sensor_telemetry;"
```

### 5. Execute Ad-hoc Script / Override `CMD`
Run an arbitrary Python command inside a one-off container instance using the fixed `ENTRYPOINT`:
```bash
docker compose run --rm web -c "print('Ad-hoc ETL task completed successfully!')"
```

### 6. Monitor Logs (Optional)
Stream logs for the web service or the entire stack:
```bash
docker compose logs -f web
```

### 7. Graceful Teardown & Cleanup
Stop all running containers, remove networks, and free system resources:
```bash
# Standard teardown (preserves database volume data)
docker compose down

# Complete teardown (removes database volume data as well)
docker compose down -v
```

---

## 🧠 Concepts Demonstrated

* **Layer Caching:** Isolating `requirements.txt` installation before application code copying.
* **ENTRYPOINT vs. CMD:** Fixing the base runtime (`python`) while keeping the execution target (`app.py`) overrideable.
* **Service Discovery:** Allowing `analytics_web` to address PostgreSQL via its hostname alias `db`.
* **State Coordination:** Utilizing `healthcheck` and `condition: service_healthy` to prevent premature ETL connection failures.
* **Volume Persistence:** Preserving Postgres data files across container reboots via named volume `pgdata`.
