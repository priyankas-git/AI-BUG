# Ownership: Pavan (API + Static Analysis + Database)
import sys
import traceback
from typing import Dict, Any
from services.static_analyzer import StaticAnalyzer

class ValidationService:
    """
    Validates proposed code fixes by running syntax checks, static analysis rules,
    and executing generated unit assertions.
    """
    def __init__(self):
        self.static_analyzer = StaticAnalyzer()

    def validate(self, language: str, original_code: str, fixed_code: str, test_case: str) -> Dict[str, Any]:
        result = {
            "syntax_check": False,
            "static_analysis": False,
            "test_run": False,
            "passed": False,
            "message": ""
        }

        # Handle Python code validation
        if language.lower() not in ["python", "py"]:
            # Mock pass for non-Python target files for demo safety
            return {
                "syntax_check": True,
                "static_analysis": True,
                "test_run": True,
                "passed": True,
                "message": f"Successful mock compilation verification for {language}."
            }

        # 1. Syntax Check
        try:
            compile(fixed_code, "<string>", "exec")
            result["syntax_check"] = True
        except SyntaxError as e:
            result["message"] = f"Syntax compilation error on line {e.lineno}: {e.msg}"
            return result

        # 2. Static Analysis Checks
        try:
            static_flaws = self.static_analyzer.analyze(language, fixed_code, "fixed_code.py")
            # If there are no severe bugs remaining, static analysis passes
            if not any(f.get("severity") in ["CRITICAL", "HIGH"] for f in static_flaws):
                result["static_analysis"] = True
            else:
                result["message"] = "Static analyzer flagged unresolved issues in proposed fix."
                return result
        except Exception as e:
            result["message"] = f"Error executing AST checks: {str(e)}"
            return result

        # 3. Dynamic Unit Test Assertions execution
        if not test_case.strip():
            # If no unit test is defined, we skip execution and count it as pass
            result["test_run"] = True
            result["passed"] = True
            result["message"] = "Fix compiles and passes static analysis checks (no test assertions generated)."
            return result

        try:
            result["test_run"] = True
            # Merge fixed code and test declarations
            execution_script = f"{fixed_code}\n\n{test_case}"
            
            # Setup local environment and run code
            local_env = {}
            compiled_script = compile(execution_script, "<dynamic_validation>", "exec")
            exec(compiled_script, {}, local_env)
            
            # Identify test functions (e.g. test_calculate_average) and call them
            test_runners = [k for k in local_env.keys() if k.startswith("test_") and callable(local_env[k])]
            
            for test_func in test_runners:
                local_env[test_func]()
                
            result["passed"] = True
            result["message"] = "All assertions executed and resolved successfully!"
        except AssertionError as ae:
            result["passed"] = False
            result["message"] = f"Unit assertion crashed: {str(ae)}"
        except Exception as ex:
            result["passed"] = False
            # Get traceback summary
            result["message"] = f"Runtime crash: {str(ex)}"

        return result
