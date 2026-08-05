# 🔐 SentinelOps

<p align="center">
  <img src="https://img.shields.io/badge/DevSecOps-Production--Grade-0ea5e9?style=for-the-badge&logo=shield&logoColor=white" alt="DevSecOps">
  <img src="https://img.shields.io/badge/Security-Shift--Left-22c55e?style=for-the-badge&logo=lock&logoColor=white" alt="Shift Left">
  <img src="https://img.shields.io/badge/Cloud-AWS-ff9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS">
  <img src="https://img.shields.io/badge/Orchestration-Kubernetes-326ce5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/GitOps-ArgoCD-fc6d26?style=for-the-badge&logo=argo&logoColor=white" alt="ArgoCD">
</p>

<h3 align="center">End-to-End Automated Security Pipeline</h3>
<p align="center"><i>Security by Design. Automation by Default.</i></p>

---

## 🎯 The Problem

```
+-----------------------------------------------------------------------------+
|                                                                             |
|   EVERY DAY, THOUSANDS OF LINES OF CODE ARE PUSHED TO PRODUCTION...         |
|                                                                             |
|   BUT HERE IS THE TERRIFYING TRUTH:                                         |
|                                                                             |
|   +------------------+  +------------------+  +------------------+         |
|   |  HARDCODED       |  |  CRITICAL CVEs   |  |  RUNTIME ATTACKS |         |
|   |  SECRETS IN      |  |  IN CONTAINER    |  |  UNDETECTED      |         |
|   |  GITHUB REPOS    |  |  IMAGES          |  |  FOR WEEKS       |         |
|   +------------------+  +------------------+  +------------------+         |
|                                                                             |
|   MOST VULNERABILITIES ARE DISCOVERED *AFTER* DEPLOYMENT.                   |
|                                                                             |
|   WHAT IF SECURITY WASN'T A FINAL CHECKPOINT...                             |
|   BUT WAS BAKED INTO EVERY SINGLE STAGE OF YOUR PIPELINE?                   |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## ✨ The Solution — SentinelOps

```
+=============================================================================+
|                                                                             |
|   SENTINELOPS  —  A PRODUCTION-GRADE, END-TO-END DEVSECOPS PIPELINE        |
|                                                                             |
|   +----------------+  +----------------+  +----------------+               |
|   |  REACT 19      |  |  NODE.JS 20    |  |  MONGODB       |               |
|   |  FRONTEND      |  |  EXPRESS API   |  |  DATABASE      |               |
|   +----------------+  +----------------+  +----------------+               |
|          |                     |                     |                     |
|          +---------------------+---------------------+                     |
|                                |                                           |
|                                V                                           |
|   +=====================================================================+  |
|   |  SIX-LAYER SECURITY ARCHITECTURE  —  FROM CODE TO RUNTIME          |  |
|   +---------------------------------------------------------------------+  |
|                                                                             |
+=============================================================================+
```

**SentinelOps** is a full-stack application (React + Node.js/Express + MongoDB) deployed on **Amazon EKS**, surrounded by a **six-layer security architecture** that automates security at every stage — from the developer's laptop to production runtime.

---

## 🏗️ Complete Pipeline Flowchart

This is the **single view** of how code travels from a developer's machine to a secured, monitored production environment:

```
+-----------------------------------------------------------------------------+
|                                                                             |
|  DEVELOPER'S LAPTOP                                                         |
|  +---------------------+                                                    |
|  |  git commit -m ...  |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|             V                                                               |
|  +---------------------+     BLOCKED IF SECRETS/ISSUES FOUND               |
|  |  PRE-COMMIT HOOKS   |--------------------------------------------------->|
|  |  * Gitleaks         |                                                    |
|  |  * Semgrep (SAST)   |                                                    |
|  |  * ESLint           |                                                    |
|  |  * File Hygiene     |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|             V  (Code passes hooks)                                          |
|  +---------------------+                                                    |
|  |  git push origin    |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
+-------------|---------------------------------------------------------------+
              |
              V
+-----------------------------------------------------------------------------+
|  GITHUB REPOSITORY                                                          |
|  +---------------------+                                                    |
|  |  Webhook Trigger    |--------------------------------------------------->|
|  +----------+----------+                                                    |
|             |                                                               |
+-------------|---------------------------------------------------------------+
              |
              V
+-----------------------------------------------------------------------------+
|  JENKINS CI/CD — 17 STAGES                                                  |
|                                                                             |
|  [1] Checkout  ->  [2] Install Deps  ->  [3] Generate .env                 |
|       |                  |                      |                           |
|       V                  V                      V                           |
|  [4] Pre-Commit Validation                                                  |
|       |                                                                     |
|       V                                                                     |
|  [5] Hadolint  ->  [6] Build Backend  ->  [7] Build Frontend               |
|       |                  |                      |                           |
|       V                  V                      V                           |
|  [8] Trivy CVE Scan  ->  [9] OWASP ZAP DAST                                |
|       |                      |                                              |
|       V                      V                                              |
|  [10] Generate Reports  ->  [11] Security Gate (Pass/Fail)                 |
|       |                      |                                              |
|       V                      V                                              |
|  [12] Cosign Sign  ->  [13] Verify Signatures                              |
|       |                                                                     |
|       V                                                                     |
|  [14] Login ECR  ->  [15] Push Signed Images                               |
|       |                                                                     |
|       V                                                                     |
|  [16] Deploy to EKS  ->  [17] Verify Rollout                               |
|       |                                                                     |
|       V                                                                     |
|  +---------------------+     +---------------------+                        |
|  |   SUCCESS           |     |   FAILURE           |                        |
|  |   Archive Reports   |     |   Auto Rollback     |                        |
|  |   Clean Resources   |     |   Alert Team        |                        |
|  +---------------------+     +---------------------+                        |
|                                                                             |
+-----------------------------------------------------------------------------+
              |
              V
+-----------------------------------------------------------------------------+
|  AMAZON ECR (Container Registry)                                            |
|  +---------------------+  +---------------------+                          |
|  |  sentinelops-backend  |  |  sentinelops-frontend |                          |
|  |  build-42 (signed)    |  |  build-42 (signed)    |                          |
|  |  latest (signed)      |  |  latest (signed)      |                          |
|  +----------+----------+  +----------+----------+                          |
|             |                      |                                        |
+-------------|----------+-----------|----------------------------------------+
              |          |           |
              V          V           V
+-----------------------------------------------------------------------------+
|  ARGOCD GITOPS (Future State)                                               |
|  +---------------------+                                                    |
|  |  Watches ECR for    |                                                    |
|  |  new image tags     |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|             V                                                               |
|  +---------------------+                                                    |
|  |  Updates Helm       |                                                    |
|  |  values in Git      |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|             V  (Auto-sync every 3 min)                                      |
|  +---------------------+                                                    |
|  |  Deploys to EKS     |                                                    |
|  |  (Desired = Actual) |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
+-------------|---------------------------------------------------------------+
              |
              V
+-----------------------------------------------------------------------------+
|  AMAZON EKS — PRODUCTION CLUSTER                                            |
|  +---------------------+  +---------------------+                          |
|  |  Backend Pods       |  |  Frontend Pods      |                          |
|  |  (Replica: 2)       |  |  (Replica: 2)       |                          |
|  +----------+----------+  +----------+----------+                          |
|             |                      |                                        |
|             +----------+-----------+                                        |
|                        |                                                    |
|                        V                                                    |
|  +---------------------+  +---------------------+                          |
|  |  ALB (Ingress)      |  |  AWS Secrets Mgr    |                          |
|  |  + WAF Protection   |  |  (via CSI Driver)   |                          |
|  +----------+----------+  +---------------------+                          |
|             |                                                               |
+-------------|---------------------------------------------------------------+
              |
              V
+-----------------------------------------------------------------------------+
|  MONITORING & SIEM STACK                                                    |
|  +----------------+  +----------------+  +----------------+               |
|  |  PROMETHEUS    |  |  GRAFANA       |  |  ELK STACK     |               |
|  |  (Metrics)     |  |  (Dashboards)  |  |  (Logs)        |               |
|  +----------------+  +----------------+  +----------------+               |
|  +----------------+  +----------------+                                   |
|  |  WAZUH (HIDS)  |  |  SNORT (NIDS)  |                                   |
|  |  File Integrity|  |  Port Scans    |                                   |
|  |  Rootkit Detect|  |  C2 Traffic    |                                   |
|  +----------------+  +----------------+                                   |
|                                                                             |
+-----------------------------------------------------------------------------+
              |
              V
+-----------------------------------------------------------------------------+
|  COMPLIANCE DASHBOARD                                                       |
|  +----------------+  +----------------+  +----------------+               |
|  |  NIST CSF      |  |  ISO 27001     |  |  PDF REPORTS   |               |
|  |  Mapping       |  |  Annex A       |  |  (Auto-gen)    |               |
|  +----------------+  +----------------+  +----------------+               |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 📊 Layer 1: Secure Development (Shift-Left)

```
+-----------------------------------------------------------------------------+
|  DEVELOPER WORKSTATION                                                      |
|                                                                             |
|  +---------------------+     +---------------------+                       |
|  |  VS CODE / TERMINAL |     |  .pre-commit-config |                       |
|  |                     |     |                     |                       |
|  |  code --> save      |---->|  HOOKS EXECUTE:     |                       |
|  |                     |     |                     |                       |
|  +---------------------+     |  [1] Gitleaks       |                       |
|                              |      Scan secrets   |                       |
|                              |                     |                       |
|                              |  [2] Semgrep        |                       |
|                              |      SAST Analysis  |                       |
|                              |                     |                       |
|                              |  [3] ESLint         |                       |
|                              |      Code Quality   |                       |
|                              |                     |                       |
|                              |  [4] File Hygiene   |                       |
|                              |      YAML/JSON/Size |                       |
|                              |                     |                       |
|                              +----------+----------+                       |
|                                         |                                   |
|                              +----------+----------+                       |
|                              |                     |                       |
|                              V                     V                       |
|                       +------------+        +------------+                 |
|                       |   PASS     |        |   BLOCK    |                 |
|                       |  Commit    |        |  Commit    |                 |
|                       |  Allowed   |        |  Rejected  |                 |
|                       +------------+        +------------+                 |
|                                                                             |
+-----------------------------------------------------------------------------+
```

**Security Value:** Vulnerabilities are caught **before** code enters the repository. No secrets, no insecure patterns, no bad commits.

---

## 📊 Layer 2: Jenkins CI/CD — 17-Stage Pipeline

```
+-----------------------------------------------------------------------------+
|                                                                             |
|   STAGE 1          CHECKOUT SOURCE                                          |
|   +---------------------------------------------------------------+        |
|   |  git clone https://github.com/9MayanK2/DevSecOps.git          |        |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 2          INSTALL PYTHON DEPENDENCIES                              |
|   +---------------------------------------------------------------+        |
|   |  pip install -r requirements.txt                                |        |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 3          GENERATE BACKEND .ENV                                    |
|   +---------------------------------------------------------------+        |
|   |  Inject MONGO_URL, JWT_SECRET, EMAIL_* from Jenkins Credentials |      |
|   |  NO HARDCODED SECRETS EVER                                      |        |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 4          PRE-COMMIT VALIDATION                                    |
|   +---------------------------------------------------------------+        |
|   |  [Gitleaks]  [ESLint-Frontend]  [ESLint-Backend]  [Semgrep]     |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 5          HADOLINT — DOCKERFILE LINTER                             |
|   +---------------------------------------------------------------+        |
|   |  Check: Multi-stage build, Non-root user, Minimal base image    |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 6          BUILD BACKEND IMAGE                                      |
|   +---------------------------------------------------------------+        |
|   |  FROM node:20-alpine -> npm ci --omit=dev -> USER appuser       |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 7          BUILD FRONTEND IMAGE                                     |
|   +---------------------------------------------------------------+        |
|   |  Stage 1: Build React  |  Stage 2: Nginx serve (non-root)       |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 8          TRIVY CONTAINER CVE SCAN                                 |
|   +---------------------------------------------------------------+        |
|   |  Backend Scan  +  Frontend Scan  ->  JSON Reports               |      |
|   |  CRITICAL CVEs = PIPELINE FAIL                                  |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 9          OWASP ZAP DAST SCAN                                      |
|   +---------------------------------------------------------------+        |
|   |  Spin up Docker Compose  ->  Attack running app  ->  Report    |      |
|   |  Detects: XSS | SQLi | CSRF | Insecure Headers                   |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 10         GENERATE SECURITY REPORTS                                |
|   +---------------------------------------------------------------+        |
|   |  Aggregate Trivy + ZAP + Gitleaks + Hadolint into master report |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 11         SECURITY GATE EVALUATION                                 |
|   +---------------------------------------------------------------+        |
|   |  Python Risk Scorer: CVSS-weighted composite score              |      |
|   |  IF score > threshold:  FAIL (exit 1)                           |      |
|   |  ELSE:  PASS (continue)                                         |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 12         COSIGN PKI DIGITAL SIGNING                               |
|   +---------------------------------------------------------------+        |
|   |  Sign backend image with private key  ->  .sig artifact         |      |
|   |  Sign frontend image with private key  ->  .sig artifact        |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 13         VERIFY DIGITAL SIGNATURES                                |
|   +---------------------------------------------------------------+        |
|   |  Verify both signatures before pushing to registry              |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 14         LOGIN TO AMAZON ECR                                      |
|   +---------------------------------------------------------------+        |
|   |  aws ecr get-login-password -> docker login                     |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 15         PUSH IMAGES TO ECR                                       |
|   +---------------------------------------------------------------+        |
|   |  Tag: build-42 + latest  ->  Push backend + frontend            |      |
|   |  Verify: aws ecr describe-images                                |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 16         DEPLOY TO AMAZON EKS                                     |
|   +---------------------------------------------------------------+        |
|   |  aws eks update-kubeconfig  ->  helm upgrade --install          |      |
|   +---------------------------+-----------------------------------+        |
|                               |                                             |
|                               V                                             |
|   STAGE 17         VERIFY KUBERNETES ROLLOUT                                |
|   +---------------------------------------------------------------+        |
|   |  kubectl rollout status deployment/backend --timeout=5m         |      |
|   |  kubectl rollout status deployment/frontend --timeout=5m        |      |
|   +---------------------------+-----------------------------------+        |
|                                                                             |
|   +---------------------+          +---------------------+                 |
|   |   SUCCESS           |          |   FAILURE           |                 |
|   |   Archive reports   |          |   bash rollback.sh  |                 |
|   |   Clean Docker      |          |   kubectl get pods  |                 |
|   |   Notify team       |          |   Alert on-call     |                 |
|   +---------------------+          +---------------------+                 |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 📊 Layer 3: Security Framework — 5-Stage Orchestrator

```
+=============================================================================+
|                     PYTHON SECURITY ORCHESTRATOR                            |
|                     security/core/orchestrator.py                           |
+=============================================================================+
|                                                                             |
|  +---------------------+                                                    |
|  |  STAGE 1            |                                                    |
|  |  PRE-FLIGHT CHECKS  |                                                    |
|  +---------------------+                                                    |
|  |  * Docker daemon?   |                                                    |
|  |  * Output dirs?     |                                                    |
|  |  * Policy file?     |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|             V                                                               |
|  +---------------------+                                                    |
|  |  STAGE 2            |                                                    |
|  |  RUN SCANNERS       |                                                    |
|  +---------------------+                                                    |
|  |  +---------------+  |                                                    |
|  |  | Gitleaks      |  |  Secrets in code                                   |
|  |  +---------------+  |                                                    |
|  |  +---------------+  |                                                    |
|  |  | Hadolint      |  |  Dockerfile best practices                         |
|  |  +---------------+  |                                                    |
|  |  +---------------+  |                                                    |
|  |  | Trivy         |  |  Container CVEs                                    |
|  |  +---------------+  |                                                    |
|  |  +---------------+  |                                                    |
|  |  | OWASP ZAP     |  |  Runtime vulnerabilities                           |
|  |  +---------------+  |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|             V                                                               |
|  +---------------------+                                                    |
|  |  STAGE 3            |                                                    |
|  |  RUN PARSERS        |                                                    |
|  +---------------------+                                                    |
|  |  Normalize all      |                                                    |
|  |  scanner outputs    |                                                    |
|  |  to common schema   |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|             V                                                               |
|  +---------------------+                                                    |
|  |  STAGE 4            |                                                    |
|  |  AGGREGATE RESULTS  |                                                    |
|  +---------------------+                                                    |
|  |  * Combine findings |                                                    |
|  |  * Map to OWASP     |                                                    |
|  |  * Map to CIS       |                                                    |
|  |  * Map to NIST CSF  |                                                    |
|  |  * Generate HTML    |                                                    |
|  |  * Generate PDF     |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|             V                                                               |
|  +---------------------+                                                    |
|  |  STAGE 5            |                                                    |
|  |  SECURITY GATE      |                                                    |
|  +---------------------+                                                    |
|  |  Risk Score: 42     |                                                    |
|  |  Threshold:  30     |                                                    |
|  |                     |                                                    |
|  |  42 > 30 = FAIL     |                                                    |
|  |  (soft-fail = warn) |                                                    |
|  +----------+----------+                                                    |
|             |                                                               |
|    +--------+--------+                                                      |
|    |                 |                                                      |
|    V                 V                                                      |
| +------+       +--------+                                                   |
| | PASS |       |  FAIL  |                                                   |
| |Exit 0|       | Exit 1 |                                                   |
| +------+       +--------+                                                   |
|                                                                             |
+=============================================================================+
```

---

## ☁️ Layer 4: AWS Architecture

```
+-----------------------------------------------------------------------------+
|                                                                             |
|                              🌐 INTERNET                                    |
|                                   |                                         |
+-----------------------------------|-----------------------------------------+
                                   |
                                   V
+-----------------------------------------------------------------------------+
|                    📍 ROUTE 53 + ACM (SSL/TLS)                              |
|                    sentinelops.example.com                                  |
|                    HTTPS Certificate (Auto-renew)                           |
+-----------------------------------|-----------------------------------------+
                                   |
                                   V
+-----------------------------------------------------------------------------+
|                    ⚖️ APPLICATION LOAD BALANCER (ALB)                       |
|                    * SSL Termination (443 -> 80)                            |
|                    * Path Routing: /api -> Backend, / -> Frontend           |
|                    * Health Checks (30s interval)                           |
|                    * Cross-AZ Load Balancing                                |
+-----------------------------------|-----------------------------------------+
                                   |
          +------------------------+------------------------+
          |                        |                        |
          V                        V                        V
+--------------------+  +--------------------+  +--------------------+
| 🛡️ AWS WAF v2      |  | 📡 PUBLIC SUBNET 1 |  | 📡 PUBLIC SUBNET 2 |
| SQLi/XSS Rules     |  | (us-east-1a)       |  | (us-east-1b)       |
| Rate Limiting      |  |                    |  |                    |
| Bot Control        |  | +----------------+ |  | +----------------+ |
|                    |  | | 🖥️ Jenkins EC2 | |  | | 🌐 NAT Gateway | |
|                    |  | | Ubuntu 22.04   | |  | | (HA Pair)      | |
|                    |  | | t3.large       | |  | +----------------+ |
|                    |  | | Port: 8080     | |  |                    |
|                    |  | +----------------+ |  | +----------------+ |
|                    |  | +----------------+ |  | | 🛡️ Bastion Host| |
|                    |  | | 🌐 NAT Gateway | |  | | (Jump Box)     | |
|                    |  | | (Outbound)     | |  | | Port: 22       | |
|                    |  | +----------------+ |  | +----------------+ |
+--------------------+  +--------------------+  +--------------------+
          |                        |                        |
          +------------------------+------------------------+
                                   |
                                   V
+-----------------------------------------------------------------------------+
|                         🏠 AWS VPC (10.0.0.0/16)                            |
|                                                                             |
|  +-----------------------------------------------------------------------+  |
|  |  🔒 PRIVATE SUBNET 1 (us-east-1a)                                      |  |
|  |                                                                        |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  |  | ☸️ EKS Worker  |  | ☸️ EKS Worker  |  | 📦 App Pods            |   |  |
|  |  |   Node 1       |  |   Node 2       |  |   Backend (x2)         |   |  |
|  |  |   t3.medium    |  |   t3.medium    |  |   Frontend (x2)        |   |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  |                                                                        |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  |  | 🔐 Secrets Mgr |  | 📊 CloudWatch  |  | 📦 ECR Pull            |   |  |
|  |  |   (CSI Driver) |  |   Agent        |  |   (Signed Images)      |   |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  +-----------------------------------------------------------------------+  |
|                                                                             |
|  +-----------------------------------------------------------------------+  |
|  |  🔒 PRIVATE SUBNET 2 (us-east-1b)                                      |  |
|  |                                                                        |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  |  | ☸️ EKS Worker  |  | ☸️ EKS Worker  |  | 🚀 ArgoCD Server       |   |  |
|  |  |   Node 3       |  |   Node 4       |  |   GitOps Controller    |   |  |
|  |  |   t3.medium    |  |   t3.medium    |  |   Port: 8080           |   |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  |                                                                        |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  |  | 📊 Prometheus  |  | 📊 Grafana     |  | 📝 ELK Stack           |   |  |
|  |  |   (Metrics)    |  |   (Dashboards) |  |   (Logs/Search)        |   |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  +-----------------------------------------------------------------------+  |
|                                                                             |
|  +-----------------------------------------------------------------------+  |
|  |  🔐 AWS MANAGED SERVICES                                               |  |
|  |                                                                        |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  |  | 📦 Amazon ECR  |  | 🔐 Secrets Mgr |  | 📊 CloudWatch          |   |  |
|  |  |   Registry     |  |   Credentials  |  |   Logs & Metrics       |   |  |
|  |  |   * backend    |  |   * MongoDB    |  |                        |   |  |
|  |  |   * frontend   |  |   * JWT        |  |                        |   |  |
|  |  +----------------+  +----------------+  +------------------------+   |  |
|  +-----------------------------------------------------------------------+  |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 🎯 ArgoCD GitOps Integration

### Current vs Future State

```
+-----------------------------------------------------------------------------+
|                                                                             |
|   CURRENT STATE: Jenkins deploys directly                                   |
|                                                                             |
|   Developer --> GitHub --> Jenkins --> Build/Scan/Sign --> ECR --> kubectl  |
|                                                                             |
|   PROBLEMS:                                                                 |
|   * No drift detection                                                      |
|   * Manual rollback only                                                    |
|   * No visual deployment topology                                           |
|   * Jenkins needs cluster access (security risk)                            |
|                                                                             |
+-----------------------------------+-----------------------------------------+
                                    |
                                    V
+-----------------------------------------------------------------------------+
|                                                                             |
|   FUTURE STATE: Jenkins builds, ArgoCD deploys                              |
|                                                                             |
|   Developer --> GitHub --> Jenkins --> Build/Scan/Sign --> ECR              |
|                                    |                                        |
|                                    |  (New signed image pushed)              |
|                                    V                                        |
|                             +----------------+                              |
|                             | ArgoCD Image   |                              |
|                             | Updater        |                              |
|                             | (Watches ECR)  |                              |
|                             +--------+-------+                              |
|                                      |                                      |
|                                      |  (Updates image tag in Git)           |
|                                      V                                      |
|                             +----------------+                              |
|                             | Git Repository |                              |
|                             | (Source of     |                              |
|                             |  Truth)        |                              |
|                             |                |                              |
|                             | helm/sentinelops/values.yaml                  |
|                             +--------+-------+                              |
|                                      |                                      |
|                                      |  (Auto-sync every 3 min)              |
|                                      V                                      |
|                             +----------------+                              |
|                             | ArgoCD App     |                              |
|                             | Controller     |                              |
|                             |                |                              |
|                             | * Self-healing |                              |
|                             | * Drift detect |                              |
|                             | * Rollback     |                              |
|                             +--------+-------+                              |
|                                      |                                      |
|                                      V                                      |
|                             +----------------+                              |
|                             | Amazon EKS     |                              |
|                             | (Target)       |                              |
|                             |                |                              |
|                             | Desired State  |                              |
|                             | = Actual State |                              |
|                             +----------------+                              |
|                                                                             |
+-----------------------------------------------------------------------------+
```

### ArgoCD Architecture

```
+-----------------------------------------------------------------------------+
|                                                                             |
|                    ARGOCD NAMESPACE (argocd)                                |
|                                                                             |
|  +----------------+  +----------------+  +----------------+               |
|  | 🎛️ ArgoCD      |  | 🔄 ArgoCD      |  | 🖥️ ArgoCD      |               |
|  |    Server      |  |    Application |  |    Image       |               |
|  |    (UI/API)    |  |    Controller  |  |    Updater     |               |
|  |    Port: 8080  |  |    (Sync Loop) |  |    (ECR Watch) |               |
|  +----------------+  +----------------+  +----------------+               |
|                                                                             |
|  +----------------+  +----------------+  +----------------+               |
|  | 🔐 ArgoCD      |  | 📊 ArgoCD      |  | 🔔 ArgoCD      |               |
|  |    Dex (SSO)   |  |    Metrics     |  |    Notifications|              |
|  |    (OIDC/LDAP) |  |    (Prometheus)|  |    (Slack/Email)|              |
|  +----------------+  +----------------+  +----------------+               |
|                                                                             |
|                              |                                              |
|              +---------------+---------------+                              |
|              |               |               |                              |
|              V               V               V                              |
|       +-----------+  +-----------+  +----------------+                     |
|       | Git Repo  |  | Amazon ECR|  | EKS Cluster    |                     |
|       | (Helm)    |  | (Images)  |  | (Deployments)  |                     |
|       +-----------+  +-----------+  +----------------+                     |
|                                                                             |
+-----------------------------------------------------------------------------+
```

### ArgoCD Implementation Steps

```
+-----------------------------------------------------------------------------+
|                                                                             |
|  STEP 1: Install ArgoCD                                                     |
|  +---------------------------------------------------------------------+   |
|  |  kubectl create namespace argocd                                    |   |
|  |  kubectl apply -n argocd -f https://raw.githubusercontent.com/...   |   |
|  +---------------------------------------------------------------------+   |
|                                    |                                        |
|                                    V                                        |
|  STEP 2: Expose ArgoCD Server                                               |
|  +---------------------------------------------------------------------+   |
|  |  kubectl port-forward svc/argocd-server -n argocd 8080:443        |   |
|  |  OR: kubectl apply -f argocd/ingress.yaml                           |   |
|  +---------------------------------------------------------------------+   |
|                                    |                                        |
|                                    V                                        |
|  STEP 3: Create Application Manifest                                        |
|  +---------------------------------------------------------------------+   |
|  |  kubectl apply -f argocd/applications/sentinelops-dev.yaml          |   |
|  +---------------------------------------------------------------------+   |
|                                    |                                        |
|                                    V                                        |
|  STEP 4: Install Image Updater                                              |
|  +---------------------------------------------------------------------+   |
|  |  kubectl apply -n argocd -f https://raw.githubusercontent.com/...   |   |
|  |  kubectl create secret docker-registry ecr-registry ...             |   |
|  +---------------------------------------------------------------------+   |
|                                    |                                        |
|                                    V                                        |
|  STEP 5: App of Apps Pattern                                                |
|  +---------------------------------------------------------------------+   |
|  |  kubectl apply -f argocd/app-of-apps/root-application.yaml          |   |
|  +---------------------------------------------------------------------+   |
|                                    |                                        |
|                                    V                                        |
|  STEP 6: Update Jenkins Pipeline                                            |
|  +---------------------------------------------------------------------+   |
|  |  stage('Trigger ArgoCD Sync') {                                     |   |
|  |      sh 'argocd login ... && argocd app sync sentinelops-dev'       |   |
|  |  }                                                                  |   |
|  +---------------------------------------------------------------------+   |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 📊 Layer 5: Monitoring & Observability

```
+-----------------------------------------------------------------------------+
|                                                                             |
|                         MONITORING & SIEM STACK                             |
|                                                                             |
|  +---------------------------+  +---------------------------+              |
|  |    📊 PROMETHEUS          |  |    📊 GRAFANA             |              |
|  |                           |  |                           |              |
|  |  Scraping Targets:        |  |  Dashboards:              |              |
|  |  * Node Exporter          |  |  * Cluster Health         |              |
|  |  * Kube State Metrics     |  |  * Pod Restarts           |              |
|  |  * App Endpoints          |  |  * Network Traffic        |              |
|  |  * ArgoCD Metrics         |  |  * Security Events        |              |
|  |                           |  |  * Resource Usage         |              |
|  |  Alerting Rules:          |  |                           |              |
|  |  * High CPU > 80%         |  |  Alert Channels:          |              |
|  |  * Pod CrashLoop          |  |  * PagerDuty              |              |
|  |  * Memory Pressure        |  |  * Email                  |              |
|  |  * Disk Full              |  |  * Slack                  |              |
|  +------------+--------------+  +------------+--------------+              |
|               |                              |                              |
|               +--------------+---------------+                              |
|                              |                                              |
|                              V                                              |
|  +---------------------------+  +---------------------------+              |
|  |    📝 ELK STACK           |  |    🛡️ WAZUH (HIDS)        |              |
|  |                           |  |                           |              |
|  |  Logstash -> Parse/Enrich |  |  * File Integrity Monitor |              |
|  |  Elasticsearch -> Index   |  |  * Rootkit Detection      |              |
|  |  Kibana -> Visualize      |  |  * Log Analysis           |              |
|  |                           |  |  * Compliance (PCI/HIPAA) |              |
|  |  Correlation Rules:       |  |                           |              |
|  |  * Brute Force + Escalate |  |  Alerts:                  |              |
|  |  * Unusual API Patterns   |  |  * File Modified          |              |
|  |  * Error Spike            |  |  * Privilege Escalation   |              |
|  +------------+--------------+  +------------+--------------+              |
|               |                              |                              |
|               +--------------+---------------+                              |
|                              |                                              |
|                              V                                              |
|  +---------------------------+                                              |
|  |    🌐 SNORT (NIDS)        |                                              |
|  |                           |                                              |
|  |  * Port Scan Detection    |                                              |
|  |  * Exploit Attempts       |                                              |
|  |  * C2 Traffic             |                                              |
|  |  * SQL Injection Patterns |                                              |
|  |                           |                                              |
|  |  Rules Updated Daily      |                                              |
|  +---------------------------+                                              |
|                                                                             |
|  DEFENSE IN DEPTH: If one layer misses an attack, another catches it.       |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 📋 Layer 6: Compliance & Reporting

```
+-----------------------------------------------------------------------------+
|                                                                             |
|                    COMPLIANCE DASHBOARD (Python Flask)                      |
|                                                                             |
|  +----------------+  +----------------+  +----------------+               |
|  |  NIST CSF      |  |  ISO 27001     |  |  OWASP TOP 10  |               |
|  |                |  |                |  |                |               |
|  |  Identify      |  |  A.12.6        |  |  A01: Broken   |               |
|  |  Protect       |  |  A.13.1        |  |       Access   |               |
|  |  Detect        |  |  A.16.1        |  |  A02: Crypto   |               |
|  |  Respond       |  |                |  |       Failures |               |
|  |  Recover       |  |                |  |  A03: Injection|               |
|  +----------------+  +----------------+  +----------------+               |
|                                                                             |
|  +----------------+  +----------------+  +----------------+               |
|  |  CIS Benchmarks|  |  Trend Analysis|  |  PDF Export    |               |
|  |                |  |                |  |                |               |
|  |  Docker        |  |  Vuln History  |  |  Executive     |               |
|  |  Kubernetes    |  |  Open/Resolved |  |  Reports       |               |
|  +----------------+  +----------------+  +----------------+               |
|                                                                             |
|  +----------------+  +----------------+  +----------------+               |
|  |  Remediation   |  |  Executive     |  |  Audit Trail   |               |
|  |  Tracker       |  |  Summary       |  |                |               |
|  |                |  |                |  |                |               |
|  |  * Issue ID    |  |  * Risk Score  |  |  * Who         |               |
|  |  * Owner       |  |  * Compliance %|  |  * What        |               |
|  |  * Due Date    |  |  * Trend Graph |  |  * When        |               |
|  |  * Status      |  |  * Action Items|  |  * Result      |               |
|  +----------------+  +----------------+  +----------------+               |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 💻 Application Stack

```
+-----------------------------------------------------------------------------+
|                                                                             |
|                         FULL-STACK APPLICATION                              |
|                                                                             |
|  +---------------------------+  +---------------------------+              |
|  |      FRONTEND             |  |      BACKEND              |              |
|  |      (React 19)           |  |      (Node.js 20)         |              |
|  |                           |  |                           |              |
|  |  React Router DOM 7.6     |  |  Express 5.1              |              |
|  |  Axios (HTTP Client)      |  |  JWT + bcrypt (Auth)      |              |
|  |  React Hot Toast          |  |  Joi (Validation)         |              |
|  |  React Icons              |  |  Mongoose 8.15 (MongoDB)  |              |
|  |  React Countdown          |  |  Nodemailer (Email)       |              |
|  |                           |  |  OpenAI API               |              |
|  |  Multi-stage Docker:      |  |  CSRF Protection          |              |
|  |  Node Build -> Nginx      |  |  CORS                     |              |
|  |  Non-root user            |  |  Cookie Parser            |              |
|  |  Health Check /health     |  |  Health Check /health     |              |
|  +------------+--------------+  +------------+--------------+              |
|               |                              |                              |
|               +--------------+---------------+                              |
|                              |                                              |
|                              V                                              |
|  +---------------------------+                                              |
|  |      DATABASE             |                                              |
|  |      (MongoDB)            |                                              |
|  |                           |                                              |
|  |  User Data                |                                              |
|  |  Application State        |                                              |
|  |  Session Management       |                                              |
|  +---------------------------+                                              |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 📁 Repository Structure

```
DevSecOps/
|
+-- app/
|   +-- client/                    # React Frontend
|   |   +-- Dockerfile             # Multi-stage: Node -> Nginx
|   |   +-- nginx/nginx.conf
|   |   +-- package.json           # React 19, Router, Axios
|   |   +-- src/                   # Components, Pages, Hooks
|   |
|   +-- server/                    # Node.js/Express Backend
|       +-- Dockerfile             # Node 20 Alpine, non-root
|       +-- package.json           # Express, JWT, Mongoose
|       +-- index.js               # Main entry
|       +-- .env                   # Generated at runtime
|
+-- security/                      # Enterprise Security Framework
|   +-- core/
|   |   +-- orchestrator.py        # 5-Stage Security Controller
|   |   +-- parser_registry.py     # Scanner output normalizers
|   |   +-- aggregator.py          # Multi-scanner aggregation
|   |   +-- security_gate.py       # Policy pass/fail evaluator
|   |   +-- compliance_mapper.py   # NIST/CIS/OWASP mapping
|   |   +-- report_generator.py    # HTML/PDF report generator
|   |
|   +-- container/
|   |   +-- trivy.sh               # CVE scanner wrapper
|   |   +-- hadolint.sh            # Dockerfile linter wrapper
|   |
|   +-- dast/
|   |   +-- zap.sh                 # OWASP ZAP DAST wrapper
|   |
|   +-- secrets/
|   |   +-- gitleaks.sh            # Secret scanning wrapper
|   |
|   +-- signing/
|   |   +-- sign_images.sh         # Cosign PKI signing
|   |   +-- verify_images.sh       # Signature verification
|   |   +-- generate_keys.sh       # One-time key generation
|   |
|   +-- parsers/                   # Scanner output normalizers
|   +-- db/                        # Database manager
|   +-- config/                    # Tool configs & PKI keys
|   +-- scripts/                   # Shared bash utilities
|
+-- terraform/                     # Infrastructure as Code
|   +-- main.tf                    # Root module composition
|   +-- variables.tf               # Input variables
|   +-- outputs.tf                 # Output values
|   +-- modules/
|       +-- network/               # VPC, subnets, SGs
|       +-- ec2/                   # Jenkins server
|       +-- ecr/                   # Container registries
|       +-- eks/                   # Kubernetes cluster
|
+-- k8s/                           # Raw Kubernetes Manifests
|   +-- namespace.yaml
|   +-- backend-deployment.yaml
|   +-- frontend-deployment.yaml
|   +-- service.yaml
|   +-- network-policy.yaml
|   +-- rbac.yaml
|
+-- helm/sentinelops/              # Helm Chart
|   +-- Chart.yaml
|   +-- values.yaml                # Configurable parameters
|   +-- templates/
|       +-- deployment.yaml
|       +-- service.yaml
|       +-- ingress.yaml
|       +-- secrets.yaml
|
+-- argocd/                        # ArgoCD GitOps Configuration
|   +-- applications/
|   |   +-- sentinelops-dev.yaml
|   |   +-- sentinelops-staging.yaml
|   |   +-- sentinelops-prod.yaml
|   +-- app-of-apps/
|   |   +-- root-application.yaml
|   +-- projects/
|   |   +-- sentinelops-project.yaml
|   +-- image-updater/
|       +-- configmap.yaml
|
+-- deployment/
|   +-- deploy.sh                  # EKS deployment script
|   +-- rollback.sh                # Automated rollback
|
+-- monitoring/
|   +-- prometheus/
|   |   +-- prometheus.yml         # Scraping config
|   +-- grafana/
|   |   +-- dashboards/
|   +-- elk/
|       +-- logstash.conf
|
+-- compliance/                    # Generated Artifacts
|   +-- reports/                   # Raw scanner outputs
|   +-- normalized/                # Normalized findings
|   +-- master_reports/            # Aggregated reports
|   +-- logs/                      # Execution logs
|
+-- docs/
|   +-- architecture.md
|   +-- DevSecOps_Project_Guide.md
|
+-- scripts/                       # Utility scripts
|
+-- Jenkinsfile                    # 17-Stage Declarative Pipeline
+-- docker-compose.yml             # Local dev environment
+-- requirements.txt               # Python dependencies
+-- .pre-commit-config.yaml        # Pre-commit hooks
+-- .gitignore
```

---

## 🚀 Quick Start

```
+-----------------------------------------------------------------------------+
|                                                                             |
|  LOCAL DEVELOPMENT                                                          |
|  +---------------------------------------------------------------------+   |
|  |  git clone https://github.com/9MayanK2/DevSecOps.git               |   |
|  |  cd DevSecOps                                                        |   |
|  |  pip install pre-commit && pre-commit install                        |   |
|  |  pip install -r requirements.txt                                     |   |
|  |  docker-compose up --build                                           |   |
|  +---------------------------------------------------------------------+   |
|                                                                             |
|  Access:  Frontend: http://localhost:3000                                  |
|           Backend:  http://localhost:5000                                  |
|                                                                             |
+-----------------------------------------------------------------------------+

+-----------------------------------------------------------------------------+
|                                                                             |
|  RUN SECURITY SCANS                                                         |
|  +---------------------------------------------------------------------+   |
|  |  ./security/run_pipeline.sh full          # Full pipeline            |   |
|  |  ./security/run_pipeline.sh pre-build     # SAST + Secrets           |   |
|  |  ./security/run_pipeline.sh gate --soft-fail  # Soft gate mode       |   |
|  +---------------------------------------------------------------------+   |
|                                                                             |
+-----------------------------------------------------------------------------+

+-----------------------------------------------------------------------------+
|                                                                             |
|  DEPLOY TO AWS EKS                                                          |
|  +---------------------------------------------------------------------+   |
|  |  cd terraform && terraform init && terraform apply                   |   |
|  |  aws eks update-kubeconfig --region us-east-1 --name sentinelops-dev |   |
|  |                                                                      |   |
|  |  # Option A: ArgoCD (GitOps)                                         |   |
|  |  kubectl create namespace argocd                                     |   |
|  |  kubectl apply -n argocd -f https://raw.githubusercontent.com/...    |   |
|  |  kubectl apply -f argocd/applications/sentinelops-dev.yaml           |   |
|  |                                                                      |   |
|  |  # Option B: Helm (Traditional)                                      |   |
|  |  helm upgrade --install sentinelops ./helm/sentinelops \             |   |
|  |    --namespace sentinelops --create-namespace \                      |   |
|  |    --set backend.image.tag=build-42 \                                |   |
|  |    --set frontend.image.tag=build-42                                 |   |
|  +---------------------------------------------------------------------+   |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 🛡️ Security Controls Mapping

```
+-----------------------------------------------------------------------------+
|                                                                             |
|  FRAMEWORK              |  HOW SENTINELOPS ADDRESSES IT                     |
|  ----------------------|--------------------------------------------------- |
|                                                                             |
|  OWASP Top 10          |  ZAP DAST + Semgrep SAST + secure coding          |
|  CIS Docker Benchmark  |  Hadolint + hardened multi-stage Dockerfiles      |
|  CIS K8s Benchmark     |  RBAC + NetworkPolicy + PodSecurityContext        |
|  NIST CSF              |  Identify | Protect | Detect | Respond | Recover   |
|  ISO 27001 Annex A     |  A.12.6 | A.13.1 | A.16.1                        |
|  PCI-DSS               |  Req 6 (secure dev) | Req 11 (vuln scanning)       |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 👥 Team & Credits

```
+-----------------------------------------------------------------------------+
|                                                                             |
|  BUILT BY A 3-PERSON TEAM FOR PGCP-ITISS PROGRAM                           |
|  CDAC ACTS, Pune | February 2026                                           |
|                                                                             |
|  +---------------------+  +---------------------+  +---------------------+ |
|  |  DevSecOps Lead     |  |  Security Engineer  |  |  Cloud & Monitoring | |
|  |                     |  |                     |  |                     | |
|  |  * Jenkins CI/CD    |  |  * Gitleaks/Semgrep |  |  * AWS EKS/IaC      | |
|  |  * Docker hardening |  |  * OWASP ZAP        |  |  * Prometheus/Grafana| |
|  |  * Trivy/Hadolint   |  |  * Python scoring   |  |  * ELK Stack        | |
|  |  * K8s/Helm/ArgoCD  |  |  * Wazuh/Snort      |  |  * Flask Dashboard  | |
|  |  * Cosign signing   |  |  * PKI/TLS certs    |  |  * MySQL/Reports    | |
|  +---------------------+  +---------------------+  +---------------------+ |
|                                                                             |
|  SHARED: Linux admin, Python scripting, Git workflow, weekly reviews       |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 🙏 Acknowledgments

- **CDAC ACTS, Pune** — Comprehensive DevSecOps curriculum and guidance
- **[Trivy](https://github.com/aquasecurity/trivy)** by Aqua Security
- **[OWASP ZAP](https://www.zaproxy.org/)** by OWASP
- **[Cosign](https://github.com/sigstore/cosign)** by Sigstore
- **[Wazuh](https://wazuh.com/)** by Wazuh Team
- **[Gitleaks](https://github.com/gitleaks/gitleaks)** by Zachary Rice
- **[Semgrep](https://semgrep.dev/)** by Semgrep, Inc.
- **[ArgoCD](https://argo-cd.readthedocs.io/)** by Argo Proj

---

<p align="center">
  <b>Built with ❤️ for the future of secure software delivery.</b><br>
  <a href="https://github.com/9MayanK2/DevSecOps">github.com/9MayanK2/DevSecOps</a>
</p>
