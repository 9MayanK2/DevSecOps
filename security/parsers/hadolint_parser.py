import os
import time
from datetime import datetime

from security.schemas.finding import Finding
from security.schemas.report import Report
from security.schemas.summary import Summary

from security.parsers.parser_utils import (
    load_json,
    save_json,
    dataclass_to_dict,
)

from security.core.logger import logger
from security.core.metadata import generate_metadata
from security.core.recommendation import get_recommendation

from security.core.validator import (
    validate_file_exists,
    validate_json,
    validate_list,
)

from security.core.severity import normalize_severity
from security.core.status import STATUS_OPEN
from security.core.categories import CATEGORY_CONTAINER
from security.core.scanner_type import SCANNER_STATIC

from security.config.config_loader import get


TOOL_NAME = "Hadolint"


REPORT_DIR = get(
    "HADOLINT",
    "report_dir"
)

OUTPUT_DIR = get(
    "HADOLINT",
    "output_dir"
)


def parse_hadolint_report(input_file: str, output_file: str):

    start_time = time.perf_counter()

    logger.info("=" * 70)
    logger.info(f"Starting {TOOL_NAME} Parser")
    logger.info(f"Input Report : {input_file}")

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    validate_file_exists(input_file)

    validate_json(input_file)

    raw_findings = load_json(input_file)

    validate_list(raw_findings)

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    findings = []

    summary = Summary()

    scan_time = datetime.utcnow().isoformat()

    metadata = generate_metadata(TOOL_NAME)

    # --------------------------------------------------
    # Parse Findings
    # --------------------------------------------------

    for item in raw_findings:

        severity = normalize_severity(
            item.get("level")
        )

        rule = get_recommendation(
            item.get("code")
        )

        finding = Finding(

            tool=TOOL_NAME,

            category=CATEGORY_CONTAINER,

            rule_id=item.get("code"),

            severity=severity,

            file=item.get("file"),

            line=item.get("line"),

            message=item.get("message"),

            title=rule["title"],

            recommendation=rule["recommendation"],

            impact=rule["impact"],

            reference=rule["reference"],

            status=STATUS_OPEN,

            scan_time=scan_time

        )

        findings.append(finding)

        summary.total += 1

        if severity == "CRITICAL":
            summary.critical += 1

        elif severity == "HIGH":
            summary.high += 1

        elif severity == "MEDIUM":
            summary.medium += 1

        elif severity == "LOW":
            summary.low += 1

        else:
            summary.info += 1

    # --------------------------------------------------
    # Overall Status
    # --------------------------------------------------

    overall_status = "PASS"

    if summary.total > 0:
        overall_status = "FAIL"

    # --------------------------------------------------
    # Build Report
    # --------------------------------------------------

    report = Report(

        metadata=metadata,

        tool=TOOL_NAME,

        category=CATEGORY_CONTAINER,

        scanner_type=SCANNER_STATIC,

        scan_time=scan_time,

        status=overall_status,

        summary=summary,

        findings=findings

    )

    # --------------------------------------------------
    # Save Report
    # --------------------------------------------------

    save_json(

        dataclass_to_dict(report),

        output_file

    )

    duration = time.perf_counter() - start_time

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    logger.info(f"Output Report : {output_file}")
    logger.info(f"Status        : {overall_status}")
    logger.info(f"Findings      : {summary.total}")
    logger.info(f"Critical      : {summary.critical}")
    logger.info(f"High          : {summary.high}")
    logger.info(f"Medium        : {summary.medium}")
    logger.info(f"Low           : {summary.low}")
    logger.info(f"Info          : {summary.info}")
    logger.info(f"Duration      : {duration:.2f} seconds")
    logger.info(f"Finished {TOOL_NAME} Parser")
    logger.info("=" * 70)


def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    logger.info("Searching Hadolint reports...")

    report_files = sorted(
        os.listdir(REPORT_DIR)
    )

    for report in report_files:

        if not report.endswith(".json"):
            continue

        input_file = os.path.join(
            REPORT_DIR,
            report
        )

        output_file = os.path.join(
            OUTPUT_DIR,
            report.replace(
                ".json",
                "_normalized.json"
            )
        )

        parse_hadolint_report(
            input_file,
            output_file
        )

    logger.info(
        "All Hadolint reports processed successfully."
    )
    logger.info("*" * 70)

if __name__ == "__main__":
    main()
