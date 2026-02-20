"""Validation service for sandbox execution."""
from dataclasses import dataclass, field
from typing import Optional
import ast


@dataclass
class ValidationResult:
    """Result of validation."""
    passed: bool = False
    error: Optional[str] = None
    output: Optional[str] = None
    execution_time_ms: Optional[float] = None
    test_results: list[dict] = field(default_factory=list)


class Validator:
    """Validates mutations in a sandbox environment."""

    def __init__(self, timeout_seconds: int = 5):
        """Initialize validator.

        Args:
            timeout_seconds: Maximum execution time for validation.
        """
        self.timeout_seconds = timeout_seconds

    def validate_code(self, code: str) -> ValidationResult:
        """Validate code by checking syntax and executing.

        Args:
            code: Code string to validate.

        Returns:
            ValidationResult with pass/fail status.
        """
        # First check syntax
        try:
            ast.parse(code)
        except SyntaxError as e:
            return ValidationResult(
                passed=False,
                error=f"Syntax error: {e}",
            )

        # Try to execute in restricted environment
        try:
            import time
            start = time.time()

            # Create restricted globals
            restricted_globals = {
                "__builtins__": {
                    "print": print,
                    "len": len,
                    "range": range,
                    "str": str,
                    "int": int,
                    "float": float,
                    "list": list,
                    "dict": dict,
                    "True": True,
                    "False": False,
                    "None": None,
                }
            }

            exec(code, restricted_globals)

            execution_time = (time.time() - start) * 1000

            return ValidationResult(
                passed=True,
                execution_time_ms=execution_time,
            )

        except Exception as e:
            return ValidationResult(
                passed=False,
                error=f"Execution error: {type(e).__name__}: {e}",
            )

    def validate_with_tests(self, code: str, tests: list[str]) -> ValidationResult:
        """Validate code with test cases.

        Args:
            code: Code string to validate.
            tests: List of test assertions.

        Returns:
            ValidationResult with test results.
        """
        # First validate basic code
        base_result = self.validate_code(code)
        if not base_result.passed:
            return base_result

        # Run tests
        test_results = []
        all_passed = True

        try:
            # Create execution environment with code
            exec_globals = {
                "__builtins__": __builtins__,
            }
            exec(code, exec_globals)

            # Run each test
            for i, test in enumerate(tests):
                try:
                    exec(test, exec_globals)
                    test_results.append({
                        "test": i + 1,
                        "passed": True,
                        "code": test,
                    })
                except AssertionError as e:
                    all_passed = False
                    test_results.append({
                        "test": i + 1,
                        "passed": False,
                        "error": str(e),
                        "code": test,
                    })
                except Exception as e:
                    all_passed = False
                    test_results.append({
                        "test": i + 1,
                        "passed": False,
                        "error": f"{type(e).__name__}: {e}",
                        "code": test,
                    })

            return ValidationResult(
                passed=all_passed,
                test_results=test_results,
            )

        except Exception as e:
            return ValidationResult(
                passed=False,
                error=f"Test execution error: {e}",
                test_results=test_results,
            )

    def validate_prompt(self, prompt: str) -> ValidationResult:
        """Validate a prompt template.

        Args:
            prompt: Prompt string to validate.

        Returns:
            ValidationResult with pass/fail status.
        """
        # Basic validation - check for common issues
        issues = []

        if not prompt or not prompt.strip():
            issues.append("Prompt is empty")

        if len(prompt) > 10000:
            issues.append("Prompt is too long (>10000 chars)")

        # Check for unbalanced braces (common in templates)
        if prompt.count("{") != prompt.count("}"):
            issues.append("Unbalanced braces in prompt template")

        if issues:
            return ValidationResult(
                passed=False,
                error="; ".join(issues),
            )

        return ValidationResult(passed=True)
