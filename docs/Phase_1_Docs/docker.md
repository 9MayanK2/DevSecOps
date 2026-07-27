# DevSecOps Project – Containerization & Orchestration

## Overview

In this phase, the MERN application was containerized using Docker and orchestrated using Docker Compose. The primary objective was to package the frontend and backend into isolated, portable containers while following container security best practices.

This phase establishes the foundation required before integrating CI/CD pipelines, image scanning, Kubernetes deployment, and cloud infrastructure.

---

# Objectives

- Containerize Backend Application
- Containerize Frontend Application
- Build Production Images
- Run Containers
- Configure Health Checks
- Configure Nginx
- Run as Non-root User
- Use Docker Compose
- Create Isolated Docker Network
- Verify Container Communication

---

# Project Structure

```
DevSecOps/
│
├── app/
│   ├── client/
│   │     ├── Dockerfile
│   │     ├── .dockerignore
│   │     └── nginx/
│   │           └── nginx.conf
│   │
│   └── server/
│         ├── Dockerfile
│         └── .dockerignore
│
└── docker-compose.yml
```

---

# Backend Containerization

## Base Image

```
node:22-alpine
```

Reasons:

- Lightweight image
- Smaller attack surface
- Faster image download
- Better security

---

## Working Directory

```
WORKDIR /app
```

Purpose:

Creates and switches into the application directory.

---

## Dependency Installation

```
COPY package*.json ./
RUN npm ci --omit=dev
```

Why npm ci?

- Uses package-lock.json
- Faster
- Deterministic builds
- Suitable for production

---

## Copy Source Code

```
COPY . .
```

Docker ignores:

- node_modules
- .git
- .env
- logs

using `.dockerignore`.

---

## Non-root User

Created:

```
appgroup
appuser
```

Changed ownership:

```
chown -R appuser:appgroup /app
```

Switched user:

```
USER appuser
```

Reason:

Running containers as root is a security risk.

---

## Exposed Port

```
EXPOSE 5000
```

Documents the application's listening port.

---

## Health Check

```
HEALTHCHECK
```

Checks:

```
GET /health
```

Purpose:

- Docker detects unhealthy containers.
- Kubernetes can later use the same endpoint for liveness/readiness probes.

---

## Container Verification

Verified:

- Docker image built successfully
- Container started successfully
- MongoDB Atlas connection successful
- Health endpoint working
- Running as appuser

---

# Frontend Containerization

## Multi-stage Build

### Builder Stage

Image:

```
node:22-alpine
```

Tasks:

- Install dependencies
- Build React application

```
npm run build
```

---

### Production Stage

Image:

```
nginx:alpine
```

Only compiled files copied:

```
build/
```

Result:

Smaller production image.

---

# Nginx

Custom nginx.conf created.

Responsibilities:

- Serve React static files
- React Router support
- Cache static assets
- Health endpoint

Example:

```
/health
```

Returns:

```
healthy
```

---

## React Routing

Configured:

```
try_files
```

Purpose:

Supports client-side routing without 404 errors.

---

## Static Asset Caching

Configured:

```
Cache-Control
expires
```

Improves performance.

---

## Non-root Nginx

Created:

```
appuser
```

Configured writable directories:

- /tmp
- /var/cache/nginx
- /var/log/nginx

Nginx configured to:

```
listen 8080;
```

instead of:

```
listen 80;
```

Reason:

Non-root users cannot bind to privileged ports (<1024).

---

## Health Check

Docker Health Check:

```
wget http://127.0.0.1:8080/health
```

Important lesson:

Using

```
localhost
```

failed because BusyBox wget resolved localhost differently.

Using

```
127.0.0.1
```

worked successfully.

---

# .dockerignore

Created for both services.

Ignored:

```
node_modules
.git
.env
logs
Docker cache
```

Benefits:

- Faster builds
- Smaller build context
- Prevents secrets from entering images

---

# Docker Images

Successfully created:

Backend

```
hopegivers-backend
```

Frontend

```
hopegivers-frontend
```

Verified using:

```
docker images
docker history
docker inspect
```

---

# Container Verification

Verified:

```
docker ps
```

```
docker logs
```

```
docker exec
```

```
whoami
```

Confirmed:

```
appuser
```

instead of root.

---

# Docker Networking

Docker Compose automatically created:

```
devsecops_devsecops-network
```

Both containers attached to the same bridge network.

Verified using:

```
docker network inspect
```

Containers communicate through service names instead of localhost.

Example:

```
http://hopegivers-backend:5000
```

---

# Docker Compose

Created:

```
docker-compose.yml
```

Responsibilities:

- Build backend
- Build frontend
- Create network
- Start containers
- Configure restart policy
- Health checks
- Environment variables
- Port mappings

Single command:

```
docker-compose up -d
```

starts the complete application.

---

# Environment Variables

Backend:

Uses

```
.env
```

for

- MongoDB Atlas URI
- JWT Secret
- Email credentials

Frontend:

Uses

```
REACT_APP_API_URL
```

Build-time environment variable.

`.env` files remain outside Docker images because they are ignored by `.dockerignore`.

---

# Verification Performed

Successfully verified:

- Backend image
- Frontend image
- Docker history
- Docker inspect
- Health checks
- Container logs
- Docker Compose
- Docker network
- Container communication
- Non-root execution
- Nginx configuration
- Static file serving

---

# Best Practices Implemented

- Alpine base images
- npm ci
- Multi-stage build
- Non-root containers
- Docker health checks
- Separate frontend/backend images
- .dockerignore
- Docker Compose
- Custom Nginx configuration
- React Router support
- Static asset caching
- Smaller production images

---

# Lessons Learned

## Dockerfile

- Layer caching
- COPY order
- npm ci vs npm install
- WORKDIR
- CMD
- EXPOSE
- HEALTHCHECK
- USER

---

## Docker

- Images
- Containers
- Layers
- Build cache
- Volumes
- Networks
- Inspect
- History
- Logs
- Exec

---

## Nginx

- Reverse proxy basics
- Static file hosting
- React SPA routing
- Health endpoint
- Cache headers

---

## Docker Compose

- Multi-container orchestration
- Automatic networking
- Service discovery
- Port mapping
- Container lifecycle

---

# Outcome

At the end of this phase, the complete MERN application runs inside Docker containers with:

- Secure backend container
- Secure frontend container
- Custom Nginx configuration
- Non-root execution
- Health monitoring
- Docker Compose orchestration
- Shared bridge network
- Production-ready container structure

This provides the foundation for the next phase of the DevSecOps pipeline.

---

# Next Phase

## Container Security

The next phase introduces automated security checks on Docker images before deployment.

Planned tools:

1. Hadolint (Dockerfile linting)
2. Trivy (Vulnerability Scanning)
3. Docker Scout (Image Analysis)
4. Syft (SBOM Generation)

After completing these checks, the project will move into Jenkins CI/CD integration, AWS ECR image publishing, and Kubernetes deployment.
