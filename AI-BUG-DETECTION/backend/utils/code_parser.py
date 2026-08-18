# Ownership: Pavan (API + Static Analysis + Database)
import ast

class CodeParser:
    """
    Utility helpers for validating syntax and parsing code blocks.
    """
    @staticmethod
    def is_valid_python(code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
