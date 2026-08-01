"""
zap_parser.py

Parser for OWASP ZAP DAST scan results.
Extends BaseParser and registers into ParserRegistry.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any

from security.core.base_parser import BaseParser
from security.core.parser_registry import registry
from security.schemas.finding import Finding


class ZapParser(BaseParser):
    def __init__(
        self,
        tool_name: str = "zap",
        category: str = "DAST Web Vulnerability",
        scanner_type: str = "Dynamic",
        input_directory: str = "compliance/reports/zap",
        output_directory: str = "compliance/normalized/zap"
    ):
        super().__init__(
            tool_name=tool_name,
            category=category,
            scanner_type=scanner_type,
            input_directory=input_directory,
            output_directory=output_directory
        )


    def extract_findings(self) -> List[Finding]:
        findings: List[Finding] = []
        raw_data = self.raw_report or {}

        site_alerts: List[dict] = []
        if isinstance(raw_data, dict):
            site_list = raw_data.get("site", [])
            for site in site_list:
                alerts = site.get("alerts", [])
                site_alerts.extend(alerts)

        severity_map = {
            "3": "HIGH",
            "2": "MEDIUM",
            "1": "LOW",
            "0": "INFO"
        }


        for alert in site_alerts:
            risk_code = str(alert.get("riskcode", "0"))
            severity = severity_map.get(risk_code, "INFO")
            plugin_id = str(alert.get("pluginid", "ZAP-ALERT"))
            cwe_id = f"CWE-{alert.get('cweid')}" if alert.get("cweid") else "CWE-693"
            rule_id = f"ZAP-{plugin_id}"

            alert_name = alert.get("name", "Web Endpoint Alert")
            desc = alert.get("desc", alert_name)

            scan_time_val = self.scan_time or datetime.utcnow().isoformat()

            finding = Finding(
                tool="OWASP ZAP",
                category="DAST Web Vulnerability",
                rule_id=rule_id,
                severity=severity,
                file=alert_name,
                line=None,
                message=f"{alert_name} - {desc[:120]}",
                recommendation=alert.get("solution", "Enforce secure web headers and sanitize input parameters."),
                status="OPEN",
                scan_time=scan_time_val,
                cwe=[cwe_id],
                description=desc,
                primary_url=alert.get("reference", "").split("\n")[0] if alert.get("reference") else "https://www.zaproxy.org/"
            )
            findings.append(finding)


        return findings


# Register in ParserRegistry
registry.register("zap", ZapParser())


def main():
    parser = ZapParser()
    parser.run()
    print(f"OWASP ZAP parser processed findings successfully.")


if __name__ == "__main__":
    main()

