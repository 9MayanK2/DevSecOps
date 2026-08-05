# SentinelOps - Architecture & Project Guide Documentation (Detail)

The `Detail/` directory holds official PDF reference documents, enterprise architecture diagrams, and comprehensive project guides for the SentinelOps DevSecOps Automated Security Pipeline.

---

## 📁 Directory Content Overview

| Document Name | Description | Key Topics |
| :--- | :--- | :--- |
| `DevSecOps_Project_Guide.pdf` | **Official Master Project Blueprint** | Full 12-week roadmap, team role splits, syllabus mapping, interview talking points, and phase-by-phase implementation plans. |
| `DevSecOps Automated Security Pipeline — Architecture.pdf` | **Visual System Architecture** | Enterprise 6-Layer DevSecOps flow: Dev -> CI/CD -> Security Gate -> K8s Cloud -> Observability -> Compliance. |

---

## 🏗️ 6-Layer Security Architecture Flowchart

```mermaid
flowchart LR
    subgraph L1["Layer 1: Developer Workstation"]
        A1[Git Commit] --> A2[Bandit SAST]
        A1 --> A3[Gitleaks Secrets Scan]
    end

    subgraph L2["Layer 2: CI/CD Automation (Jenkins)"]
        B1[Jenkins Trigger] --> B2[Docker Build]
        B2 --> B3[Hadolint Dockerfile Scan]
        B2 --> B4[Trivy Container Scan]
    end

    subgraph L3["Layer 3: Security Gate & Engine"]
        C1[Python Orchestrator] --> C2[OWASP ZAP DAST]
        C1 --> C3[CVSS Risk Scoring Engine]
        C3 --> C4[Cosign Image Signing]
    end

    subgraph L4["Layer 4: Cloud & Orchestration"]
        D1[AWS ECR Push] --> D2[AWS EKS Cluster]
        D2 --> D3[Kubernetes RBAC & NetPol]
    end

    subgraph L5["Layer 5: Observability & Defense"]
        E1[Prometheus & Grafana] --> E2[Wazuh HIDS & Snort NIDS]
    end

    subgraph L6["Layer 6: Compliance & Audit"]
        F1[SQLite DB] --> F2[NIST / ISO 27001 Auto-Mapping Dashboard]
    end

    L1 --> L2 --> L3 --> L4 --> L5 --> L6
```

---

## 📖 Usage Instructions

These PDF files serve as reference material for project evaluation, technical audits, team alignment, and DevSecOps interview preparation.
