"""
compliance_mapper.py

Compliance Mapping Engine for DevSecOps Framework.
Maps findings (CWEs / Rules) to OWASP Top 10 (2021), CIS Benchmarks, and NIST SP 800-53.
Saves output inside compliance/reports/compliance/compliance_matrix.json.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Any

from security.common.logger import logger

COMPLIANCE_DIR = Path("compliance/reports/compliance")
COMPLIANCE_MATRIX_PATH = COMPLIANCE_DIR / "compliance_matrix.json"


class ComplianceMapper:
    """
    Maps normalized findings to OWASP Top 10 (2021), CIS Benchmarks, and NIST SP 800-53.
    """

    MAPPING_RULES = {
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
        }
    }

    def map_finding(self, finding: dict) -> dict:
        """
        Enriches a finding with compliance standard mappings.
        """
        rule_id = finding.get("rule_id", "")
        cwes = finding.get("cwe", []) or []
        category = finding.get("category", "")

        compliance_entries: List[dict] = []

        if rule_id in self.MAPPING_RULES:
            compliance_entries.append(self.MAPPING_RULES[rule_id])

        for cwe in cwes:
            if cwe in self.MAPPING_RULES and self.MAPPING_RULES[cwe] not in compliance_entries:
                compliance_entries.append(self.MAPPING_RULES[cwe])

        if not compliance_entries:
            if category == "Secrets Detection":
                compliance_entries.append({
                    "owasp": "A02:2021-Cryptographic Failures",
                    "cis": "CIS Controls v8 3.12 - Protect Sensitive Data",
                    "nist": "IA-5 Authenticator Management"
                })
            elif category == "Container Security":
                compliance_entries.append({
                    "owasp": "A06:2021-Vulnerable and Outdated Components" if finding.get("cve") else "A05:2021-Security Misconfiguration",
                    "cis": "CIS Docker Benchmark 4.0 - Container Hardening",
                    "nist": "CM-6 Configuration Settings"
                })

        finding["compliance"] = compliance_entries
        return finding

    def process_master_report(self, master_report: dict) -> dict:
        """
        Enriches master report findings and builds a compliance matrix summary inside compliance/reports/compliance/.
        """
        logger.info("Processing Compliance Layer mappings into compliance/reports/compliance/...")

        owasp_breakdown: Dict[str, int] = {}
        cis_breakdown: Dict[str, int] = {}
        nist_breakdown: Dict[str, int] = {}

        enriched_findings = []
        for finding in master_report.get("findings", []):
            enriched = self.map_finding(finding)
            enriched_findings.append(enriched)

            for comp in enriched.get("compliance", []):
                owasp = comp.get("owasp")
                cis = comp.get("cis")
                nist = comp.get("nist")

                if owasp:
                    owasp_breakdown[owasp] = owasp_breakdown.get(owasp, 0) + 1
                if cis:
                    cis_breakdown[cis] = cis_breakdown.get(cis, 0) + 1
                if nist:
                    nist_breakdown[nist] = nist_breakdown.get(nist, 0) + 1

        master_report["findings"] = enriched_findings

        # Build Compliance Summary Matrix
        compliance_matrix = {
            "title": "DevSecOps Enterprise Compliance Matrix",
            "generated_at": master_report.get("generated_at"),
            "total_findings": len(enriched_findings),
            "frameworks": {
                "owasp_top_10_2021": owasp_breakdown,
                "cis_benchmarks": cis_breakdown,
                "nist_sp_800_53": nist_breakdown
            }
        }

        # Save inside compliance/reports/compliance/
        COMPLIANCE_DIR.mkdir(parents=True, exist_ok=True)
        with open(COMPLIANCE_MATRIX_PATH, "w", encoding="utf-8") as fp:
            json.dump(compliance_matrix, fp, indent=4)

        logger.info(f"Saved compliance matrix to {COMPLIANCE_MATRIX_PATH}")
        return master_report


def main():
    mapper = ComplianceMapper()
    print("Compliance Mapper initialized.")


if __name__ == "__main__":
    main()
