"""
compliance_mapper.py

Universal 4-Layer Compliance Mapping Engine for DevSecOps Framework.
Maps findings (CWEs / Rules / CVEs / Categories) to OWASP Top 10 (2021), CIS Benchmarks, and NIST SP 800-53 Rev. 5.

4-Layer Lookup Architecture:
  - Layer 1: Specific Rule-ID / Direct Rule Signature Match
  - Layer 2: Direct CWE Lookup via Auto-Generated Open Standards CWE Database
  - Layer 3: NVD API 2.0 Threat Intelligence Enrichment (Dynamic CVE -> CWE Resolution)
  - Layer 4: Universal Category & Heuristic Standard Fallback

Outputs report to compliance/reports/compliance/compliance_matrix.json.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from security.common.logger import logger
from security.core.nvd_enrichment import NVDEnricher

COMPLIANCE_DIR = Path("compliance/reports/compliance")
COMPLIANCE_MATRIX_PATH = COMPLIANCE_DIR / "compliance_matrix.json"
CWE_DB_PATH = Path("security/knowledge/cwe_database.json")


class ComplianceMapper:
    """
    Universal 4-Layer Compliance Engine providing framework breakdown, compliance %, and control metrics.
    """

    # Layer 1: Rule-ID & Tool Specific Signature Mappings
    RULE_MAPPINGS = {
        "CWE-798": {
            "owasp": "A02:2021-Cryptographic Failures",
            "cis": "CIS Controls v8 3.12 - Rekey or Revoke Credentials",
            "nist": "IA-5 Authenticator Management"
        },
        "aws-access-token": {
            "owasp": "A02:2021-Cryptographic Failures",
            "cis": "CIS Controls v8 3.12 - Protect Sensitive Cloud Credentials",
            "nist": "IA-5 Authenticator Management"
        },
        "generic-api-key": {
            "owasp": "A02:2021-Cryptographic Failures",
            "cis": "CIS Controls v8 3.12 - Avoid Hardcoded API Keys",
            "nist": "IA-5 Authenticator Management"
        },
        "DL3059": {
            "owasp": "A05:2021-Security Misconfiguration",
            "cis": "CIS Docker Benchmark 4.6 - Healthcheck Instruction",
            "nist": "CM-6 Configuration Settings"
        },
        "DL3002": {
            "owasp": "A05:2021-Security Misconfiguration",
            "cis": "CIS Docker Benchmark 4.1 - Non-root Container User",
            "nist": "AC-6 Least Privilege"
        },
        "DL3006": {
            "owasp": "A05:2021-Security Misconfiguration",
            "cis": "CIS Docker Benchmark 4.2 - Base Image Tagging",
            "nist": "CM-6 Configuration Settings"
        },
        "DL3018": {
            "owasp": "A06:2021-Vulnerable and Outdated Components",
            "cis": "CIS Docker Benchmark 4.3 - Pin Package Versions",
            "nist": "SI-2 Flaw Remediation"
        }
    }

    # Baseline controls count per framework
    FRAMEWORK_BASELINES = {
        "owasp_top_10_2021": 10,
        "cis_benchmarks": 15,
        "nist_sp_800_53": 20
    }

    def __init__(self, cwe_db_path: Path = CWE_DB_PATH):
        self.cwe_db_path = Path(cwe_db_path)
        self.cwe_db = self._load_cwe_db()
        self.nvd_enricher = NVDEnricher()

    def _load_cwe_db(self) -> Dict[str, dict]:
        if not self.cwe_db_path.exists():
            # If not present, attempt dynamic generation
            try:
                from security.knowledge.generate_cwe_db import generate_database
                generate_database()
            except Exception as ex:
                logger.warning(f"Could not auto-generate CWE database: {ex}")
                return {}

        try:
            with open(self.cwe_db_path, "r", encoding="utf-8") as fp:
                return json.load(fp)
        except Exception as ex:
            logger.warning(f"Could not load CWE database at {self.cwe_db_path}: {ex}")
            return {}

    def map_finding(self, finding: dict) -> dict:
        """
        Enriches a finding using the 4-Layer Universal Lookup System.
        """
        rule_id = finding.get("rule_id", "")
        cwes = finding.get("cwe", []) or []
        cve = finding.get("cve", "")
        category = finding.get("category", "")
        tool = finding.get("tool", "")

        compliance_entries: List[dict] = []
        matched_layers: List[str] = []

        # -------------------------------------------------------------
        # LAYER 1: Rule-ID & Tool Specific Signature Direct Match
        # -------------------------------------------------------------
        if rule_id in self.RULE_MAPPINGS:
            compliance_entries.append(self.RULE_MAPPINGS[rule_id])
            matched_layers.append("Layer 1 (Rule-ID Direct Match)")

        # -------------------------------------------------------------
        # LAYER 2: Direct CWE Lookup via Auto-Generated Open Standards DB
        # -------------------------------------------------------------
        for cwe in cwes:
            cwe_norm = cwe.upper().strip()
            if not cwe_norm.startswith("CWE-"):
                cwe_norm = f"CWE-{cwe_norm}"

            if cwe_norm in self.RULE_MAPPINGS and self.RULE_MAPPINGS[cwe_norm] not in compliance_entries:
                compliance_entries.append(self.RULE_MAPPINGS[cwe_norm])
                matched_layers.append(f"Layer 1/2 ({cwe_norm} Rule Match)")

            if cwe_norm in self.cwe_db:
                db_entry = self.cwe_db[cwe_norm]
                mapping = {
                    "owasp": db_entry.get("owasp"),
                    "cis": db_entry.get("cis"),
                    "nist": db_entry.get("nist")
                }
                if mapping not in compliance_entries:
                    compliance_entries.append(mapping)
                    matched_layers.append(f"Layer 2 ({cwe_norm} Open Standard DB Match)")

        # -------------------------------------------------------------
        # LAYER 3: NVD API Threat Intelligence Enrichment for Missing CWEs / CVEs
        # -------------------------------------------------------------
        if not compliance_entries and cve:
            enriched_cwes = self.nvd_enricher.fetch_cwes_for_cve(cve)
            for e_cwe in enriched_cwes:
                if e_cwe in self.cwe_db:
                    db_entry = self.cwe_db[e_cwe]
                    mapping = {
                        "owasp": db_entry.get("owasp"),
                        "cis": db_entry.get("cis"),
                        "nist": db_entry.get("nist")
                    }
                    if mapping not in compliance_entries:
                        compliance_entries.append(mapping)
                        matched_layers.append(f"Layer 3 (NVD API {cve} -> {e_cwe} Enrichment)")

        # -------------------------------------------------------------
        # LAYER 4: Universal Category & Heuristic Fallback Standard Mapping
        # -------------------------------------------------------------
        if not compliance_entries:
            if category == "Secrets Detection" or "gitleaks" in tool.lower():
                compliance_entries.append({
                    "owasp": "A02:2021-Cryptographic Failures",
                    "cis": "CIS Controls v8 3.12 - Protect Sensitive Data",
                    "nist": "IA-5 Authenticator Management"
                })
                matched_layers.append("Layer 4 (Secrets Detection Heuristic Fallback)")

            elif category == "Container Security" or "hadolint" in tool.lower() or "trivy" in tool.lower():
                compliance_entries.append({
                    "owasp": "A06:2021-Vulnerable and Outdated Components" if cve else "A05:2021-Security Misconfiguration",
                    "cis": "CIS Docker Benchmark 4.0 - Container Hardening",
                    "nist": "CM-6 Configuration Settings" if not cve else "SI-2 Flaw Remediation"
                })
                matched_layers.append("Layer 4 (Container Security Heuristic Fallback)")

            elif category == "DAST" or "zap" in tool.lower():
                compliance_entries.append({
                    "owasp": "A03:2021-Injection",
                    "cis": "CIS Controls v8 16.1 - Application Software Security",
                    "nist": "SI-10 Information Input Validation"
                })
                matched_layers.append("Layer 4 (DAST Heuristic Fallback)")

            else:
                compliance_entries.append({
                    "owasp": "A05:2021-Security Misconfiguration",
                    "cis": "CIS Controls v8 4.1 - Secure Configuration",
                    "nist": "CM-6 Configuration Settings"
                })
                matched_layers.append("Layer 4 (General Universal Security Fallback)")

        finding["compliance"] = compliance_entries
        finding["compliance_layers"] = matched_layers
        return finding

    def process_master_report(self, master_report: dict) -> dict:
        """
        Enriches master report findings and calculates decoupled control compliance metrics.
        """
        logger.info("Processing 4-Layer Universal Compliance Engine mappings...")

        owasp_controls: Dict[str, int] = {}
        cis_controls: Dict[str, int] = {}
        nist_controls: Dict[str, int] = {}

        enriched_findings = []
        for finding in master_report.get("findings", []):
            enriched = self.map_finding(finding)
            enriched_findings.append(enriched)

            for comp in enriched.get("compliance", []):
                owasp = comp.get("owasp")
                cis = comp.get("cis")
                nist = comp.get("nist")

                if owasp:
                    owasp_controls[owasp] = owasp_controls.get(owasp, 0) + 1
                if cis:
                    cis_controls[cis] = cis_controls.get(cis, 0) + 1
                if nist:
                    nist_controls[nist] = nist_controls.get(nist, 0) + 1

        master_report["findings"] = enriched_findings

        # Compute Framework Summaries & Percentages
        framework_summary: Dict[str, dict] = {}

        for fw_name, total_baseline in self.FRAMEWORK_BASELINES.items():
            if fw_name == "owasp_top_10_2021":
                failed_dict = owasp_controls
            elif fw_name == "cis_benchmarks":
                failed_dict = cis_controls
            else:
                failed_dict = nist_controls

            controls_failed = len(failed_dict)
            controls_passed = max(0, total_baseline - controls_failed)
            compliance_pct = round((controls_passed / total_baseline) * 100.0, 1)

            framework_summary[fw_name] = {
                "total_controls_baseline": total_baseline,
                "controls_passed": controls_passed,
                "controls_failed": controls_failed,
                "compliance_percentage": compliance_pct,
                "failed_controls_breakdown": failed_dict
            }

        # Calculate overall framework compliance average score
        total_pct = sum(fdata["compliance_percentage"] for fdata in framework_summary.values())
        overall_compliance_score = round(total_pct / len(framework_summary), 1) if framework_summary else 100.0

        compliance_matrix = {
            "title": "DevSecOps Enterprise Universal Compliance Matrix",
            "generated_at": master_report.get("generated_at"),
            "overall_compliance_score": overall_compliance_score,
            "total_findings": len(enriched_findings),
            "framework_summaries": framework_summary
        }

        # Save to compliance/reports/compliance/compliance_matrix.json
        COMPLIANCE_DIR.mkdir(parents=True, exist_ok=True)
        with open(COMPLIANCE_MATRIX_PATH, "w", encoding="utf-8") as fp:
            json.dump(compliance_matrix, fp, indent=4)

        master_report["compliance_summary"] = framework_summary
        if "summary" in master_report:
            master_report["summary"]["compliance_score"] = overall_compliance_score

        # Also update master_report.json on disk
        master_report_path = Path("compliance/master_reports/master_report.json")
        try:
            with open(master_report_path, "w", encoding="utf-8") as fp:
                json.dump(master_report, fp, indent=4)
        except Exception as ex:
            logger.warning(f"Could not update master_report.json on disk: {ex}")

        logger.info(f"Saved 4-Layer Universal Compliance Matrix with Score: {overall_compliance_score}% to {COMPLIANCE_MATRIX_PATH}")
        return master_report


def main():
    mapper = ComplianceMapper()
    print("4-Layer Universal Compliance Mapper initialized successfully.")


if __name__ == "__main__":
    main()
