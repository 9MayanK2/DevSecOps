from dataclasses import dataclass, field
from typing import List

from .finding import Finding
from .summary import Summary


@dataclass
class Report:

    metadata: dict

    tool: str

    category: str

    scanner_type: str

    scan_time: str

    status: str

    summary: Summary

    findings: List[Finding] = field(default_factory=list)
