from dataclasses import dataclass

@dataclass
class Finding:

    tool: str

    category: str

    rule_id: str

    severity: str

    file: str

    line: int

    message: str

    title: str | None = None

    recommendation: str | None = None

    impact: str | None = None

    reference: str | None = None

    status: str = "OPEN"

    scan_time: str = ""
