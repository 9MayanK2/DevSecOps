# ☁ AWS Infrastructure Architecture

> **Document Version:** 1.0
>
> **Project:** SentinelOps – Enterprise DevSecOps Security Orchestrator Framework

---

# Table of Contents

1. Introduction
2. Why AWS?
3. AWS Architecture Overview
4. Infrastructure Components
5. Networking Architecture
6. IAM & Security
7. Compute Layer
8. Container Registry
9. Kubernetes Platform
10. Storage Layer
11. Networking Flow
12. Terraform Module Design
13. High Availability
14. Security Best Practices
15. Future Enhancements

---

# 1. Introduction

SentinelOps is deployed entirely on **Amazon Web Services (AWS)** using Infrastructure as Code (Terraform).

Instead of manually provisioning cloud resources through the AWS Console, every infrastructure component is automatically created, configured, and version-controlled.

This ensures:

- Reproducible deployments
- Infrastructure consistency
- Easy disaster recovery
- Version-controlled cloud infrastructure
- Enterprise scalability

The infrastructure follows AWS Well-Architected Framework principles by separating networking, compute, storage, security, and orchestration into independent modules.

---

# 2. Why AWS?

AWS provides a mature cloud platform with managed services that simplify infrastructure management while maintaining security and scalability.

SentinelOps uses AWS because it offers:

- Managed Kubernetes (Amazon EKS)
- Secure Container Registry (Amazon ECR)
- Infrastructure Automation
- Identity and Access Management
- High Availability
- Load Balancing
- Persistent Block Storage
- Auto Scaling

AWS allows SentinelOps to focus on secure software delivery rather than infrastructure maintenance.

---

# 3. AWS Infrastructure Overview

```text
                           Internet
                               │
                               ▼
                   AWS Application Load Balancer
                               │
────────────────────────────────────────────────────────────
                    Public Subnets
────────────────────────────────────────────────────────────

        Jenkins EC2

        NAT Gateway

────────────────────────────────────────────────────────────
                   Private Subnets
────────────────────────────────────────────────────────────

               Amazon EKS Cluster

      ┌──────────────────────────────┐

      Worker Node Group

      Frontend Pods

      Backend Pods

      Prometheus

      Grafana

      Alertmanager

      └──────────────────────────────┘

────────────────────────────────────────────────────────────

Amazon ECR

Amazon EBS

IAM Roles

CloudWatch (Future)

Route53 (Future)
```

---

# 4. Infrastructure Components

SentinelOps infrastructure consists of the following AWS services.

| Service | Purpose |
|----------|----------|
| VPC | Network Isolation |
| Public Subnets | Internet-facing Resources |
| Private Subnets | Application Workloads |
| Internet Gateway | Public Connectivity |
| NAT Gateway | Outbound Internet Access |
| Security Groups | Firewall Rules |
| IAM | Authentication & Authorization |
| EC2 | Jenkins Server |
| Amazon ECR | Docker Image Repository |
| Amazon EKS | Kubernetes Platform |
| Amazon EBS | Persistent Storage |
| Application Load Balancer | External Traffic Routing |

---

# 5. Networking Architecture

The network follows a two-tier architecture.

## Public Network

Contains:

- Jenkins
- ALB
- NAT Gateway

These resources must communicate with the Internet.

---

## Private Network

Contains:

- Kubernetes Worker Nodes
- Backend
- Frontend
- Monitoring Stack

No application workload is directly exposed to the Internet.

---

# Network Flow

```text
Internet

↓

ALB

↓

Ingress

↓

Frontend

↓

Backend

↓

MongoDB
```

---

# Why Public & Private Subnets?

Separating workloads improves security.

Public Subnets

Purpose:

Receive external traffic.

Private Subnets

Purpose:

Run business applications securely without direct Internet exposure.

---

# Internet Gateway

The Internet Gateway allows resources inside the VPC to communicate with the Internet.

Used by:

- Jenkins
- ALB

---

# NAT Gateway

Worker Nodes require Internet access to:

- Pull Docker Images
- Install Packages
- Access AWS APIs

Instead of exposing nodes publicly, outbound traffic passes through the NAT Gateway.

Benefits:

- Secure outbound access
- No inbound Internet traffic
- Improved security posture

---

# Route Tables

Public Route Table

```
0.0.0.0/0

↓

Internet Gateway
```

Private Route Table

```
0.0.0.0/0

↓

NAT Gateway
```

---

# 6. IAM & Security

AWS IAM controls access between services.

SentinelOps follows the Principle of Least Privilege.

Current IAM Roles

- Jenkins EC2
- EKS Cluster Role
- Worker Node Role
- AWS Load Balancer Controller
- EBS CSI Driver

Each component receives only the permissions it requires.

---

# OIDC & IAM Roles for Service Accounts (IRSA)

To securely grant AWS permissions to Kubernetes workloads, SentinelOps uses:

- Amazon EKS OIDC Provider
- IAM Roles for Service Accounts (IRSA)

Benefits:

- No static AWS credentials inside Pods
- Fine-grained permissions
- Improved security
- Easier auditing

Current usage includes the EBS CSI Driver, and the same approach can be extended to future components such as the AWS Load Balancer Controller and other controllers that interact with AWS APIs.

---

# 7. Compute Layer

## Jenkins EC2

Jenkins performs:

- Pipeline Execution
- Security Validation
- Docker Build
- Image Push
- Kubernetes Deployment

Keeping Jenkins outside Kubernetes separates CI infrastructure from production workloads.

---

# Amazon EKS

Amazon EKS manages containerized workloads.

Responsibilities

- Scheduling
- Scaling
- Self-Healing
- Rolling Updates
- Service Discovery

SentinelOps currently deploys:

- Frontend
- Backend
- Monitoring Stack

Future workloads

- ArgoCD
- Wazuh
- Snort

---

# Worker Nodes

Managed Node Groups execute Pods.

Benefits

- Automatic upgrades
- Auto recovery
- High Availability

---

# 8. Container Registry

Amazon ECR stores Docker images.

Images

```
sentinelops-backend

sentinelops-frontend
```

Deployment Flow

```
Docker Build

↓

Amazon ECR

↓

Amazon EKS
```

---

# 9. Storage Layer

Persistent storage is provided through Amazon EBS.

Current consumers

- Prometheus
- Grafana
- Alertmanager

The EBS CSI Driver dynamically provisions volumes using the `gp3` StorageClass, ensuring monitoring data persists across Pod restarts.

---

# 10. Kubernetes Networking

```text
Internet

↓

ALB

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

All inter-service communication occurs within the Kubernetes cluster.

---

# 11. Terraform Module Design

SentinelOps infrastructure is organized into reusable Terraform modules.

```
terraform/

modules/

network/

iam/

ec2/

ecr/

eks/

rds/
```

Benefits

- Modular Design
- Code Reusability
- Easier Maintenance
- Independent Updates

---

# Module Responsibilities

## Network

Creates

- VPC
- Subnets
- Route Tables
- NAT Gateway
- Internet Gateway

---

## IAM

Creates

- IAM Roles
- IAM Policies
- Role Attachments

---

## EC2

Creates

- Jenkins Server

---

## ECR

Creates

- Backend Repository
- Frontend Repository

---

## EKS

Creates

- Cluster
- Managed Node Group
- OIDC Configuration

---

## RDS

Reserved for future database deployments.

---

# 12. High Availability

SentinelOps is designed for high availability.

Implemented

- Multiple Worker Nodes
- Multi-Subnet Deployment
- Managed Node Groups
- Rolling Updates

Future Enhancements

- Cluster Autoscaler
- Horizontal Pod Autoscaler
- Multi-AZ Database
- Cross-Region Disaster Recovery

---

# 13. Security Best Practices

Current practices include:

- Infrastructure as Code
- Private Subnets
- Principle of Least Privilege
- IAM Roles
- Kubernetes Secrets
- Non-root Containers
- Image Scanning
- Continuous Monitoring

Future enhancements include:

- AWS WAF
- AWS Shield
- AWS Secrets Manager
- KMS Encryption
- GuardDuty Integration

---

# 14. Infrastructure Deployment Flow

```text
Terraform Init

↓

Terraform Plan

↓

Terraform Apply

↓

AWS Resources Created

↓

Configure kubectl

↓

Deploy Monitoring

↓

Deploy Application

↓

Application Ready
```

---

# 15. Summary

The AWS infrastructure of SentinelOps provides a secure, scalable, and automated foundation for modern DevSecOps practices.

By combining Terraform, Amazon EKS, Amazon ECR, IAM, VPC networking, and persistent storage, the platform enables reliable application delivery while supporting future capabilities such as GitOps, runtime security, compliance automation, and enterprise monitoring.