<div align="center">

# 🛡️ SentinelOps
### Enterprise DevSecOps Security Orchestrator Framework

[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform)]()
[![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazonaws)]()
[![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)]()
[![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-326CE5?logo=kubernetes)]()
[![Jenkins](https://img.shields.io/badge/Jenkins-CI/CD-D24939?logo=jenkins)]()
[![Helm](https://img.shields.io/badge/Helm-Package_Manager-0F1689?logo=helm)]()
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus)]()
[![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800?logo=grafana)]()

### Secure • Automated • Scalable • Cloud Native

</div>

---

# 📖 About SentinelOps

SentinelOps is an **Enterprise DevSecOps Security Orchestrator Framework** designed to automate the secure software delivery lifecycle from code commit to production deployment.

The platform integrates **Infrastructure as Code (IaC), Continuous Integration (CI), Continuous Deployment (CD), Container Security, Kubernetes, Cloud Infrastructure, Monitoring, and Security Automation** into a single workflow.

Unlike traditional CI/CD pipelines, SentinelOps continuously validates application security throughout every stage of the Software Development Life Cycle (SDLC) by integrating multiple security tools directly into the deployment pipeline.

The project demonstrates how modern organizations build, secure, deploy, monitor, and manage cloud-native applications on **Amazon Web Services (AWS)** using **DevSecOps best practices**.

---

# 🎯 Project Objective

The primary objective of SentinelOps is to create an automated DevSecOps platform that:

- Automates Infrastructure Provisioning
- Automates Application Deployment
- Integrates Security Scanning
- Detects Vulnerabilities Early
- Reduces Manual Operations
- Implements Secure CI/CD
- Deploys Applications to Kubernetes
- Continuously Monitors Infrastructure
- Provides Security Visibility
- Supports Enterprise Scalability

---

# 🚀 Features

## Infrastructure Automation

- Infrastructure as Code using Terraform
- Automated AWS Resource Provisioning
- Amazon VPC Architecture
- Public & Private Subnets
- Internet Gateway
- NAT Gateway
- Route Tables
- Security Groups
- IAM Roles & Policies

---

## Containerization

- Dockerized Frontend
- Dockerized Backend
- Multi-stage Docker Builds
- Non-root Containers
- Health Checks
- Optimized Images

---

## CI/CD Automation

- GitHub Webhooks
- Jenkins Pipeline
- Automated Docker Build
- Automated Image Push
- Automated Kubernetes Deployment
- Zero Downtime Rolling Updates
- Rollback Support

---

## DevSecOps Security

Integrated Security Tools

- Gitleaks
- Bandit
- Trivy
- Semgrep
- OWASP ZAP

Security validation occurs automatically during the CI/CD pipeline.

---

## Kubernetes

- Amazon EKS
- Helm Charts
- Deployments
- Services
- ConfigMaps
- Secrets
- Ingress
- AWS Load Balancer Controller
- Rolling Updates
- Rollbacks

---

## Monitoring

- Prometheus
- Grafana
- Alertmanager
- Node Exporter
- kube-state-metrics
- Persistent Storage (Amazon EBS CSI)

---

# 🏗 High Level Architecture

```text
                    Developer
                        │
                        ▼
                GitHub Repository
                        │
                GitHub Webhook
                        │
                        ▼
                  Jenkins Server
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
     Build          Security        Docker Images
                    Validation
        │
        │
        ▼
   Docker Build
        │
        ▼
 Amazon ECR Repository
        │
        ▼
 Helm Deployment
        │
        ▼
 Amazon EKS Cluster
        │
 ┌──────┴───────────────┐
 │                      │
 ▼                      ▼
Frontend            Backend
 │                      │
 └──────────┬───────────┘
            ▼
      AWS Application
      Load Balancer
            │
            ▼
         End Users
```

---

# 🔄 Complete DevSecOps Workflow

```text
Developer
     │
     ▼
Git Push
     │
     ▼
GitHub Repository
     │
     ▼
GitHub Webhook
     │
     ▼
Jenkins Pipeline
     │
     ├──────────────────────────────────────────────┐
     │                                              │
     ▼                                              ▼
Checkout Code                              Pre-Build Security
                                                    │
                                                    ▼
                                              Gitleaks Scan
                                                    │
                                                    ▼
                                               Bandit Scan
                                                    │
                                                    ▼
                                               Semgrep Scan
                                                    │
                                                    ▼
                                                Trivy Scan
                                                    │
                                                    ▼
                                              OWASP ZAP Scan
                                                    │
                                                    ▼
                                           Security Reports
                                                    │
                                                    ▼
                                             Docker Build
                                                    │
                                                    ▼
                                              Push to ECR
                                                    │
                                                    ▼
                                              Helm Deploy
                                                    │
                                                    ▼
                                               Amazon EKS
                                                    │
                                                    ▼
                                          Rolling Deployment
                                                    │
                                                    ▼
                                               Prometheus
                                                    │
                                                    ▼
                                                 Grafana
```

---

# ☁ AWS Architecture

```text
                           AWS Cloud

 ┌──────────────────────────────────────────────────────────┐

                       Amazon VPC

 ┌──────────────────────────────────────────────────────────┐

      Public Subnet                Private Subnet

  ┌──────────────────┐      ┌──────────────────────────┐

       Jenkins EC2             Amazon EKS Cluster

                                ├── Backend Pods
                                ├── Frontend Pods
                                ├── Prometheus
                                ├── Grafana
                                ├── Alertmanager

                                Amazon ECR

                                Amazon EBS

                                AWS ALB

 └──────────────────────────────────────────────────────────┘
```

---

# 🛠 Technology Stack

| Category | Technologies |
|----------|--------------|
| Cloud | AWS |
| Infrastructure | Terraform |
| CI/CD | Jenkins |
| Source Control | GitHub |
| Containers | Docker |
| Container Registry | Amazon ECR |
| Orchestration | Kubernetes (Amazon EKS) |
| Package Manager | Helm |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Alerting | Alertmanager |
| Security | Bandit, Gitleaks, Trivy, Semgrep, OWASP ZAP |
| Backend | Node.js |
| Frontend | React |
| Database | MongoDB |
| Operating System | Ubuntu Linux |
| Shell | Bash |

---

# 📊 Current Project Progress

| Module | Status |
|---------|--------|
| Terraform Infrastructure | ✅ Completed |
| Docker | ✅ Completed |
| Jenkins CI | ✅ Completed |
| DevSecOps Pipeline | ✅ Completed |
| Amazon ECR | ✅ Completed |
| Amazon EKS | ✅ Completed |
| Helm Deployment | ✅ Completed |
| Kubernetes | ✅ Completed |
| Monitoring Stack | ✅ Completed |
| Grafana Dashboard | ✅ Completed |
| Prometheus | ✅ Completed |
| Alertmanager | ✅ Completed |
| GitHub Webhook | ✅ Completed |
| Rolling Updates | ✅ Completed |
| Rollbacks | ✅ Completed |
| Application Metrics | 🚧 In Progress |
| Argo CD | ⏳ Planned |
| Wazuh Integration | ⏳ Planned |
| Snort Integration | ⏳ Planned |
| Compliance Dashboard | ⏳ Planned |
| Terraform Remote Backend | ⏳ Planned |
| Notifications | ⏳ Planned |

---

# ⭐ Key Highlights

- Enterprise-grade DevSecOps Architecture
- Cloud Native Deployment
- Automated Infrastructure Provisioning
- Continuous Security Validation
- Kubernetes-based Deployment
- Infrastructure Monitoring
- Security-first CI/CD Pipeline
- Production-ready Architecture
- Highly Scalable Design
- Modular Infrastructure

# 📂 Repository Structure

```text
SentinelOps/
│
├── app/
│   ├── client/                 # React Frontend
│   └── server/                 # Node.js Backend
│
├── deployment/
│   ├── deploy.sh
│   ├── update-image.sh
│   ├── rollback.sh
│   └── verify-rollout.sh
│
├── docker/
│   ├── backend/
│   └── frontend/
│
├── helm/
│   └── sentinelops/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── monitoring/
│   ├── grafana/
│   ├── dashboards/
│   ├── kube-prometheus/
│   └── storageclass/
│
├── security/
│   ├── core/
│   ├── scanners/
│   ├── reports/
│   └── run_pipeline.sh
│
├── terraform/
│   ├── modules/
│   │   ├── network/
│   │   ├── iam/
│   │   ├── ec2/
│   │   ├── ecr/
│   │   ├── eks/
│   │   └── rds/
│   │
│   ├── main.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
│
├── Jenkinsfile
├── docker-compose.yml
└── README.md
```

---

# 🏗 Infrastructure Architecture

SentinelOps provisions the complete AWS infrastructure using Terraform.

```text
Terraform
     │
     ▼
AWS
 │
 ├── IAM
 ├── VPC
 ├── Public Subnets
 ├── Private Subnets
 ├── Internet Gateway
 ├── NAT Gateway
 ├── Route Tables
 ├── Security Groups
 ├── Jenkins EC2
 ├── Amazon ECR
 ├── Amazon EKS
 └── Worker Nodes
```

Terraform creates every infrastructure component automatically, eliminating manual provisioning and ensuring repeatable deployments.

---

# 🌐 Network Architecture

```text
                    Amazon VPC

         10.0.0.0/16

                │

     ┌──────────┴──────────┐

 Public Subnets        Private Subnets

      │                     │

 Jenkins EC2          Amazon EKS Cluster

      │                     │

 Internet             Backend Pods
                      Frontend Pods
                      Monitoring Stack
```

The application workload is isolated inside private subnets while only Jenkins and the Application Load Balancer are exposed publicly.

---

# 🐳 Container Architecture

Both frontend and backend are containerized.

```text
Backend

Source Code
      │
Dockerfile
      │
Docker Build
      │
Docker Image
      │
Amazon ECR
```

```text
Frontend

React Source
      │
Multi-stage Docker Build
      │
Optimized Image
      │
Amazon ECR
```

### Docker Best Practices

- Multi-stage builds
- Non-root user
- Health checks
- Small image size
- Environment variables
- Layer caching

---

# 🚀 Jenkins CI/CD Pipeline

The Jenkins pipeline automates the complete deployment process.

```text
Git Push
    │
    ▼
GitHub
    │
Webhook
    │
    ▼
Jenkins
```

Pipeline Stages

```text
Checkout
    │
    ▼
Security Scanning
    │
    ▼
Docker Build
    │
    ▼
Push Images
    │
    ▼
Helm Deployment
    │
    ▼
Kubernetes Rollout
```

---

# 🔐 DevSecOps Security Pipeline

Security is integrated into every build.

```text
Developer

↓

GitHub

↓

Jenkins

↓

Gitleaks

↓

Bandit

↓

Semgrep

↓

Trivy

↓

OWASP ZAP

↓

Reports

↓

Deployment
```

---

## Gitleaks

Purpose

Detects accidentally committed secrets.

Examples

- AWS Keys
- API Tokens
- Passwords
- Private Keys

---

## Bandit

Purpose

Performs Static Application Security Testing (SAST) for Python.

Detects

- Insecure functions
- Weak cryptography
- Dangerous subprocess calls
- Hardcoded passwords

---

## Semgrep

Purpose

Language-aware Static Code Analysis.

Detects

- SQL Injection
- Command Injection
- XSS
- Insecure APIs
- Security Misconfigurations

---

## Trivy

Purpose

Container Image Vulnerability Scanner.

Scans

- Docker Images
- Operating System Packages
- Application Libraries

Detects

- Critical
- High
- Medium
- Low Vulnerabilities

---

## OWASP ZAP

Purpose

Dynamic Application Security Testing (DAST)

Detects

- XSS
- SQL Injection
- Authentication Issues
- Missing Security Headers
- Session Problems

---

# ☸ Kubernetes Deployment Architecture

```text
Amazon EKS

│

├── Backend Deployment

├── Frontend Deployment

├── ConfigMaps

├── Secrets

├── Services

├── Ingress

├── Helm

└── Monitoring
```

---

# Helm Deployment Flow

```text
Helm Chart

↓

Templates

↓

Values.yaml

↓

Kubernetes Manifests

↓

Amazon EKS
```

Helm enables version-controlled, reusable, and configurable Kubernetes deployments.

---

# 🌍 Traffic Flow

```text
User

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

↓

MongoDB
```

---

# 📊 Monitoring Architecture

Monitoring is implemented using the Prometheus ecosystem.

```text
Amazon EKS

↓

Node Exporter

↓

kube-state-metrics

↓

Prometheus

↓

Alertmanager

↓

Grafana
```

Prometheus continuously collects metrics from the Kubernetes cluster while Grafana visualizes infrastructure health through dashboards.

---

# 📈 Monitoring Components

## Prometheus

Responsible for

- Metrics Collection
- Time Series Database
- Alert Rules
- Service Discovery

---

## Grafana

Responsible for

- Dashboards
- Visualization
- Querying Prometheus
- Operational Monitoring

---

## Alertmanager

Responsible for

- Alert Routing
- Alert Grouping
- Notification Management

---

## Node Exporter

Provides

- CPU Usage
- Memory Usage
- Filesystem
- Network
- Disk Utilization

---

## kube-state-metrics

Provides

- Pod Status
- Deployments
- ReplicaSets
- DaemonSets
- StatefulSets
- PVC Status

---

# 🔄 Deployment Strategy

SentinelOps uses Kubernetes Rolling Updates.

```text
Old Pods

↓

New Pods Created

↓

Health Checks

↓

Traffic Shift

↓

Old Pods Removed
```

Benefits

- Zero Downtime
- Automatic Rollback Support
- High Availability

---

# 🔁 Rollback Strategy

If deployment fails

```text
Deployment Failure

↓

kubectl rollout undo

↓

Previous Stable Version

↓

Application Restored
```

---

# 🔒 Security Best Practices

SentinelOps implements

- Principle of Least Privilege
- Infrastructure as Code
- Immutable Containers
- Non-root Containers
- Secret Management
- Automated Security Scanning
- Continuous Monitoring
- Kubernetes RBAC Ready
- Secure Image Storage
- Automated Rollbacks

---

# 📊 Current Monitoring Coverage

Infrastructure Metrics

- CPU
- Memory
- Storage
- Network
- Pods
- Nodes

Security Metrics

- Vulnerabilities
- Secret Detection
- Code Quality

Deployment Metrics

- Rollouts
- Rollbacks
- Build Status

Application Metrics

🚧 Planned

Business Metrics

🚧 Planned

Compliance Metrics

🚧 Planned

# ⚙️ Installation Guide

## Prerequisites

Before deploying SentinelOps, ensure the following tools are installed:

| Tool | Version |
|------|----------|
| Git | Latest |
| Terraform | >= 1.5 |
| Docker | Latest |
| kubectl | Latest |
| Helm | v3+ |
| AWS CLI | v2 |
| Jenkins | Latest |
| Node.js | LTS |
| npm | Latest |

---

# ☁️ Step 1: Clone Repository

```bash
git clone https://github.com/<your-username>/SentinelOps.git

cd SentinelOps
```

---

# 🌍 Step 2: Configure AWS

```bash
aws configure
```

Provide

```
Access Key

Secret Key

Region

Output Format
```

---

# 🏗 Step 3: Deploy Infrastructure

```bash
cd terraform

terraform init

terraform plan

terraform apply
```

Terraform creates

- VPC
- IAM
- EC2
- ECR
- EKS
- Networking

---

# 🐳 Step 4: Build Docker Images

Backend

```bash
docker build -t sentinelops-backend .
```

Frontend

```bash
docker build -t sentinelops-frontend .
```

---

# 🚀 Step 5: Push Images

```bash
docker push <ECR_URI>/sentinelops-backend

docker push <ECR_URI>/sentinelops-frontend
```

---

# ☸ Step 6: Deploy Kubernetes

```bash
helm install sentinelops helm/sentinelops
```

Verify

```bash
kubectl get pods -n sentinelops
```

---

# 📊 Step 7: Install Monitoring

```bash
helm install monitoring prometheus-community/kube-prometheus-stack
```

Verify

```bash
kubectl get pods -n monitoring
```

---

# 🔍 Step 8: Verify Deployment

```bash
kubectl get all -n sentinelops
```

```bash
kubectl get ingress
```

```bash
kubectl get svc
```

---

# 📷 Project Screenshots

The following screenshots demonstrate the deployment and monitoring workflow.

## Infrastructure

- Terraform Apply
- AWS Console
- VPC
- EC2
- EKS
- ECR

---

## Jenkins

- Pipeline Success
- Build History
- Security Stage
- Deployment Stage

---

## Kubernetes

- Running Pods
- Services
- Ingress
- Deployments

---

## Monitoring

- Grafana Dashboard
- Prometheus Targets
- Alertmanager
- Node Exporter Dashboard

---

## Security Reports

- Gitleaks
- Bandit
- Trivy
- Semgrep
- OWASP ZAP

---

# 🧪 Pipeline Walkthrough

The following workflow is executed automatically after every Git push.

```text
Developer

↓

Git Push

↓

GitHub

↓

Webhook

↓

Jenkins

↓

Checkout Code

↓

Security Validation

↓

Docker Build

↓

Push to Amazon ECR

↓

Helm Upgrade

↓

Amazon EKS

↓

Rolling Deployment

↓

Prometheus

↓

Grafana

↓

Production
```

---

# 📈 Monitoring Dashboard

Current Dashboards

- Kubernetes Cluster
- Node Exporter
- Prometheus
- Cluster Monitoring

Metrics Collected

- CPU Usage
- Memory Usage
- Disk Usage
- Pod Status
- Deployment Health
- Node Health
- PVC Status
- Network Statistics

---

# 🔐 Security Validation

SentinelOps performs automated security validation during every deployment.

| Tool | Purpose |
|-------|----------|
| Gitleaks | Secret Detection |
| Bandit | Python SAST |
| Semgrep | Static Code Analysis |
| Trivy | Container Vulnerability Scanning |
| OWASP ZAP | Dynamic Security Testing |

Security scans are executed before deployment to prevent insecure applications from reaching production.

---

# 🚀 Future Roadmap

The following features are planned to further enhance SentinelOps.

## Phase 1

- ✅ Terraform
- ✅ Docker
- ✅ Jenkins
- ✅ Kubernetes
- ✅ Helm
- ✅ Monitoring

---

## Phase 2

- Argo CD
- GitOps Deployment
- Automatic Synchronization

---

## Phase 3

- Wazuh SIEM
- Security Event Collection
- Threat Detection

---

## Phase 4

- Snort IDS
- Network Intrusion Detection
- Security Alerts

---

## Phase 5

Compliance Dashboard

- ISO 27001
- NIST CSF
- OWASP Top 10
- CIS Benchmarks

---

## Phase 6

Notification Services

- Email Alerts
- Slack Alerts
- Microsoft Teams

---

## Phase 7

Application Metrics

- Login Requests
- Active Users
- API Response Time
- Request Count
- Error Rate

---

## Phase 8

High Availability

- Horizontal Pod Autoscaler
- Cluster Autoscaler
- Multi-AZ Support
- Backup Strategy

---

# 📚 Key Learnings

This project provided practical experience with:

- Infrastructure as Code
- Cloud Architecture
- DevSecOps
- Docker
- Kubernetes
- Helm
- AWS
- Monitoring
- Security Automation
- CI/CD
- GitOps
- Observability
- Container Security

---

# 💼 Resume Highlights

SentinelOps demonstrates experience with:

- Enterprise DevSecOps
- AWS Cloud
- Terraform
- Jenkins
- Docker
- Kubernetes
- Helm
- Prometheus
- Grafana
- Security Automation
- CI/CD
- Infrastructure Automation
- Cloud Native Applications

---

# 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork Repository
2. Create Feature Branch

```bash
git checkout -b feature/my-feature
```

3. Commit Changes

```bash
git commit -m "Added new feature"
```

4. Push Branch

```bash
git push origin feature/my-feature
```

5. Open Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Mayank Trivedi**

Computer Engineer | DevSecOps Enthusiast | Cloud & Security Engineer

GitHub:

https://github.com/9MayanK2

LinkedIn:

(Add your LinkedIn Profile)

---

# ⭐ Support

If you found this project useful:

⭐ Star this repository

🍴 Fork the repository

📢 Share your feedback

---

# 🎯 Project Vision

SentinelOps is designed to demonstrate how modern organizations can securely build, test, deploy, monitor, and manage cloud-native applications using DevSecOps principles.

The platform combines Infrastructure as Code, Continuous Integration, Continuous Deployment, Container Security, Kubernetes orchestration, cloud-native monitoring, and security automation into a single enterprise-ready solution.

The long-term vision of SentinelOps is to evolve into a centralized DevSecOps platform that integrates CI/CD, GitOps, security scanning, observability, compliance reporting, intrusion detection, and automated remediation, providing organizations with a unified view of their software delivery pipeline and security posture.