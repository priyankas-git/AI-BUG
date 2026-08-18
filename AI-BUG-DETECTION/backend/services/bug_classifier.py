# Ownership: Disha (AI Bug Detection Engine)
from typing import Dict, Any

class BugClassifier:
    """
    Classifies and normalizes bugs into standard categories.
    """
    def classify(self, bug_details: Dict[str, Any]) -> str:
        valid_types = [
            "Syntax Error", "Logic Error", "Runtime Error", "Security Vulnerability",
            "Performance Issue", "Input Validation Issue", "Exception Handling Issue",
            "API Misuse", "Code Smell"
        ]
        bug_type = bug_details.get("type", "Logic Error").strip()
        for t in valid_types:
            if t.lower() == bug_type.lower():
                return t
        return "Logic Error"
