"""
verify_db.py

Database Persistence & Connectivity Verification Script for CI/CD Pipelines.
"""

import sys
from security.db.database import DatabaseManager
from security.common.logger import logger


def main():
    try:
        db = DatabaseManager()
        scans = db.get_recent_scans(1)
        if not scans:
            logger.error("No scan records found in database!")
            sys.exit(1)

        db_dest = "RDS MySQL" if db.db_type != "sqlite" else f"SQLite ({db.db_path})"
        scan_info = scans[0]
        scan_id = scan_info.get("scan_id", "N/A")
        verdict = scan_info.get("verdict", "N/A")
        score = scan_info.get("compliance_score", 0.0)

        print(f"[SUCCESS] Database Connection OK [{db.db_type.upper()} -> {db_dest}]")
        print(f"[SUCCESS] Latest Ingested Scan: {scan_id} | Verdict: {verdict} | Compliance Score: {score:.1f}%")
        sys.exit(0)
    except Exception as ex:
        logger.error(f"Database verification failed: {ex}")
        sys.exit(1)


if __name__ == "__main__":
    main()
