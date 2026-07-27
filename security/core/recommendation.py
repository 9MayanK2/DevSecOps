"""
Recommendation Engine

Provides remediation guidance for security findings.
"""

import json
from pathlib import Path


RULE_DB = Path("security/knowledge/hadolint_rules.json")


with open(RULE_DB, "r", encoding="utf-8") as file:
    HADOLINT_RULES = json.load(file)


def get_recommendation(rule_id):

    return HADOLINT_RULES.get(
        rule_id,
        {
            "title": "Unknown Rule",
            "recommendation": None,
            "impact": None,
            "reference": None
        }
    )
