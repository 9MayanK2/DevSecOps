"""
recommendation.py

Enterprise Recommendation Engine

Responsibilities
----------------
✔ Load rule databases
✔ Cache databases
✔ Return scanner-specific recommendations
✔ Support fallback generation
✔ Future-ready for all scanners
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional


############################################################
# Knowledge Base Directory
############################################################

KNOWLEDGE_DIR = Path("security/knowledge")


############################################################
# Database Cache
############################################################

_RULE_CACHE: Dict[str, dict] = {}


############################################################
# Default Rule
############################################################

DEFAULT_RULE = {

    "title": None,

    "recommendation": None,

    "impact": None,

    "reference": None

}


############################################################
# Database Loader
############################################################

def load_rule_database(scanner: str) -> dict:
    """
    Load rule database for scanner.

    Uses in-memory cache.
    """

    scanner = scanner.lower()

    if scanner in _RULE_CACHE:
        return _RULE_CACHE[scanner]

    rule_file = KNOWLEDGE_DIR / f"{scanner}_rules.json"

    if not rule_file.exists():

        _RULE_CACHE[scanner] = {}

        return {}

    with open(

        rule_file,

        "r",

        encoding="utf-8"

    ) as fp:

        rules = json.load(fp)

    _RULE_CACHE[scanner] = rules

    return rules


############################################################
# Recommendation Lookup
############################################################

def get_recommendation(

    scanner: str,

    rule_id: str

) -> Optional[dict]:
    """
    Return recommendation if present.

    Returns None if rule doesn't exist.
    """

    if not rule_id:
        return None

    rules = load_rule_database(scanner)

    return rules.get(rule_id)


############################################################
# Generic Recommendation Builder
############################################################

def build_generic_recommendation(

    title: str | None = None,

    description: str | None = None,

    fixed_version: str | None = None,

    references: list | None = None,

) -> dict:
    """
    Automatically build a recommendation when
    no local rule exists.
    """

    recommendation = (

        f"Upgrade to fixed version {fixed_version}."

        if fixed_version

        else

        "No vendor fix is currently available."

    )

    reference = None

    if references:

        reference = references[0]

    return {

        "title":

            title,

        "recommendation":

            recommendation,

        "impact":

            description,

        "reference":

            reference

    }


############################################################
# Clear Cache
############################################################

def clear_cache():

    """
    Reload rule databases.

    Useful for testing.
    """

    _RULE_CACHE.clear()
