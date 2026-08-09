"""
database.py

Cloud-Ready Database Persistence Layer for DevSecOps Framework.
Supports Local SQLite, AWS EC2 / RDS PostgreSQL, and AWS RDS MySQL.
"""

from __future__ import annotations

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from security.common.logger import logger

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_PATH = Path(os.getenv("DB_PATH", "compliance/db/security_framework.db"))


class DatabaseManager:
    """
    Manages Database Initialization, Schema Migrations, and Report Ingestion across SQLite, MySQL, and PostgreSQL.
    """

    def __init__(self, db_path: str | Path = DB_PATH, db_type: Optional[str] = None):
        self.db_path = Path(db_path)
        self.db_type = (db_type or DB_TYPE).lower()
        self.init_db()

    def get_connection(self):
        """
        Creates DB connection (SQLite for local, PyMySQL / mysql-connector for MySQL, psycopg2 for PostgreSQL).
        """
        if self.db_type == "sqlite":
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            return conn

        elif self.db_type in ("mysql", "mariadb"):
            try:
                import pymysql
                return pymysql.connect(
                    host=os.getenv("DB_HOST", "localhost"),
                    port=int(os.getenv("DB_PORT", 3306)),
                    database=os.getenv("DB_NAME", "devsecops"),
                    user=os.getenv("DB_USER", "root"),
                    password=os.getenv("DB_PASSWORD", ""),
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True
                )
            except ImportError:
                try:
                    import mysql.connector
                    return mysql.connector.connect(
                        host=os.getenv("DB_HOST", "localhost"),
                        port=int(os.getenv("DB_PORT", 3306)),
                        database=os.getenv("DB_NAME", "devsecops"),
                        user=os.getenv("DB_USER", "root"),
                        password=os.getenv("DB_PASSWORD", "")
                    )
                except ImportError:
                    raise RuntimeError(
                        "MySQL driver missing. Please install PyMySQL or mysql-connector-python: "
                        "pip install pymysql mysql-connector-python"
                    )

        elif self.db_type == "postgres":
            import psycopg2
            import psycopg2.extras
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", 5432)),
                dbname=os.getenv("DB_NAME", "devsecops"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "")
            )
            return conn
        else:
            raise ValueError(f"Unsupported DB_TYPE: {self.db_type}")

    def _ph(self, sql: str) -> str:
        """
        Converts ? SQL parameter placeholders to %s for MySQL / PostgreSQL.
        """
        if self.db_type in ("mysql", "mariadb", "postgres"):
            return sql.replace("?", "%s")
        return sql

    def init_db(self) -> None:
        """
        Creates projects, scans, and findings tables if missing.
        """
        id_auto = "INTEGER PRIMARY KEY AUTOINCREMENT" if self.db_type == "sqlite" else "INT AUTO_INCREMENT PRIMARY KEY"
        txt_type = "TEXT" if self.db_type == "sqlite" else "LONGTEXT"

        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            # 1. Projects Table
            cursor.execute(self._ph("""
                CREATE TABLE IF NOT EXISTS projects (
                    project_id VARCHAR(64) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    repository_url VARCHAR(500),
                    branch VARCHAR(100),
                    created_at VARCHAR(64)
                );
            """))

            # 2. Scans Table
            cursor.execute(self._ph("""
                CREATE TABLE IF NOT EXISTS scans (
                    scan_id VARCHAR(64) PRIMARY KEY,
                    project_id VARCHAR(64),
                    scan_time VARCHAR(64) NOT NULL,
                    title VARCHAR(255),
                    scanners_executed TEXT,
                    total_findings INT DEFAULT 0,
                    critical_count INT DEFAULT 0,
                    high_count INT DEFAULT 0,
                    medium_count INT DEFAULT 0,
                    low_count INT DEFAULT 0,
                    info_count INT DEFAULT 0,
                    fixable_count INT DEFAULT 0,
                    exploitable_count INT DEFAULT 0,
                    scanned_targets INT DEFAULT 0,
                    scanned_packages INT DEFAULT 0,
                    scanned_files INT DEFAULT 0,
                    total_risk_score INT DEFAULT 0,
                    risk_level VARCHAR(32) DEFAULT 'UNKNOWN',
                    compliance_score FLOAT DEFAULT 0.0,
                    owasp_score FLOAT DEFAULT 0.0,
                    cis_score FLOAT DEFAULT 0.0,
                    nist_score FLOAT DEFAULT 0.0,
                    verdict VARCHAR(32) DEFAULT 'UNKNOWN',
                    created_at VARCHAR(64)
                );
            """))

            # 3. Findings Table
            cursor.execute(self._ph(f"""
                CREATE TABLE IF NOT EXISTS findings (
                    id {id_auto},
                    scan_id VARCHAR(64) NOT NULL,
                    project_id VARCHAR(64),
                    tool VARCHAR(64) NOT NULL,
                    category VARCHAR(128),
                    rule_id VARCHAR(128),
                    severity VARCHAR(32),
                    file {txt_type},
                    line INT,
                    message {txt_type},
                    recommendation {txt_type},
                    status VARCHAR(32),
                    scan_time VARCHAR(64),
                    package_name VARCHAR(255),
                    installed_version VARCHAR(100),
                    fixed_version VARCHAR(100),
                    cvss_score FLOAT,
                    cwe {txt_type},
                    cve VARCHAR(100),
                    severity_source VARCHAR(64),
                    target {txt_type},
                    target_class VARCHAR(64),
                    target_type VARCHAR(64),
                    description {txt_type},
                    primary_url {txt_type},
                    references_json {txt_type},
                    compliance_json {txt_type},
                    exploit_available INT DEFAULT 0,
                    fix_available INT DEFAULT 0,
                    epss_score FLOAT,
                    kev INT DEFAULT 0,
                    created_at VARCHAR(64)
                );
            """))

            # Column Migration for existing tables
            cols_to_add_scans = [
                ("project_id", "VARCHAR(64)"),
                ("fixable_count", "INT DEFAULT 0"),
                ("exploitable_count", "INT DEFAULT 0"),
                ("scanned_targets", "INT DEFAULT 0"),
                ("scanned_packages", "INT DEFAULT 0"),
                ("scanned_files", "INT DEFAULT 0"),
                ("owasp_score", "FLOAT DEFAULT 0.0"),
                ("cis_score", "FLOAT DEFAULT 0.0"),
                ("nist_score", "FLOAT DEFAULT 0.0")
            ]
            for col_name, col_def in cols_to_add_scans:
                try:
                    cursor.execute(f"ALTER TABLE scans ADD COLUMN {col_name} {col_def};")
                except Exception:
                    pass

            cols_to_add_findings = [
                ("project_id", "VARCHAR(64)"),
                ("scan_time", "VARCHAR(64)"),
                ("package_name", "VARCHAR(255)"),
                ("installed_version", "VARCHAR(100)"),
                ("fixed_version", "VARCHAR(100)"),
                ("cvss_score", "FLOAT"),
                ("severity_source", "VARCHAR(64)"),
                ("target_class", "VARCHAR(64)"),
                ("target_type", "VARCHAR(64)"),
                ("description", txt_type),
                ("primary_url", txt_type),
                ("references_json", txt_type),
                ("compliance_json", txt_type),
                ("exploit_available", "INT DEFAULT 0"),
                ("fix_available", "INT DEFAULT 0"),
                ("epss_score", "FLOAT"),
                ("kev", "INT DEFAULT 0"),
                ("created_at", "VARCHAR(64)")
            ]
            for col_name, col_def in cols_to_add_findings:
                try:
                    cursor.execute(f"ALTER TABLE findings ADD COLUMN {col_name} {col_def};")
                except Exception:
                    pass

            if self.db_type == "sqlite":
                conn.commit()

        except Exception as ex:
            logger.warning(f"Database initialization warning ({self.db_type}): {ex}")
        finally:
            conn.close()

    def save_master_report(self, master_report: dict, project_name: str = "DevSecOps Pipeline", verdict: str = "UNKNOWN") -> str:
        """
        Ingests master_report.json into projects, scans, and findings tables.
        """
        summary = master_report.get("summary", {})
        risk_summary = master_report.get("risk_summary", {})
        compliance_summary = master_report.get("compliance_summary", {})
        now_iso = datetime.utcnow().isoformat()
        scan_id = f"SCAN-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        project_id = f"PRJ-{project_name.lower().replace(' ', '-')}"
        scanners_str = json.dumps(master_report.get("scanners_executed", []))

        owasp_score = compliance_summary.get("owasp_top_10_2021", {}).get("compliance_percentage", 0.0)
        cis_score = compliance_summary.get("cis_benchmarks", {}).get("compliance_percentage", 0.0)
        nist_score = compliance_summary.get("nist_sp_800_53", {}).get("compliance_percentage", 0.0)

        conn = self.get_connection()
        try:
            cursor = conn.cursor()

            # 1. Upsert Project
            cursor.execute(self._ph("""
                INSERT INTO projects (project_id, name, repository_url, branch, created_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(project_id) DO UPDATE SET created_at = excluded.created_at;
            """ if self.db_type == "sqlite" else """
                INSERT INTO projects (project_id, name, repository_url, branch, created_at)
                VALUES (?, ?, ?, ?, ?)
                ON DUPLICATE KEY UPDATE name=VALUES(name);
            """), (project_id, project_name, "https://github.com/9MayanK2/DevSecOps", "main", now_iso))

            # 2. Insert Scan Record
            cursor.execute(self._ph("""
                INSERT INTO scans (
                    scan_id, project_id, scan_time, title, scanners_executed,
                    total_findings, critical_count, high_count, medium_count, low_count, info_count,
                    fixable_count, exploitable_count, scanned_targets, scanned_packages, scanned_files,
                    total_risk_score, risk_level, compliance_score, owasp_score, cis_score, nist_score,
                    verdict, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """), (
                scan_id, project_id,
                master_report.get("generated_at", now_iso),
                master_report.get("title", "Master DevSecOps Security Report"),
                scanners_str,
                summary.get("total_findings", len(master_report.get("findings", []))),
                summary.get("critical", 0),
                summary.get("high", 0),
                summary.get("medium", 0),
                summary.get("low", 0),
                summary.get("info", 0),
                summary.get("fixable", 0),
                summary.get("exploitable", 0),
                summary.get("scanned_targets", 1),
                summary.get("scanned_packages", 0),
                summary.get("scanned_files", 0),
                risk_summary.get("total_risk_score", 0),
                risk_summary.get("risk_level", "UNKNOWN"),
                summary.get("compliance_score", 100.0),
                owasp_score, cis_score, nist_score,
                verdict, now_iso
            ))

            # 3. Insert Findings
            for finding in master_report.get("findings", []):
                cwe_str = json.dumps(finding.get("cwe", []))
                ref_str = json.dumps(finding.get("references", []))
                comp_str = json.dumps(finding.get("compliance", []))

                cursor.execute(self._ph("""
                    INSERT INTO findings (
                        scan_id, project_id, tool, category, rule_id, severity,
                        file, line, message, recommendation, status, scan_time,
                        package_name, installed_version, fixed_version, cvss_score,
                        cwe, cve, severity_source, target, target_class, target_type,
                        description, primary_url, references_json, compliance_json,
                        exploit_available, fix_available, epss_score, kev, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """), (
                    scan_id, project_id,
                    finding.get("tool", "Unknown"),
                    finding.get("category", "General"),
                    finding.get("rule_id", ""),
                    finding.get("severity", "UNKNOWN"),
                    finding.get("file", ""),
                    finding.get("line"),
                    finding.get("message", ""),
                    finding.get("recommendation", ""),
                    finding.get("status", "OPEN"),
                    finding.get("scan_time", now_iso),
                    finding.get("package_name"),
                    finding.get("installed_version"),
                    finding.get("fixed_version"),
                    finding.get("cvss_score"),
                    cwe_str,
                    finding.get("cve"),
                    finding.get("severity_source"),
                    finding.get("target"),
                    finding.get("target_class"),
                    finding.get("target_type"),
                    finding.get("description"),
                    finding.get("primary_url"),
                    ref_str, comp_str,
                    1 if finding.get("exploit_available") else 0,
                    1 if finding.get("fix_available") else 0,
                    finding.get("epss_score"),
                    1 if finding.get("kev") else 0,
                    now_iso
                ))

            if self.db_type == "sqlite":
                conn.commit()

        except Exception as ex:
            logger.error(f"Database Ingestion Error ({self.db_type}): {ex}")
            raise ex
        finally:
            conn.close()

        logger.info(f"Database Ingestion Successful [{self.db_type.upper()}] (Scan ID: {scan_id})")
        return scan_id

    def update_scan_verdict(self, scan_id: str, verdict: str) -> None:
        """
        Updates the security gate verdict (PASS / FAIL) for a scan record.
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self._ph("UPDATE scans SET verdict = ? WHERE scan_id = ?"), (verdict, scan_id))
            if self.db_type == "sqlite":
                conn.commit()
        except Exception as ex:
            logger.warning(f"Could not update scan verdict: {ex}")
        finally:
            conn.close()

    def get_recent_scans(self, limit: int = 10) -> List[dict]:
        """
        Retrieves recent scan runs from database.
        """
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self._ph("SELECT * FROM scans ORDER BY created_at DESC LIMIT ?"), (limit,))
            rows = cursor.fetchall()
            if self.db_type == "sqlite":
                return [dict(row) for row in rows]
            return list(rows)
        finally:
            conn.close()


def main():
    db = DatabaseManager()
    scans = db.get_recent_scans(5)
    print(f"Database Manager ({db.db_type.upper()}) initialized. Recent scans count: {len(scans)}")


if __name__ == "__main__":
    main()
