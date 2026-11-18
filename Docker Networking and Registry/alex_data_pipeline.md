# 🚂 Unit 7: Docker Networking and Registry - Practical Lab (Alex Data Pipeline)

Welcome to the **Alex Data Pipeline** repository! This file documents the hands-on implementation of Docker concepts regarding **Docker Networking** and **Docker Registry**, tailored specifically for modern **Data Engineering** workflows.

---

## 🏗️ Architecture Overview

In this practical application for **Unit 7**, we simulated a production-grade data pipeline environment for "Alex Data", featuring:

1. **PostgreSQL Database**: For storing shipment data and processing analytics.
2. **Custom Bridge Network (`data_ops_net`)**: To isolate project services and ensure secure service-to-service communication using Docker's internal DNS.
3. **Local Private Registry (on Port 5000)**: To securely store and manage proprietary ETL pipeline images before production deployment.

---

## 🛠️ Step-by-Step Implementation Workflow

Follow these steps in order to set up and manage your project's networks and registries locally:

### Step 1: Create a Custom Bridge Network
To isolate data pipeline services from default networks and ensure secure internal communication:
```bash
docker network create --driver bridge data_ops_net
```
* **To verify the network creation:**
  ```bash
  docker network ls
  ```

### Step 2: Deploy the Database Service
Run a PostgreSQL container attached directly to the custom network with the required environment variables:
```bash
docker run -d \
  --network data_ops_net \
  --name db_server \
  -e POSTGRES_PASSWORD=secret_pass \
  postgres:latest
```

### Step 3: Deploy a Local Private Registry
Simulate an on-premise company registry to push your custom ETL pipeline images safely:
```bash
docker run -d \
  -p 5000:5000 \
  --name local_registry \
  registry:2
```

### Step 4: Build, Tag, and Push the Data Pipeline Image

1. **Build the image locally:**
   ```bash
   docker build -t my-etl-pipeline:v1 .
   ```

2. **Tag the image with the local registry endpoint:**
   Tells Docker where the private registry is located:
   ```bash
   docker image tag my-etl-pipeline:v1 localhost:5000/my-etl-pipeline:v1
   ```

3. **Push the image to the local registry:**
   ```bash
   docker push localhost:5000/my-etl-pipeline:v1
   ```

---

## 📋 Comprehensive Docker Commands Reference

| Command | Category | Description |
| :--- | :--- | :--- |
| `docker network create --driver bridge <name>` | Networking | Creates a new isolated custom bridge network. |
| `docker network ls` | Networking | Lists all available Docker networks on the host. |
| `docker inspect <container_name>` | Troubleshooting | Inspects container configuration details (IP, networks, etc.). |
| `docker login` | Registry | Authenticates with public or private Docker registries. |
| `docker image tag <src> <target>` | Image Management | Tags an image to match a specific registry repository URL. |
| `docker push <registry_url>/<image>:<tag>` | Registry | Uploads a local container image to a registry. |
| `docker pull <registry_url>/<image>:<tag>` | Registry | Downloads a container image from a registry to your host. |

---

## 🔒 Summary of Docker Network Types

* **Bridge**: The default isolated virtual network. Requires port mapping (`-p`) for external access, or custom bridge networks for secure container-to-container communication using names.
* **Host**: Removes isolation completely; the container shares the host machine's network stack and port space directly.
* **None**: Total isolation; the container gets no network interface or internet access, ideal for sensitive local batch processing.

---

## 🚀 Author

**Ahmed Ibrahim**  
*Computer Science Undergraduate @ Alexandria University | Microsoft Data Engineer Trainee (DEPI)*  
GitHub: [ahmed-ibrahim-EG](https://github.com/ahmed-ibrahim-EG)

*Crafted with passion for Data Engineering mastery.*
