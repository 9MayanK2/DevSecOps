"""
gitleaks_parser.py

Enterprise Gitleaks Parser

Converts Gitleaks secret scan JSON reports into normalized Finding objects enriched with CWE classifications.
"""

from __future__ import annotations

from datetime import datetime

from security.core.base_parser import BaseParser
from security.core.parser_registry import registry
from security.schemas.finding import Finding
from security.common.logger import logger
from security.common.recommendation import get_recommendation
from security.common.severity import normalize_severity
from security.common.status import STATUS_OPEN
from security.common.categories import CATEGORY_SECRETS
from security.common.scanner_type import SCANNER_STATIC
from security.common.validator import validate_gitleaks_report
from security.config.config_loader import get


TOOL_NAME = "Gitleaks"
REPORT_DIR = get("GITLEAKS", "report_dir")
OUTPUT_DIR = get("GITLEAKS", "output_dir")

GITLEAKS_CWE_MAP = {
    "aws-access-token": ["CWE-798"],
    "aws-secret-access-key": ["CWE-798"],
    "generic-api-key": ["CWE-798"],
    "github-pat": ["CWE-798"],
    "private-key": ["CWE-798", "CWE-311"],
    "rsa-private-key": ["CWE-798", "CWE-311"],
    "ssh-private-key": ["CWE-798", "CWE-311"],
    "pgp-private-key": ["CWE-798", "CWE-311"],
    "slack-web-hook": ["CWE-798"],
    "stripe-api-key": ["CWE-798"],
    "jwt": ["CWE-798", "CWE-347"],
    "jwt-token": ["CWE-798", "CWE-347"]
}


def determine_gitleaks_severity(rule_id: str) -> str:
    rule_id_lower = rule_id.lower()
    critical_rules = {
        "aws-access-token",
        "aws-secret-access-key",
        "private-key",
        "rsa-private-key",
        "ssh-private-key",
        "pgp-private-key",
    }

    if any(crit in rule_id_lower for crit in critical_rules):
        return "CRITICAL"
    return "HIGH"


def determine_gitleaks_cwes(rule_id: str) -> list[str]:
    rule_id_lower = rule_id.lower()
    if rule_id_lower in GITLEAKS_CWE_MAP:
        return GITLEAKS_CWE_MAP[rule_id_lower]

    if "private-key" in rule_id_lower or "rsa" in rule_id_lower or "ssh" in rule_id_lower:
        return ["CWE-312", "CWE-798"]
    elif "jwt" in rule_id_lower or "token" in rule_id_lower:
        return ["CWE-522", "CWE-798"]
    return ["CWE-798"]


class GitleaksParser(BaseParser):
    def __init__(self):
        super().__init__(
            tool_name=TOOL_NAME,
            category=CATEGORY_SECRETS,
            scanner_type=SCANNER_STATIC,
            input_directory=REPORT_DIR,
            output_directory=OUTPUT_DIR
        )

    def validate(self) -> None:
        logger.info(f"[{self.tool_name}] Validating report...")
        validate_gitleaks_report(self.raw_report)

    def build_rule(self, item: dict) -> dict:
        rule_id = item.get("RuleID", "")
        rule = get_recommendation(TOOL_NAME, rule_id)
        if rule is not None and isinstance(rule, dict) and "recommendation" in rule:
            return rule

        return {
            "title": rule_id or "Secret Detected",
            "description": item.get("Description", "Potential secret exposed."),
            "recommendation": "Remove hardcoded secret and rotate credentials immediately.",
            "references": [
                "https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password"
            ]
        }

    def extract_findings(self) -> list[Finding]:
        findings = []

        if not self.raw_report:
            logger.warning("Gitleaks report is empty.")
            return findings

        for item in self.raw_report:
            raw_file = item.get("File", "")
            file_path = raw_file[11:] if raw_file.startswith("/workspace/") else raw_file

            if file_path.startswith("compliance/"):
                continue

            rule_id = item.get("RuleID", "generic-secret")
            severity = determine_gitleaks_severity(rule_id)
            cwes = determine_gitleaks_cwes(rule_id)
            rule = self.build_rule(item)
            secret = item.get("Secret", "")

            masked_secret = (
                secret[:3] + "..." + secret[-3:]
                if len(secret) > 6
                else "***"
            )

            message = f"{item.get('Description', 'Secret detected.')} (Match: {masked_secret})"
            scan_time_val = self.scan_time or datetime.utcnow().isoformat()

            finding = Finding(
                tool=TOOL_NAME,
                category=CATEGORY_SECRETS,
                rule_id=rule_id,
                severity=severity,
                file=file_path,
                line=item.get("StartLine"),
                message=message,
                recommendation=rule.get("recommendation"),
                status=STATUS_OPEN,
                scan_time=scan_time_val,
                package_name=None,
                installed_version=None,
                fixed_version=None,
                cvss_score=None,
                cwe=cwes,
                cve=None,
                severity_source=TOOL_NAME,
                target=file_path,
                target_class="Secret",
                target_type="Code/Config",
                description=rule.get("description") or item.get("Description"),
                primary_url=(
                    rule.get("references")[0]
                    if rule.get("references")
                    else None
                ),
                references=rule.get("references", []),
                compliance=[],
                exploit_available=False,
                fix_available=False,
                epss_score=None,
                kev=False
            )

            findings.append(finding)

        logger.info(f"Parsed {len(findings)} Gitleaks findings enriched with CWEs.")
        return findings

    def before_parse(self):
        logger.info(f"[{TOOL_NAME}] Preparing parser...")

    def after_parse(self):
        logger.info(f"[{TOOL_NAME}] Parser completed successfully.")


registry.register("gitleaks", GitleaksParser)


def main():
    parser = GitleaksParser()
    parser.run()


if __name__ == "__main__":
    main()
