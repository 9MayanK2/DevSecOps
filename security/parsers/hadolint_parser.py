"""
hadolint_parser.py

Enterprise Hadolint Parser

Converts Hadolint JSON reports into normalized Finding objects enriched with CWE classifications.
"""

from __future__ import annotations

from security.core.base_parser import BaseParser
from security.core.parser_registry import registry
from security.schemas.finding import Finding
from security.common.logger import logger
from security.common.recommendation import get_recommendation
from security.common.severity import normalize_severity
from security.common.status import STATUS_OPEN
from security.common.categories import CATEGORY_CONTAINER
from security.common.scanner_type import SCANNER_STATIC
from security.common.validator import validate_hadolint_report
from security.config.config_loader import get


TOOL_NAME = "Hadolint"
REPORT_DIR = get("HADOLINT", "report_dir")
OUTPUT_DIR = get("HADOLINT", "output_dir")

HADOLINT_CWE_MAP = {
    "DL3000": ["CWE-706"],
    "DL3001": ["CWE-252"],
    "DL3002": ["CWE-269"],
    "DL3003": ["CWE-706"],
    "DL3004": ["CWE-269"],
    "DL3005": ["CWE-16"],
    "DL3006": ["CWE-1188"],
    "DL3007": ["CWE-1188"],
    "DL3008": ["CWE-1104"],
    "DL3009": ["CWE-459"],
    "DL3013": ["CWE-1104"],
    "DL3014": ["CWE-16"],
    "DL3015": ["CWE-16"],
    "DL3016": ["CWE-1104"],
    "DL3018": ["CWE-1104"],
    "DL3019": ["CWE-16"],
    "DL3020": ["CWE-732"],
    "DL3025": ["CWE-20"],
    "DL3045": ["CWE-706"],
    "DL3059": ["CWE-1059"]
}


def determine_hadolint_cwes(code: str) -> list[str]:
    """
    Maps Hadolint Dockerfile rule codes to precise MITRE CWEs.
    """
    code_upper = code.upper()
    if code_upper in HADOLINT_CWE_MAP:
        return HADOLINT_CWE_MAP[code_upper]
    return ["CWE-16"]


class HadolintParser(BaseParser):
    def __init__(self):
        super().__init__(
            tool_name=TOOL_NAME,
            category=CATEGORY_CONTAINER,
            scanner_type=SCANNER_STATIC,
            input_directory=REPORT_DIR,
            output_directory=OUTPUT_DIR
        )

    def validate(self) -> None:
        logger.info(f"[{self.tool_name}] Validating report...")
        validate_hadolint_report(self.raw_report)

    def build_rule(self, item: dict) -> dict:
        rule = get_recommendation(TOOL_NAME, item.get("code", ""))
        if rule is not None:
            return rule

        return {
            "title": item.get("code", "Unknown Rule"),
            "description": item.get("message", ""),
            "recommendation": "No recommendation available.",
            "reference": None
        }

    def extract_findings(self) -> list[Finding]:
        findings = []

        if not self.raw_report:
            logger.warning("Hadolint report is empty.")
            return findings

        for item in self.raw_report:
            severity = normalize_severity(item.get("level", "UNKNOWN"))
            rule_code = item.get("code", "")
            rule = self.build_rule(item)
            cwes = determine_hadolint_cwes(rule_code)

            finding = Finding(
                tool=TOOL_NAME,
                category=CATEGORY_CONTAINER,
                rule_id=rule_code,
                severity=severity,
                file=item.get("file"),
                line=item.get("line"),
                message=item.get("message"),
                recommendation=rule.get("recommendation"),
                status=STATUS_OPEN,
                scan_time=self.scan_time,
                package_name=None,
                installed_version=None,
                fixed_version=None,
                cvss_score=None,
                cwe=cwes,
                cve=None,
                severity_source=TOOL_NAME,
                target=item.get("file"),
                target_class="Dockerfile",
                target_type="Container",
                description=rule.get("description"),
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

        logger.info(f"Parsed {len(findings)} Hadolint findings enriched with CWEs.")
        return findings

    def before_parse(self):
        logger.info(f"[{TOOL_NAME}] Preparing parser...")

    def after_parse(self):
        logger.info(f"[{TOOL_NAME}] Parser completed successfully.")


registry.register("hadolint", HadolintParser)


def main():
    parser = HadolintParser()
    parser.run()


if __name__ == "__main__":
    main()
