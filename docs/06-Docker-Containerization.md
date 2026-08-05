# 🐳 Docker Containerization

> **Document Version:** 1.0
>
> **Project:** SentinelOps – Enterprise DevSecOps Security Orchestrator Framework

---

# Table of Contents

1. Introduction
2. Why Docker?
3. Why Containers Instead of Virtual Machines?
4. Containerization Strategy
5. Project Structure
6. Backend Container
7. Frontend Container
8. Docker Compose
9. Image Build Process
10. Image Security
11. Amazon ECR Integration
12. Deployment Workflow
13. Best Practices
14. Future Improvements
15. Summary

---

# 1. Introduction

Modern cloud-native applications require consistency across development, testing, and production environments.

SentinelOps uses Docker to package every application component together with its runtime dependencies into lightweight, portable, and reproducible containers.

Instead of deploying source code directly on virtual machines, SentinelOps deploys immutable Docker images, ensuring identical execution across every environment.

---

# 2. Why Docker?

Docker was selected because it provides:

- Environment consistency
- Fast deployments
- Lightweight isolation
- Dependency packaging
- Simplified scalability
- Cloud-native compatibility
- Kubernetes integration

Containerization removes the common "works on my machine" problem by ensuring every environment runs the same application image.

---

# 3. Why Containers Instead of Virtual Machines?

Traditional deployment

```text
Server

↓

Operating System

↓

Application

↓

Dependencies
```

Problems

- Environment mismatch
- Manual dependency installation
- Difficult scaling
- Slow deployment

---

Docker deployment

```text
Docker Image

↓

Docker Engine

↓

Container

↓

Application Ready
```

Benefits

- Portable
- Lightweight
- Fast startup
- Immutable
- Easy rollback

---

# 4. Containerization Strategy

SentinelOps separates the application into independent containers.

```text
                SentinelOps

                     │

      ┌──────────────┴──────────────┐

      ▼                             ▼

Frontend Container            Backend Container

      │                             │

React Application          Node.js Application

      │                             │

      └──────────────┬──────────────┘

                     ▼

               Kubernetes
```

Each container is independently deployable and scalable.

---

# 5. Project Structure

```text
docker/

├── backend/
│   └── Dockerfile
│
├── frontend/
│   └── Dockerfile
│
└── docker-compose.yml
```

---

# 6. Backend Container

The backend container packages the Express.js API together with all required Node.js dependencies.

Responsibilities

- Serve REST APIs
- Authenticate users
- Connect to MongoDB
- Handle business logic
- Expose health endpoint

Container Features

- Alpine Linux base image
- Non-root user
- Optimized layers
- Health Check
- Environment Variables

---

## Backend Build Flow

```text
Node.js Source

↓

Install Dependencies

↓

Copy Source Code

↓

Build Image

↓

Run Container
```

---

## Backend Security

The backend image follows several security best practices.

Implemented

- Non-root container
- Minimal base image
- Docker Healthcheck
- Environment variables
- Layer optimization

---

# 7. Frontend Container

The frontend is built using a multi-stage Docker build.

Stage 1

Application Build

Stage 2

Production Runtime

Benefits

- Smaller image size
- No build dependencies
- Faster deployment
- Reduced attack surface

---

## Frontend Build Flow

```text
React Source

↓

Install Dependencies

↓

Vite Build

↓

Static Assets

↓

Production Image
```

---

# 8. Docker Compose

Docker Compose provides a local development environment where multiple containers can run together.

Current services include:

- Backend
- Frontend

Future additions may include:

- MongoDB
- Redis
- Security tools

Compose simplifies local testing before deployment to Kubernetes.

---

# 9. Image Build Process

The CI pipeline generates Docker images automatically.

```text
GitHub

↓

Jenkins

↓

Docker Build

↓

Docker Image

↓

Amazon ECR
```

Each image is tagged and stored in Amazon ECR before deployment.

---

# 10. Image Security

Container security begins during image creation.

Security measures include:

- Minimal base images
- Layer optimization
- Vulnerability scanning
- Non-root execution
- Health checks

The CI pipeline integrates Trivy to scan container images before deployment.

---

# 11. Amazon ECR Integration

Amazon Elastic Container Registry acts as the centralized image repository.

Stored images

```text
sentinelops-backend

sentinelops-frontend
```

Deployment workflow

```text
Docker Build

↓

Amazon ECR

↓

Amazon EKS
```

Using ECR provides:

- Version control
- Secure image storage
- IAM integration
- High availability

---

# 12. Container Deployment Workflow

```text
Developer

↓

Source Code

↓

GitHub

↓

Jenkins

↓

Docker Build

↓

Amazon ECR

↓

Helm

↓

Amazon EKS

↓

Running Containers
```

Containers are never deployed directly.

Kubernetes always deploys images stored in Amazon ECR.

---

# 13. Best Practices

SentinelOps follows modern container security practices.

Implemented

- Multi-stage builds
- Non-root containers
- Health checks
- Lightweight base images
- Immutable images
- CI/CD image builds
- Container vulnerability scanning

Future enhancements

- Image signing (Cosign)
- Software Bill of Materials (SBOM)
- Admission Controller validation
- Distroless images
- Docker Content Trust

---

# 14. Future Improvements

Planned enhancements include:

- Private image signing
- Image provenance
- Supply-chain security
- OCI artifact support
- Automated image cleanup
- Multi-architecture builds
- Registry replication

---

# 15. Summary

Docker provides the containerization layer for SentinelOps by packaging the frontend and backend applications into immutable, portable images.

Combined with Amazon ECR, Kubernetes, and Jenkins, Docker enables secure, repeatable, and scalable application deployments while supporting modern DevSecOps practices.