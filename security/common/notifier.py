"""
notifier.py

Enterprise Webhook & Alert Notification Module.
Sends real-time Slack / Microsoft Teams / Webhook alerts on Security Gate failure.
"""

from __future__ import annotations

import os
import json
import urllib.request
import urllib.error

from security.common.logger import logger

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "").strip()


def send_gate_alert(master_report: dict, reasons: list[str], passed: bool) -> bool:
    """
    Sends Security Gate verdict and summary alert via Slack Webhook.
    """
    webhook_url = SLACK_WEBHOOK_URL or os.getenv("WEBHOOK_URL", "").strip()
    if not webhook_url:
        return False

    summary = master_report.get("summary", {})
    risk_summary = master_report.get("risk_summary", {})
    title = master_report.get("title", "DevSecOps Security Pipeline")
    status_str = "PASS" if passed else "FAIL"
    color = "#36a64f" if passed else "#e01e5a"

    payload = {
        "text": f"*{title} — Security Gate Verdict: {status_str}*",
        "attachments": [
            {
                "color": color,
                "fields": [
                    {
                        "title": "Verdict",
                        "value": f"`{status_str}`",
                        "short": True
                    },
                    {
                        "title": "Compliance Score",
                        "value": f"{summary.get('compliance_score', 0.0):.1f}%",
                        "short": True
                    },
                    {
                        "title": "Risk Level",
                        "value": f"{risk_summary.get('risk_level', 'UNKNOWN')}",
                        "short": True
                    },
                    {
                        "title": "Total Findings",
                        "value": f"{summary.get('total_findings', 0)} (Critical: {summary.get('critical', 0)}, High: {summary.get('high', 0)})",
                        "short": True
                    }
                ],
                "footer": "SentinelOps Security Orchestrator"
            }
        ]
    }

    if not passed and reasons:
        payload["attachments"][0]["fields"].append({
            "title": "Failure Reasons",
            "value": "\n".join([f"• {r}" for r in reasons]),
            "short": False
        })

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status in (200, 204):
                logger.info("Security Gate Webhook alert sent successfully.")
                return True
    except Exception as ex:
        logger.warning(f"Could not send Webhook alert: {ex}")

    return False
