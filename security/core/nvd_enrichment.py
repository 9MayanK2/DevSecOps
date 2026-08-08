"""
nvd_enrichment.py

NVD API 2.0 Enrichment Engine for DevSecOps Framework.
Enriches findings containing CVE IDs with CWE mappings from the National Vulnerability Database API.
Includes disk-based caching and graceful offline / rate-limit fallbacks.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Optional

from security.common.logger import logger

CACHE_PATH = Path("compliance/db/nvd_cache.json")


class NVDEnricher:
    """
    Enriches CVE identifiers with CWE classifications via NVD API 2.0.
    """

    def __init__(self, cache_path: Path = CACHE_PATH, timeout_seconds: int = 4):
        self.cache_path = Path(cache_path)
        self.timeout = timeout_seconds
        self.cache: Dict[str, List[str]] = self._load_cache()

    def _load_cache(self) -> Dict[str, List[str]]:
        if not self.cache_path.exists():
            return {}
        try:
            with open(self.cache_path, "r", encoding="utf-8") as fp:
                return json.load(fp)
        except Exception as ex:
            logger.warning(f"Could not load NVD cache: {ex}")
            return {}

    def _save_cache(self) -> None:
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, "w", encoding="utf-8") as fp:
                json.dump(self.cache, fp, indent=4)
        except Exception as ex:
            logger.warning(f"Could not save NVD cache: {ex}")

    def fetch_cwes_for_cve(self, cve_id: str) -> List[str]:
        """
        Queries NVD API for a given CVE ID and returns a list of associated CWE IDs.
        """
        cve_clean = cve_id.strip().upper()
        if not cve_clean.startswith("CVE-"):
            return []

        if cve_clean in self.cache:
            return self.cache[cve_clean]

        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_clean}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "SentinelOps-DevSecOps-Framework/1.0"}
        )

        try:
            logger.info(f"Querying NVD API 2.0 for {cve_clean}...")
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    vulnerabilities = data.get("vulnerabilities", [])
                    cwes: List[str] = []
                    if vulnerabilities:
                        cve_item = vulnerabilities[0].get("cve", {})
                        weaknesses = cve_item.get("weaknesses", [])
                        for w in weaknesses:
                            for desc in w.get("description", []):
                                val = desc.get("value", "")
                                if val.startswith("CWE-") and val not in cwes:
                                    cwes.append(val)
                    
                    self.cache[cve_clean] = cwes
                    self._save_cache()
                    logger.info(f"NVD API returned CWEs for {cve_clean}: {cwes}")
                    return cwes
        except Exception as ex:
            logger.warning(f"NVD API enrichment skipped for {cve_clean} (offline/timeout/rate-limited): {ex}")
            # Cache empty to prevent repeated failed network calls during the same run
            self.cache[cve_clean] = []
            self._save_cache()

        return []
