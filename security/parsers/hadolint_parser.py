"""
hadolint_parser.py

Enterprise Hadolint Parser

This parser converts Hadolint reports into the
framework's normalized Finding objects.

Responsibilities
----------------
✔ Parse Hadolint JSON
✔ Normalize severity
✔ Attach recommendations
✔ Create Finding objects

Everything else is handled by BaseParser.
"""

from __future__ import annotations

from security.core.base_parser import BaseParser
from security.core.parser_registry import registry

from security.schemas.finding import Finding

from security.common.logger import logger
from security.common.recommendation import get_recommendation
from security.common.severity import normalize_severity
from security.common.status import STATUS_OPEN
from security.common.categories import CATEGORY_CONTAINER
from security.common.scanner_type import SCANNER_STATIC

from security.config.config_loader import get


############################################################
# Configuration
############################################################

TOOL_NAME = "Hadolint"

REPORT_DIR = get(
    "HADOLINT",
    "report_dir"
)

OUTPUT_DIR = get(
    "HADOLINT",
    "output_dir"
)


############################################################
# Hadolint Parser
############################################################

class HadolintParser(BaseParser):

    """
    Enterprise Hadolint parser.

    BaseParser performs:

        ✔ Read report
        ✔ Validate report
        ✔ Metadata generation
        ✔ Statistics
        ✔ Report generation
        ✔ Save report
        ✔ Logging

    This parser only converts Hadolint JSON
    into normalized Finding objects.
    """

    ########################################################
    # Constructor
    ########################################################

    def __init__(self):

        super().__init__(

            tool_name=TOOL_NAME,

            category=CATEGORY_CONTAINER,

            scanner_type=SCANNER_STATIC,

            input_directory=REPORT_DIR,

            output_directory=OUTPUT_DIR

        )

    ########################################################
    # Extract Findings
    ########################################################

    def extract_findings(self):
        """
        Convert Hadolint JSON into
        normalized Finding objects.
        """

        findings = []

        ####################################################
        # Empty Report
        ####################################################

        if not self.raw_report:

            logger.warning(

                "Hadolint report is empty."

            )

            return findings

        ####################################################
        # Parse Every Finding
        ####################################################

        for item in self.raw_report:

            ################################################
            # Normalize Severity
            ################################################

            severity = normalize_severity(

                item.get(

                    "level",

                    "UNKNOWN"

                )

            )

            ################################################
            # Recommendation Database
            ################################################

            recommendation = get_recommendation(

                TOOL_NAME,
                item.get(

                    "code",

                    ""

                )

            )
            ################################################
            # Build Finding
            ################################################

            finding = Finding(

                ################################################
                # Framework
                ################################################

                tool=TOOL_NAME,

                category=CATEGORY_CONTAINER,

                ################################################
                # Rule Information
                ################################################

                rule_id=item.get(

                    "code"

                ),

                title=recommendation.get(

                    "title",

                    item.get(

                        "code",

                        ""

                    )

                ),

                ################################################
                # Severity
                ################################################

                severity=severity,

                ################################################
                # Location
                ################################################

                file=item.get(

                    "file"

                ),

                line=item.get(

                    "line"

                ),

                ################################################
                # Description
                ################################################

                message=item.get(

                    "message"

                ),

                ################################################
                # Recommendation
                ################################################

                recommendation=recommendation.get(

                    "recommendation",

                    "No recommendation available."

                ),

                impact=recommendation.get(

                    "impact",

                    ""

                ),

                reference=recommendation.get(

                    "reference",

                    ""

                ),

                ################################################
                # Runtime
                ################################################

                status=STATUS_OPEN,

                scan_time=self.scan_time

            )

            ################################################
            # Add Finding
            ################################################

            findings.append(

                finding

            )

        ####################################################
        # Finished
        ####################################################

        logger.info(

            f"Parsed {len(findings)} Hadolint findings."

        )

        return findings

    ########################################################
    # Lifecycle Hook
    ########################################################

    def before_parse(self):
        """
        Executed before parsing starts.

        Future use:
            - Load rule cache
            - Download knowledge base
            - Initialize database
        """

        logger.info(

            f"[{TOOL_NAME}] Preparing parser..."

        )

    ########################################################
    # Lifecycle Hook
    ########################################################

    def after_parse(self):
        """
        Executed after parsing completes.

        Future use:
            - Send notifications
            - Push metrics
            - Cleanup resources
        """

        logger.info(

            f"[{TOOL_NAME}] Parser finished successfully."

        )


############################################################
# Register Parser
############################################################

registry.register(

    "hadolint",

    HadolintParser

)


############################################################
# Main
############################################################

def main():

    logger.info(

        "=" * 70

    )

    logger.info(

        "Starting Hadolint Parser"

    )

    logger.info(

        "=" * 70

    )

    parser = HadolintParser()

    parser.run()


if __name__ == "__main__":

    main()
