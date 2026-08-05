# ☸️ Kubernetes Architecture

> **Document Version:** 1.0
>
> **Project:** SentinelOps – Enterprise DevSecOps Security Orchestrator Framework

---

# Table of Contents

1. Introduction
2. Why Kubernetes?
3. SentinelOps Kubernetes Architecture
4. Amazon EKS Cluster
5. Namespaces
6. Application Components
7. Deployments
8. Services
9. Ingress
10. Persistent Storage
11. Monitoring Stack
12. Kubernetes Networking
13. Deployment Strategy
14. High Availability
15. Security Best Practices
16. Future Enhancements
17. Summary

---

# 1. Introduction

SentinelOps uses **Amazon Elastic Kubernetes Service (EKS)** as its container orchestration platform.

Kubernetes manages the complete lifecycle of application containers including deployment, scaling, service discovery, rolling updates, self-healing, and persistent storage.

Instead of deploying Docker containers directly on virtual machines, SentinelOps deploys workloads as Kubernetes resources managed by the control plane.

---

# 2. Why Kubernetes?

Traditional Docker deployments become difficult to manage as applications grow.

Problems include:

- Manual container management
- No automatic recovery
- Difficult scaling
- No service discovery
- Downtime during deployments

Kubernetes solves these problems by providing:

- Self-healing
- Rolling updates
- Automatic scheduling
- Service discovery
- Load balancing
- High availability
- Declarative deployments

---

# 3. SentinelOps Kubernetes Architecture

```text
                     Amazon EKS

                          │

          ┌───────────────┴───────────────┐

          ▼                               ▼

   sentinelops Namespace          monitoring Namespace

          │                               │

    Frontend Deployment            Prometheus

    Backend Deployment             Grafana

    Services                       Alertmanager

    Ingress                        Node Exporter

                                   kube-state-metrics
```

The application and monitoring components are separated into dedicated namespaces for improved organization and operational isolation.

---

# 4. Amazon EKS Cluster

The SentinelOps platform runs on an Amazon EKS cluster provisioned through Terraform.

Current architecture includes:

- Managed Control Plane
- Managed Node Group
- Worker Nodes
- Private Networking
- IAM Integration
- EBS CSI Driver
- AWS Load Balancer Controller

The managed control plane removes the operational overhead of maintaining Kubernetes master nodes.

---

# 5. Namespaces

SentinelOps uses multiple namespaces to logically separate workloads.

## sentinelops

Contains:

- Frontend
- Backend
- Services
- Ingress
- ConfigMaps
- Secrets

---

## monitoring

Contains:

- Prometheus
- Grafana
- Alertmanager
- Node Exporter
- kube-state-metrics

Separating workloads into namespaces improves resource organization and simplifies access control.

---

# 6. Application Components

The application consists of two primary workloads.

## Frontend

Technology:

- React
- Vite

Responsibilities:

- User Interface
- Dashboard
- Authentication Pages
- API Communication

---

## Backend

Technology:

- Node.js
- Express

Responsibilities:

- REST APIs
- Authentication
- Business Logic
- Database Access

Both components are deployed independently, allowing separate scaling and updates.

---

# 7. Deployments

Deployments ensure that the desired number of Pods are always running.

Current deployments include:

```text
Frontend Deployment

↓

Frontend Pods
```

```text
Backend Deployment

↓

Backend Pods
```

Monitoring deployments:

- Grafana
- Prometheus Operator
- kube-state-metrics
- Node Exporter
- Alertmanager

Deployments enable rolling updates and automatic recovery when Pods fail.

---

# 8. Services

Services provide stable networking for Kubernetes workloads.

Current services include:

| Service | Purpose |
|----------|----------|
| Frontend Service | Access React application |
| Backend Service | Access REST APIs |
| Grafana Service | Access monitoring dashboard |
| Prometheus Service | Metrics collection |

Services abstract Pod IP addresses, allowing applications to communicate reliably even when Pods are recreated.

---

# 9. Ingress

SentinelOps uses the **AWS Load Balancer Controller** to expose Kubernetes services through an **Application Load Balancer (ALB)**.

Example routes:

```text
/

↓

Frontend
```

```text
/api

↓

Backend
```

```text
/health

↓

Backend Health Endpoint
```

```text
/grafana

↓

Grafana Dashboard
```

Ingress centralizes external traffic management while allowing path-based routing to different services.

---

# 10. Persistent Storage

Monitoring components require persistent storage to retain metrics and dashboards.

SentinelOps uses:

- Amazon EBS
- EBS CSI Driver
- StorageClass: gp3

Persistent storage is allocated for:

- Prometheus
- Grafana
- Alertmanager

This ensures that monitoring data is preserved across Pod restarts and upgrades.

---

# 11. Monitoring Stack

The monitoring namespace provides observability for the Kubernetes cluster.

Components:

## Prometheus

Collects metrics from:

- Nodes
- Pods
- Services
- Kubernetes API

---

## Grafana

Visualizes collected metrics using dashboards.

Provides insights into:

- CPU utilization
- Memory usage
- Pod health
- Cluster performance

---

## Alertmanager

Processes alerts generated by Prometheus.

Supports notification routing and alert grouping.

---

## Node Exporter

Collects node-level metrics such as:

- CPU
- Memory
- Disk
- Network

---

## kube-state-metrics

Exports Kubernetes object metrics including:

- Deployments
- ReplicaSets
- Pods
- Nodes
- StatefulSets

---

# 12. Kubernetes Networking

Traffic flows through the cluster as follows:

```text
Internet

↓

AWS ALB

↓

Ingress

↓

Frontend Service

↓

Frontend Pods

↓

Backend Service

↓

Backend Pods
```

Internal communication between services remains within the Kubernetes cluster.

---

# 13. Deployment Strategy

SentinelOps uses declarative deployments managed by Helm.

Deployment process:

```text
Helm Upgrade

↓

Deployment Updated

↓

New ReplicaSet

↓

New Pods Created

↓

Health Verification

↓

Old Pods Removed
```

This rolling update strategy minimizes downtime during application upgrades.

---

# 14. High Availability

The platform is designed for resilience.

Current implementation includes:

- Multiple worker nodes
- Multiple Pod replicas
- Managed node groups
- Rolling deployments
- Self-healing workloads

Future enhancements:

- Horizontal Pod Autoscaler (HPA)
- Cluster Autoscaler
- Pod Disruption Budgets
- Multi-AZ database deployments

---

# 15. Security Best Practices

SentinelOps follows Kubernetes security best practices.

Implemented:

- Namespace isolation
- Non-root containers
- Kubernetes Secrets
- IAM Roles for Service Accounts (IRSA)
- AWS Security Groups
- Persistent storage through EBS CSI Driver
- Health probes
- Immutable container images

Future improvements:

- Network Policies
- Pod Security Standards
- Admission Controllers
- Secrets Manager integration
- Runtime security monitoring

---

# 16. Future Enhancements

The Kubernetes platform has been designed for future expansion.

Planned additions include:

- Argo CD GitOps deployments
- Wazuh agents
- Snort IDS
- Horizontal Pod Autoscaler
- Cluster Autoscaler
- Service Mesh (Istio)
- Distributed tracing
- Multi-cluster deployments
- Disaster recovery automation

---

# 17. Summary

Amazon EKS serves as the runtime platform for SentinelOps, providing container orchestration, service discovery, persistent storage, and high availability.

Through Kubernetes Deployments, Services, Ingress resources, Helm charts, and the monitoring stack, SentinelOps delivers a resilient and scalable platform capable of supporting secure software delivery and future enterprise DevSecOps capabilities.