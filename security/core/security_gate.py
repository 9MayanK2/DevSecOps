"""
security_gate.py

Enterprise Security Gate Evaluator

Evaluates master aggregated findings against policy thresholds.
Displays terminal executive summary and returns PASS/FAIL verdict.
"""

from __future__ import annotations

from typing import List, Dict, Any
from security.common.logger import logger


class SecurityGate:
    """
    Evaluates master report metrics against security policy rules.
    """

    def __init__(self, master_report: dict):
        self.report = master_report
        self.summary = master_report.get("summary", {})

    def evaluate(
        self,
        fail_on_critical: bool = True,
        fail_on_high: bool = False,
        min_score: float = 70.0
    ) -> bool:
        """
        Evaluates findings against policy thresholds and prints summary table.
        """
        logger.info("Evaluating Security Gate policy...")

        total_findings = self.summary.get("total_findings", 0)
        critical_count = self.summary.get("critical", 0)
        high_count = self.summary.get("high", 0)
        medium_count = self.summary.get("medium", 0)
        low_count = self.summary.get("low", 0)
        info_count = self.summary.get("info", 0)
        score = self.summary.get("compliance_score", 100.0)

        reasons: List[str] = []

        if fail_on_critical and critical_count > 0:
            reasons.append(f"Found {critical_count} CRITICAL findings (Policy: 0 allowed).")

        if fail_on_high and high_count > 0:
            reasons.append(f"Found {high_count} HIGH findings (Policy: 0 allowed).")

        if score < min_score:
            reasons.append(f"Compliance score {score:.1f}% is below minimum {min_score}%.")

        passed = len(reasons) == 0

        scanners = ", ".join(self.report.get("scanners_executed", [])) or "None"

        print("\n" + "=" * 65)
        print("             DEVSECOPS SECURITY GATE SUMMARY")
        print("=" * 65)
        print(f" Scanners Executed : {scanners}")
        print(f" Total Findings    : {total_findings}")
        print(f"   - CRITICAL      : {critical_count}")
        print(f"   - HIGH          : {high_count}")
        print(f"   - MEDIUM        : {medium_count}")
        print(f"   - LOW           : {low_count}")
        print(f"   - INFO          : {info_count}")
        print(f" Compliance Score  : {score:.1f}%")
        print("=" * 65)

        if passed:
            print(" VERDICT           : [ PASS ] Security Gate Passed Successfully!")
            print("=" * 65 + "\n")
        else:
            print(" VERDICT           : [ FAIL ] Security Gate Failed!")
            for reason in reasons:
                print(f"  ❌ {reason}")
            print("=" * 65 + "\n")

        return passed
