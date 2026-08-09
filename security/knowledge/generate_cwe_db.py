"""
generate_cwe_db.py

Auto-generates a comprehensive CWE database mapping MITRE CWEs to:
- OWASP Top 10 (2021)
- NIST SP 800-53 Rev. 5 Controls
- CIS Controls v8
"""

import json
from pathlib import Path

CWE_DB_PATH = Path("security/knowledge/cwe_database.json")

CWE_MAPPINGS = {
    # -------------------------------------------------------------------------
    # Cryptographic Failures & Sensitive Data Protection (OWASP A02 / CIS 3 / NIST IA-5, SC-8, SC-13, SC-28)
    # -------------------------------------------------------------------------
    "CWE-798": {
        "name": "Use of Hard-coded Credentials",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.12 - Rekey or Revoke Credentials",
        "nist": "IA-5 Authenticator Management"
    },
    "CWE-259": {
        "name": "Use of Hard-coded Password",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.12 - Avoid Hardcoded Passwords",
        "nist": "IA-5 Authenticator Management"
    },
    "CWE-522": {
        "name": "Insufficiently Protected Credentials",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.12 - Protect Credentials",
        "nist": "IA-5 Authenticator Management"
    },
    "CWE-916": {
        "name": "Use of Password Hash With Insufficient Computational Effort",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.11 - Encrypt Sensitive Data",
        "nist": "IA-5 Authenticator Management"
    },
    "CWE-312": {
        "name": "Cleartext Storage of Sensitive Information",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.11 - Encrypt Sensitive Data at Rest",
        "nist": "SC-28 Protection of Information at Rest"
    },
    "CWE-319": {
        "name": "Cleartext Transmission of Sensitive Information",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.10 - Encrypt Sensitive Data in Transit",
        "nist": "SC-8 Transmission Confidentiality and Integrity"
    },
    "CWE-325": {
        "name": "Missing Required Cryptographic Step",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.11 - Encrypt Sensitive Data",
        "nist": "SC-13 Cryptographic Protection"
    },
    "CWE-326": {
        "name": "Inadequate Encryption Strength",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.11 - Encrypt Sensitive Data",
        "nist": "SC-13 Cryptographic Protection"
    },
    "CWE-327": {
        "name": "Use of a Broken or Risky Cryptographic Algorithm",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.11 - Encrypt Sensitive Data at Rest",
        "nist": "SC-13 Cryptographic Protection"
    },
    "CWE-295": {
        "name": "Improper Certificate Validation",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.10 - Encrypt Sensitive Data in Transit",
        "nist": "SC-8 Transmission Confidentiality and Integrity"
    },
    "CWE-330": {
        "name": "Use of Insufficiently Random Values",
        "owasp": "A02:2021-Cryptographic Failures",
        "cis": "CIS Controls v8 3.11 - Encrypt Sensitive Data",
        "nist": "SC-13 Cryptographic Protection"
    },

    # -------------------------------------------------------------------------
    # Software & Data Integrity Failures (OWASP A08 / CIS 16 / NIST SI-7)
    # -------------------------------------------------------------------------
    "CWE-347": {
        "name": "Improper Verification of Cryptographic Signature",
        "owasp": "A08:2021-Software and Data Integrity Failures",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-7 Software, Firmware, and Information Integrity"
    },
    "CWE-354": {
        "name": "Improper Validation of Integrity Check Value",
        "owasp": "A08:2021-Software and Data Integrity Failures",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-7 Software, Firmware, and Information Integrity"
    },

    # -------------------------------------------------------------------------
    # Injection & Input Validation (OWASP A03 / CIS 16 / NIST SI-10)
    # -------------------------------------------------------------------------
    "CWE-79": {
        "name": "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-89": {
        "name": "Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-20": {
        "name": "Improper Input Validation",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-78": {
        "name": "Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-94": {
        "name": "Improper Control of Generation of Code ('Code Injection')",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-190": {
        "name": "Integer Overflow or Wraparound",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-704": {
        "name": "Incorrect Type Conversion or Cast",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-917": {
        "name": "Expression Language Injection",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-1336": {
        "name": "Template Engine Injection",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-1325": {
        "name": "Improper Control of Generation of Code or Expression",
        "owasp": "A03:2021-Injection",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },

    # -------------------------------------------------------------------------
    # Broken Access Control & Authorization (OWASP A01 / CIS 5, 16 / NIST AC-3, AC-6)
    # -------------------------------------------------------------------------
    "CWE-22": {
        "name": "Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')",
        "owasp": "A01:2021-Broken Access Control",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "AC-3 Access Enforcement"
    },
    "CWE-200": {
        "name": "Exposure of Sensitive Information to an Unauthorized Actor",
        "owasp": "A01:2021-Broken Access Control",
        "cis": "CIS Controls v8 3.1 - Data Classification",
        "nist": "SC-28 Protection of Information at Rest"
    },
    "CWE-269": {
        "name": "Improper Privilege Management",
        "owasp": "A01:2021-Broken Access Control",
        "cis": "CIS Controls v8 5.2 - Access Control Management",
        "nist": "AC-6 Least Privilege"
    },
    "CWE-862": {
        "name": "Missing Authorization",
        "owasp": "A01:2021-Broken Access Control",
        "cis": "CIS Controls v8 5.2 - Access Control Management",
        "nist": "AC-3 Access Enforcement"
    },
    "CWE-352": {
        "name": "Cross-Site Request Forgery (CSRF)",
        "owasp": "A01:2021-Broken Access Control",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "AC-3 Access Enforcement"
    },
    "CWE-601": {
        "name": "URL Redirection to Untrusted Site ('Open Redirect')",
        "owasp": "A01:2021-Broken Access Control",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "AC-3 Access Enforcement"
    },
    "CWE-639": {
        "name": "Authorization Bypass Through User-Controlled Key (IDOR)",
        "owasp": "A01:2021-Broken Access Control",
        "cis": "CIS Controls v8 5.2 - Access Control Management",
        "nist": "AC-3 Access Enforcement"
    },

    # -------------------------------------------------------------------------
    # Security Misconfiguration & Hardening (OWASP A05 / CIS 4, 16 / NIST CM-6, SI-11)
    # -------------------------------------------------------------------------
    "CWE-693": {
        "name": "Protection Mechanism Failure",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 4.1 - Secure Configuration",
        "nist": "CM-6 Configuration Settings"
    },
    "CWE-1021": {
        "name": "Improper Restriction of Rendered UI Layers or Frames ('Clickjacking')",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SC-7 Boundary Protection"
    },
    "CWE-276": {
        "name": "Incorrect Default Permissions",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 4.1 - Secure Configuration",
        "nist": "CM-6 Configuration Settings"
    },
    "CWE-732": {
        "name": "Incorrect Permission Assignment for Critical Resource",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 4.1 - Secure Configuration",
        "nist": "CM-6 Configuration Settings"
    },
    "CWE-209": {
        "name": "Generation of Error Message Containing Sensitive Information",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 4.1 - Secure Configuration",
        "nist": "SI-11 Error Handling"
    },
    "CWE-248": {
        "name": "Uncaught Exception",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 4.1 - Secure Configuration",
        "nist": "SI-11 Error Handling"
    },
    "CWE-436": {
        "name": "Interpretation Conflict",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-1188": {
        "name": "Insecure Default Initialization of Resource",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 4.1 - Secure Configuration",
        "nist": "CM-6 Configuration Settings"
    },
    "CWE-611": {
        "name": "Improper Restriction of XML External Entity Reference (XXE)",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },
    "CWE-1059": {
        "name": "Command Shell Execution Configuration",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Docker Benchmark 4.6 - Healthcheck Instruction",
        "nist": "CM-6 Configuration Settings"
    },
    "CWE-706": {
        "name": "Use of Incorrect Path Traversal or Absolute Path",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Docker Benchmark 4.0 - Container Hardening",
        "nist": "CM-6 Configuration Settings"
    },
    "CWE-16": {
        "name": "Configuration Error",
        "owasp": "A05:2021-Security Misconfiguration",
        "cis": "CIS Controls v8 4.1 - Secure Configuration",
        "nist": "CM-6 Configuration Settings"
    },

    # -------------------------------------------------------------------------
    # Vulnerable & Outdated Components / Memory Flaws (OWASP A06 / CIS 7 / NIST SI-2)
    # -------------------------------------------------------------------------
    "CWE-119": {
        "name": "Improper Restriction of Operations within Bounds of Memory Buffer",
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "cis": "CIS Controls v8 7.1 - Vulnerability Management",
        "nist": "SI-2 Flaw Remediation"
    },
    "CWE-125": {
        "name": "Out-of-bounds Read",
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "cis": "CIS Controls v8 7.1 - Vulnerability Management",
        "nist": "SI-2 Flaw Remediation"
    },
    "CWE-787": {
        "name": "Out-of-bounds Write",
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "cis": "CIS Controls v8 7.1 - Vulnerability Management",
        "nist": "SI-2 Flaw Remediation"
    },
    "CWE-416": {
        "name": "Use After Free",
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "cis": "CIS Controls v8 7.1 - Vulnerability Management",
        "nist": "SI-2 Flaw Remediation"
    },
    "CWE-825": {
        "name": "Expired Pointer Dereference",
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "cis": "CIS Controls v8 7.1 - Vulnerability Management",
        "nist": "SI-2 Flaw Remediation"
    },
    "CWE-476": {
        "name": "NULL Pointer Dereference",
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "cis": "CIS Controls v8 7.1 - Vulnerability Management",
        "nist": "SI-2 Flaw Remediation"
    },
    "CWE-1104": {
        "name": "Use of Unmaintained Third Party Components",
        "owasp": "A06:2021-Vulnerable and Outdated Components",
        "cis": "CIS Controls v8 7.1 - Vulnerability Management",
        "nist": "SI-2 Flaw Remediation"
    },

    # -------------------------------------------------------------------------
    # Authentication & Identification Failures (OWASP A07 / CIS 6 / NIST IA-2)
    # -------------------------------------------------------------------------
    "CWE-287": {
        "name": "Improper Authentication",
        "owasp": "A07:2021-Identification and Authentication Failures",
        "cis": "CIS Controls v8 6.1 - Multi-Factor Authentication",
        "nist": "IA-2 Identification and Authentication"
    },
    "CWE-306": {
        "name": "Missing Authentication for Critical Function",
        "owasp": "A07:2021-Identification and Authentication Failures",
        "cis": "CIS Controls v8 6.1 - Multi-Factor Authentication",
        "nist": "IA-2 Identification and Authentication"
    },
    "CWE-307": {
        "name": "Improper Restriction of Excessive Authentication Attempts",
        "owasp": "A07:2021-Identification and Authentication Failures",
        "cis": "CIS Controls v8 6.1 - Multi-Factor Authentication",
        "nist": "IA-2 Identification and Authentication"
    },

    # -------------------------------------------------------------------------
    # Insecure Design & System Architecture (OWASP A04 / CIS 13 / NIST SC-5, SC-7)
    # -------------------------------------------------------------------------
    "CWE-400": {
        "name": "Uncontrolled Resource Consumption",
        "owasp": "A04:2021-Insecure Design",
        "cis": "CIS Controls v8 13.1 - Network Architecture",
        "nist": "SC-5 Denial of Service Protection"
    },
    "CWE-770": {
        "name": "Allocation of Resources Without Limits or Throttling",
        "owasp": "A04:2021-Insecure Design",
        "cis": "CIS Controls v8 13.1 - Network Architecture",
        "nist": "SC-5 Denial of Service Protection"
    },
    "CWE-1333": {
        "name": "Inefficient Regular Expression Complexity (ReDoS)",
        "owasp": "A04:2021-Insecure Design",
        "cis": "CIS Controls v8 13.1 - Network Architecture",
        "nist": "SC-5 Denial of Service Protection"
    },
    "CWE-407": {
        "name": "Algorithmic Complexity Vulnerability",
        "owasp": "A04:2021-Insecure Design",
        "cis": "CIS Controls v8 13.1 - Network Architecture",
        "nist": "SC-5 Denial of Service Protection"
    },
    "CWE-835": {
        "name": "Loop with Unreachable Exit Condition (Infinite Loop)",
        "owasp": "A04:2021-Insecure Design",
        "cis": "CIS Controls v8 13.1 - Network Architecture",
        "nist": "SC-5 Denial of Service Protection"
    },
    "CWE-514": {
        "name": "Covert Channel",
        "owasp": "A04:2021-Insecure Design",
        "cis": "CIS Controls v8 13.1 - Network Architecture",
        "nist": "SC-7 Boundary Protection"
    },
    "CWE-502": {
        "name": "Deserialization of Untrusted Data",
        "owasp": "A08:2021-Software and Data Integrity Failures",
        "cis": "CIS Controls v8 16.1 - Application Software Security",
        "nist": "SI-10 Information Input Validation"
    },

    # -------------------------------------------------------------------------
    # Security Logging & SSRF (OWASP A09, A10 / CIS 8, 13 / NIST AU-2, SC-7)
    # -------------------------------------------------------------------------
    "CWE-532": {
        "name": "Insertion of Sensitive Information into Log File",
        "owasp": "A09:2021-Security Logging and Monitoring Failures",
        "cis": "CIS Controls v8 8.2 - Audit Log Management",
        "nist": "AU-2 Event Logging"
    },
    "CWE-918": {
        "name": "Server-Side Request Forgery (SSRF)",
        "owasp": "A10:2021-Server-Side Request Forgery (SSRF)",
        "cis": "CIS Controls v8 13.3 - Filter Network Traffic",
        "nist": "SC-7 Boundary Protection"
    }
}


def generate_database():
    CWE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CWE_DB_PATH, "w", encoding="utf-8") as fp:
        json.dump(CWE_MAPPINGS, fp, indent=4)
    print(f"✅ Generated open standards CWE database with {len(CWE_MAPPINGS)} entries at {CWE_DB_PATH}")


if __name__ == "__main__":
    generate_database()
