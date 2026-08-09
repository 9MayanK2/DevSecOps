"""
nvd_enrichment.py

NVD API 2.0 Enrichment Engine for DevSecOps Framework.

Features:
✔ Disk-based caching with TTL (Time-To-Live) expiration
✔ LRU Cache Size Limiting (prevents unlimited disk growth)
✔ NVD API Key support via environment variable (NVD_API_KEY) or constructor
✔ HTTP 429 Rate-Limit backoff handling
✔ Graceful offline / timeout fallbacks
"""

from __future__ import annotations

import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Optional

from security.common.logger import logger

CACHE_PATH = Path("compliance/db/nvd_cache.json")
DEFAULT_TTL_SECONDS = 30 * 86400  # 30 Days TTL
DEFAULT_MAX_ENTRIES = 1000        # Max 1,000 cached CVEs (~100KB limit)


class NVDEnricher:
    """
    Enriches CVE identifiers with CWE classifications via NVD API 2.0.
    Includes LRU pruning, TTL expiration, and NVD API Key authentication.
    """

    def __init__(
        self,
        cache_path: Path = CACHE_PATH,
        timeout_seconds: int = 4,
        ttl_seconds: int = DEFAULT_TTL_SECONDS,
        max_entries: int = DEFAULT_MAX_ENTRIES,
        api_key: Optional[str] = None,
    ):
        self.cache_path = Path(cache_path)
        self.timeout = timeout_seconds
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self.api_key = api_key or os.getenv("NVD_API_KEY", "").strip() or None
        self.cache: Dict[str, dict] = self._load_cache()

    def _load_cache(self) -> Dict[str, dict]:
        if not self.cache_path.exists():
            return {}

        try:
            with open(self.cache_path, "r", encoding="utf-8") as fp:
                raw_data = json.load(fp)

            migrated_cache: Dict[str, dict] = {}
            now = time.time()

            for key, val in raw_data.items():
                # Backward compatibility: Migrate legacy list format -> dictionary format
                if isinstance(val, list):
                    migrated_cache[key] = {
                        "cwes": val,
                        "timestamp": now,
                        "accessed_at": now
                    }
                elif isinstance(val, dict) and "cwes" in val:
                    # Check TTL expiration during load
                    entry_ts = val.get("timestamp", now)
                    if (now - entry_ts) <= self.ttl_seconds:
                        migrated_cache[key] = val

            return migrated_cache

        except Exception as ex:
            logger.warning(f"Could not load NVD cache: {ex}")
            return {}

    def _prune_and_save_cache(self) -> None:
        """
        Enforces LRU max size limits and saves cache to disk.
        """
        try:
            now = time.time()

            # Evict expired TTL entries
            valid_items = [
                (k, v) for k, v in self.cache.items()
                if (now - v.get("timestamp", now)) <= self.ttl_seconds
            ]

            # If exceeding max_entries, prune least recently accessed entries (LRU)
            if len(valid_items) > self.max_entries:
                valid_items.sort(key=lambda item: item[1].get("accessed_at", 0), reverse=True)
                valid_items = valid_items[:self.max_entries]

            self.cache = dict(valid_items)

            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, "w", encoding="utf-8") as fp:
                json.dump(self.cache, fp, indent=4)

        except Exception as ex:
            logger.warning(f"Could not save NVD cache: {ex}")

    def fetch_cwes_for_cve(self, cve_id: str) -> List[str]:
        """
        Queries NVD API 2.0 for a given CVE ID and returns associated CWE IDs.
        Uses cached data if valid and non-expired.
        """
        cve_clean = cve_id.strip().upper()
        if not cve_clean.startswith("CVE-"):
            return []

        now = time.time()

        # Check Cache Hit
        if cve_clean in self.cache:
            entry = self.cache[cve_clean]
            ts = entry.get("timestamp", 0)
            if (now - ts) <= self.ttl_seconds:
                entry["accessed_at"] = now  # Update LRU access timestamp
                return entry.get("cwes", [])
            else:
                logger.info(f"NVD Cache TTL expired for {cve_clean}. Re-fetching...")

        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_clean}"
        headers = {"User-Agent": "SentinelOps-DevSecOps-Framework/1.0"}

        # API Key Support (Increases NVD rate limits from 5 req/30s to 50 req/30s)
        if self.api_key:
            headers["apiKey"] = self.api_key

        req = urllib.request.Request(url, headers=headers)

        try:
            key_status = " (Authenticated with API Key)" if self.api_key else ""
            logger.info(f"Querying NVD API 2.0 for {cve_clean}{key_status}...")

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

                    self.cache[cve_clean] = {
                        "cwes": cwes,
                        "timestamp": now,
                        "accessed_at": now
                    }
                    self._prune_and_save_cache()
                    logger.info(f"NVD API returned CWEs for {cve_clean}: {cwes}")
                    return cwes

        except urllib.error.HTTPError as http_err:
            if http_err.code == 429:
                logger.warning(f"NVD API Rate Limited (HTTP 429) for {cve_clean}. Consider providing NVD_API_KEY.")
            else:
                logger.warning(f"NVD API HTTP Error {http_err.code} for {cve_clean}: {http_err.reason}")

        except Exception as ex:
            logger.warning(f"NVD API enrichment skipped for {cve_clean} (offline/timeout): {ex}")

        # Short temporary cache for offline/timeout to prevent repeating network blocks in current run
        self.cache[cve_clean] = {
            "cwes": [],
            "timestamp": now,
            "accessed_at": now
        }
        self._prune_and_save_cache()
        return []
