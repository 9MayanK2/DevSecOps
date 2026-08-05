# SentinelOps - Technical Documentation & Developer Guides (`docs/`)

The `docs/` outer directory contains architectural specifications, syllabus mappings, step-by-step implementation roadmaps, pre-commit configuration breakdowns, and container security standards for SentinelOps.

---

## 📁 Outer Directory Structure & Subfolder Breakdown

```text
docs/
├── architecture.md                 # High-level architecture notes & webhook integration specs
├── DevSecOps_Project_Guide.md     # Comprehensive 400+ line master project guide & syllabus mapping
└── Phase_1_Docs/                   # Phase 1 Developer Setup & Tooling Tutorials
    ├── docker.md                   # Multi-stage Docker build guidelines & Hadolint linting rules
    └── pre-commit.md               # Line-by-line breakdown of .pre-commit-config.yaml & hooks
```

---

## 🔄 Technical Documentation Flowchart

```mermaid
flowchart TD
    DOCS[SentinelOps Technical Documentation docs/] --> MAIN[DevSecOps Master Project Guide]
    DOCS --> PHASE1[Phase 1 Implementation Guides docs/Phase_1_Docs/]
    DOCS --> ARCH[Architecture & Webhook Notes docs/architecture.md]

    MAIN --> M1[6-Layer DevSecOps Security Framework]
    MAIN --> M2[12-Week Phase Roadmap & Deliverables]
    MAIN --> M3[Interview Q&A & Academic Syllabus Alignment]

    PHASE1 --> P1[docs/Phase_1_Docs/pre-commit.md]
    PHASE1 --> P2[docs/Phase_1_Docs/docker.md]

    P1 --> P1_1[Gitleaks Hooks vs Local Hooks]
    P1 --> P1_2[Version Locking & CLI Flags]
    P2 --> P2_1[Multi-Stage Docker Builds]
    P2 --> P2_2[Hadolint Enforcement Rules DL3006/DL3002]
```

---

## 💻 Subfolder Details (`docs/Phase_1_Docs/`)

1. **`pre-commit.md`**: Explains pre-commit hooks line by line. Teaches developers how external git repositories (Gitleaks) differ from local script hooks (njsscan/Bandit), version locking with `rev:`, and pass-filename CLI options.
2. **`docker.md`**: Standardizes container image creation across the team. Defines rules for multi-stage Docker builds, non-root user creation (`appuser`), and Hadolint linter compliance.
