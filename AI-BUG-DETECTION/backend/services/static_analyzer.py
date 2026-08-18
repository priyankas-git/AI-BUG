# Ownership: Pavan (API + Static Analysis + Database)
import ast
from typing import Dict, Any, List

class BugVisitor(ast.NodeVisitor):
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.bugs = []

    def visit_BinOp(self, node):
        # 1. Division by Zero AST checks
        if isinstance(node.op, ast.Div):
            # Check literal 0
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                self.bugs.append({
                    "type": "Runtime Error",
                    "severity": "HIGH",
                    "confidence": 1.0,
                    "file": self.file_name,
                    "line": node.lineno,
                    "description": "Division by zero detected.",
                    "explanation": "A division operator has a divisor set to literal zero, leading to an immediate crash.",
                    "impact": "Will raise ZeroDivisionError and crash execution flow.",
                    "suggestion": "Validate that the divisor is not zero before executing division.",
                    "fixed_code": None,
                    "test_case": None
                })
        self.generic_visit(node)

    def visit_Call(self, node):
        # 2. SQL Injection AST checks (e.g. execute("sql..." % params))
        if isinstance(node.func, ast.Attribute) and node.func.attr == "execute":
            if node.args:
                arg = node.args[0]
                is_unsafe = False
                
                # Check for query % args
                if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod):
                    is_unsafe = True
                # Check for query.format(...)
                elif isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute) and arg.func.attr == "format":
                    is_unsafe = True
                # Check for f-string (JoinedStr in AST)
                elif isinstance(arg, ast.JoinedStr):
                    is_unsafe = True
                    
                if is_unsafe:
                    self.bugs.append({
                        "type": "Security Vulnerability",
                        "severity": "CRITICAL",
                        "confidence": 0.95,
                        "file": self.file_name,
                        "line": node.lineno,
                        "description": "SQL Injection vector candidate.",
                        "explanation": "Dynamic string construction (f-string/mod formatting) inside query execution allows attackers to alter query structures.",
                        "impact": "Unauthorized database exposure, modification, or command execution.",
                        "suggestion": "Transition to parameterized database queries (e.g., execute('SELECT * FROM users WHERE name = ?', (name,)))",
                        "fixed_code": None,
                        "test_case": None
                    })
        self.generic_visit(node)

class StaticAnalyzer:
    """
    Performs parsing checks and flags deterministic AST structures.
    """
    def analyze(self, language: str, code: str, file_name: str) -> List[Dict[str, Any]]:
        results = []
        if language.lower() not in ["python", "py"]:
            return results

        try:
            tree = ast.parse(code)
            visitor = BugVisitor(file_name)
            visitor.visit(tree)
            results.extend(visitor.bugs)
        except SyntaxError as e:
            results.append({
                "type": "Syntax Error",
                "severity": "CRITICAL",
                "confidence": 1.0,
                "file": file_name,
                "line": e.lineno,
                "description": f"Syntax Error: {e.msg}",
                "explanation": f"Failed compiling code near line {e.lineno}.",
                "impact": "Prevents compiling or execution.",
                "suggestion": f"Fix syntax structure on line {e.lineno}.",
                "fixed_code": None,
                "test_case": None
            })
        except Exception:
            pass

        return results
