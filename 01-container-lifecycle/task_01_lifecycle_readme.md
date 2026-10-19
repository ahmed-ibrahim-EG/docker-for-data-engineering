# Task 01: Docker Container Lifecycle Management

A hands-on reference guide demonstrating the core lifecycle of a Docker container: launching in detached mode, verifying active processes, executing in-container commands, stopping, inspecting exit codes, and cleaning up resources.

---

## 🎯 Lab Objectives

1. Launch a container in the background (Detached Mode) using `-d` and set an explicit container name using `--name`.
2. Inspect active runtime states using `docker ps`.
3. Execute live diagnostics inside the container using `docker exec`.
4. Gracefully terminate container execution with `docker stop`.
5. Verify termination codes (`Exited (137)`) via `docker ps -a`.
6. Enforce proper cleanup order: remove the container first (`docker rm`), then delete the base image (`docker rmi`).

---

## 🚀 Execution Steps

### Step 1: Launch Container in Background
```bash
docker run -d --name c1 redis
```
* **Flags:**
  * `-d`: Detached mode (runs container in the background, freeing the terminal).
  * `--name c1`: Assigns an explicit name (`c1`) instead of an auto-generated identifier.
* **Image:** `redis` (pulled automatically from Docker Hub if not locally present).

---

### Step 2: Verify Active Runtime
```bash
docker ps
```
* **Expected Output:** Lists the active `c1` container with status `Up <duration>`.

---

### Step 3: Run Internal Diagnostics
```bash
docker exec c1 redis-cli ping
```
* **Explanation:** Executes the `redis-cli ping` utility inside the running container without opening an interactive shell.
* **Expected Output:**
  ```text
  PONG
  ```

---

### Step 4: Stop the Container
```bash
docker stop c1
```
* **Explanation:** Halts the primary process inside the container. The status shifts from `Up` to `Exited`.

---

### Step 5: Verify Stopped State & Exit Code
```bash
docker ps -a
```
* **Expected Output:** Shows `c1` in the list with `STATUS: Exited (137)` (indicating manual termination).

---

### Step 6: Resource Cleanup
```bash
# 1. Delete stopped container
docker rm c1

# 2. Delete base image
docker rmi redis
```

> ⚠️ **Key Rule:** You cannot remove an image with `docker rmi` if a container (even an exited one) still references it. Always delete containers before deleting images.
