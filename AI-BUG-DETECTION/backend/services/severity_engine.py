# Ownership: Disha (AI Bug Detection Engine)
from typing import Dict, Any

class SeverityEngine:
    """
    Evaluates or adjusts severity levels:
    - CRITICAL (security compromises, major flaws)
    - HIGH (major logic failures)
    - MEDIUM (limited functionality, edge cases)
    - LOW (minor maintainability or code-quality)
    """
    def evaluate(self, bug_details: Dict[str, Any]) -> str:
        # TODO: Business logic to normalize severity levels
        severity = bug_details.get("severity", "MEDIUM").upper()
        if severity not in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            return "MEDIUM"
        return severity
