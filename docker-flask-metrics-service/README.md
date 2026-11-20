# Containerized Data Metrics Service (Flask & Docker)

A lightweight containerized microservice exposing batch pipeline health and processing metrics for Data Engineering workflows.

## Docker CLI Workflow Practiced
- `docker pull python:3.11-alpine`
- `docker images`
- `docker run -d --name metrics-app -p 5000:5000 metrics-service:v1.0`
- `docker ps` & `docker ps -a`
- `docker inspect metrics-app`
- `docker exec -it metrics-app sh`
- `docker attach metrics-app`
- `docker stop metrics-app`
- `docker start metrics-app`
- `docker rm metrics-app`
