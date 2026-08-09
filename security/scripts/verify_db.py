"""
verify_db.py

Database Persistence & Connectivity Verification Script for CI/CD Pipelines.
Supports graceful fallback and detailed diagnostics.
"""

from __future__ import annotations

import os
import sys
from security.db.database import DatabaseManager
from security.common.logger import logger


def main():
    soft_fail = os.getenv("SOFT_FAIL", "false").lower() == "true" or os.getenv("ENFORCE_GATE", "true").lower() == "false"
    primary_db_type = os.getenv("DB_TYPE", "sqlite").lower()

    # 1. Try Primary Database Connection
    try:
        db = DatabaseManager()
        scans = db.get_recent_scans(1)
        if scans:
            db_dest = "RDS MySQL" if db.db_type != "sqlite" else f"SQLite ({db.db_path})"
            scan_info = scans[0]
            scan_id = scan_info.get("scan_id", "N/A")
            verdict = scan_info.get("verdict", "N/A")
            score = scan_info.get("compliance_score", 0.0)

            print(f"[SUCCESS] Database Connection OK [{db.db_type.upper()} -> {db_dest}]")
            print(f"[SUCCESS] Latest Ingested Scan: {scan_id} | Verdict: {verdict} | Compliance Score: {score:.1f}%")
            sys.exit(0)
        else:
            logger.warning(f"Primary DB ({primary_db_type.upper()}) returned 0 scan records.")
    except Exception as ex:
        logger.warning(f"Could not connect to primary DB ({primary_db_type.upper()}): {ex}")

    # 2. Try Fallback to Local SQLite DB
    if primary_db_type != "sqlite":
        try:
            logger.info("Attempting local SQLite database fallback check...")
            db_sqlite = DatabaseManager(db_type="sqlite")
            scans_sqlite = db_sqlite.get_recent_scans(1)
            if scans_sqlite:
                scan_info = scans_sqlite[0]
                print(f"[SUCCESS] Fallback Database Connection OK [SQLITE -> {db_sqlite.db_path}]")
                print(f"[SUCCESS] Latest Ingested Scan: {scan_info.get('scan_id')} | Verdict: {scan_info.get('verdict')} | Compliance Score: {scan_info.get('compliance_score', 0.0):.1f}%")
                sys.exit(0)
        except Exception as ex:
            logger.warning(f"Local SQLite fallback check failed: {ex}")

    # 3. Soft Fail Handling
    if soft_fail:
        print("⚠️ [WARNING] Database verification unsuccessful, but SOFT_FAIL mode is active. Continuing build...")
        sys.exit(0)
    else:
        logger.error("Database verification failed: No valid scan records found in primary or fallback databases.")
        sys.exit(1)


if __name__ == "__main__":
    main()
