"""
validator.py

Enterprise Validation Utilities

Reusable validation functions used across
all security parsers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from security.core.exceptions import (
    ValidationError,
    InvalidReportError,
)


############################################################
# File Validation
############################################################

def validate_file_exists(path: str | Path) -> None:
    """
    Ensure a report file exists.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Report not found: {path}"
        )


############################################################
# Directory Validation
############################################################

def validate_directory(path: str | Path) -> None:
    """
    Ensure directory exists.
    """

    path = Path(path)

    if not path.exists():

        raise FileNotFoundError(
            f"Directory not found: {path}"
        )

    if not path.is_dir():

        raise ValidationError(
            f"{path} is not a directory."
        )


############################################################
# JSON Validation
############################################################

def validate_json(path: str | Path) -> None:
    """
    Ensure a file contains valid JSON.
    """

    validate_file_exists(path)

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as fp:

            json.load(fp)

    except json.JSONDecodeError as ex:

        raise InvalidReportError(
            f"Invalid JSON file: {path}"
        ) from ex


############################################################
# Dictionary Validation
############################################################

def validate_dict(data: Any) -> None:
    """
    Ensure report is a dictionary.
    """

    if not isinstance(data, dict):

        raise ValidationError(
            "Expected dictionary report."
        )


############################################################
# List Validation
############################################################

def validate_list(data: Any) -> None:
    """
    Ensure report is a list.
    """

    if not isinstance(data, list):

        raise ValidationError(
            "Expected list report."
        )


############################################################
# Empty Validation
############################################################

def validate_not_empty(data: Any) -> None:
    """
    Ensure report contains data.
    """

    if data is None:

        raise ValidationError(
            "Report is empty."
        )

    if hasattr(data, "__len__"):

        if len(data) == 0:

            raise ValidationError(
                "Report contains no data."
            )


############################################################
# Required Keys
############################################################

def validate_required_keys(
    data: dict,
    keys: Iterable[str],
) -> None:
    """
    Ensure required keys exist.
    """

    validate_dict(data)

    missing = [

        key

        for key in keys

        if key not in data

    ]

    if missing:

        raise ValidationError(

            "Missing required keys: "

            + ", ".join(missing)

        )


############################################################
# Generic Report Validation
############################################################

def validate_report(data: Any) -> None:
    """
    Generic validation used by BaseParser.

    Accepts dictionary or list reports.
    """

    validate_not_empty(data)

    if not isinstance(

        data,

        (dict, list)

    ):

        raise ValidationError(

            "Unsupported report format."

        )


############################################################
# Trivy Validation
############################################################

def validate_trivy_report(data: dict) -> None:
    """
    Validate minimum Trivy structure.
    """

    validate_required_keys(

        data,

        [

            "Results",

        ]

    )


############################################################
# Hadolint Validation
############################################################

def validate_hadolint_report(data: list) -> None:
    """
    Validate Hadolint report.
    """

    validate_list(data)

    validate_not_empty(data)
