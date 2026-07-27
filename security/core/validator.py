"""
Validation utilities for security parsers.
"""

import json
import os


def validate_file_exists(path: str):
    """
    Ensure the report file exists.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Report not found: {path}"
        )


def validate_json(path: str):
    """
    Ensure report contains valid JSON.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            json.load(file)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON: {path}\n{e}"
        )


def validate_list(data):
    """
    Hadolint JSON should be a list.
    """
    if not isinstance(data, list):
        raise ValueError(
            "Expected Hadolint report to be a JSON list."
        )
