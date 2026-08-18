# Ownership: Pavan (API + Static Analysis + Database)
from typing import Dict, Any, List

class ResultFusion:
    """
    Combines static analysis and AI reasoning results into a normalized set of unique bugs.
    """
    def fuse(self, static_results: List[Dict[str, Any]], ai_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # TODO: Dedup based on file, line, and type.
        seen = set()
        fused = []

        for result in static_results + ai_results:
            key = (result.get("file"), result.get("line"), result.get("type"))
            if key not in seen:
                seen.add(key)
                fused.append(result)

        return fused
