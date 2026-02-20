"""Test GEP Loop services."""
import pytest
from datetime import datetime

from app.services.scanner import Scanner, ScanResult
from app.services.signal import SignalGenerator, EvolutionSignal
from app.services.intent import IntentClassifier, Intent
from app.services.mutator import Mutator, MutationResult
from app.services.validator import Validator, ValidationResult
from app.services.solidifier import Solidifier
from app.services.gep_loop import GEPLoop


class TestScanner:
    """Test log scanner service."""

    def test_scanner_initialization(self):
        """Test scanner can be initialized."""
        scanner = Scanner()
        assert scanner is not None

    def test_scan_error_log(self):
        """Test scanning error log for patterns."""
        scanner = Scanner()
        log_entry = {
            "timestamp": "2026-02-21T10:00:00Z",
            "level": "ERROR",
            "message": "ConnectionError: Failed to connect to database",
            "source": "app.database",
        }

        result = scanner.scan(log_entry)
        assert isinstance(result, ScanResult)
        assert result.has_issue is True
        assert result.issue_type == "error"
        assert "ConnectionError" in result.patterns

    def test_scan_stagnation_pattern(self):
        """Test detecting stagnation (repeated failures)."""
        scanner = Scanner()
        logs = [
            {"level": "ERROR", "message": "TimeoutError: API call timed out"},
            {"level": "ERROR", "message": "TimeoutError: API call timed out"},
            {"level": "ERROR", "message": "TimeoutError: API call timed out"},
        ]

        result = scanner.detect_stagnation(logs)
        assert result.has_issue is True
        assert result.issue_type == "stagnation"

    def test_scan_success_log(self):
        """Test scanning successful log entry."""
        scanner = Scanner()
        log_entry = {
            "level": "INFO",
            "message": "Task completed successfully",
        }

        result = scanner.scan(log_entry)
        assert result.has_issue is False


class TestSignalGenerator:
    """Test signal generation service."""

    def test_signal_from_error(self):
        """Test generating signal from error scan result."""
        generator = SignalGenerator()
        scan_result = ScanResult(
            has_issue=True,
            issue_type="error",
            patterns=["ConnectionError", "database"],
            context={"source": "app.database"},
        )

        signal = generator.generate(scan_result)
        assert isinstance(signal, EvolutionSignal)
        assert signal.signal_type == "repair"
        assert signal.priority > 0

    def test_signal_from_stagnation(self):
        """Test generating signal from stagnation detection."""
        generator = SignalGenerator()
        scan_result = ScanResult(
            has_issue=True,
            issue_type="stagnation",
            patterns=["TimeoutError"],
            context={"count": 3},
        )

        signal = generator.generate(scan_result)
        assert signal.signal_type == "repair"


class TestIntentClassifier:
    """Test intent classification service."""

    def test_classify_repair_intent(self):
        """Test classifying repair intent from error signal."""
        classifier = IntentClassifier()
        signal = EvolutionSignal(
            signal_type="repair",
            patterns=["ConnectionError"],
            context={},
        )

        intent = classifier.classify(signal)
        assert intent.action == "fix"
        assert intent.target is not None

    def test_classify_optimize_intent(self):
        """Test classifying optimization intent."""
        classifier = IntentClassifier()
        signal = EvolutionSignal(
            signal_type="improve",
            patterns=["performance", "slow"],
            context={},
        )

        intent = classifier.classify(signal)
        assert intent.action == "optimize"


class TestMutator:
    """Test mutation generation service."""

    def test_mutator_initialization(self):
        """Test mutator can be initialized."""
        mutator = Mutator()
        assert mutator is not None

    def test_generate_code_mutation(self):
        """Test generating code mutation."""
        mutator = Mutator()
        intent = Intent(
            action="fix",
            target="database_connection",
            context={"error": "ConnectionError"},
        )

        result = mutator.mutate(intent)
        assert isinstance(result, MutationResult)
        assert result.code is not None or result.prompt is not None

    def test_generate_prompt_mutation(self):
        """Test generating prompt mutation."""
        mutator = Mutator()
        intent = Intent(
            action="optimize",
            target="api_timeout",
            context={"issue": "timeout"},
        )

        result = mutator.mutate(intent)
        assert result.success is True


class TestValidator:
    """Test sandbox validation service."""

    def test_validator_initialization(self):
        """Test validator can be initialized."""
        validator = Validator()
        assert validator is not None

    def test_validate_simple_code(self):
        """Test validating simple code snippet."""
        validator = Validator()
        code = "x = 1 + 1"

        result = validator.validate_code(code)
        assert isinstance(result, ValidationResult)
        assert result.passed is True

    def test_validate_failing_code(self):
        """Test validating code that fails."""
        validator = Validator()
        code = "raise ValueError('test error')"

        result = validator.validate_code(code)
        assert result.passed is False
        assert result.error is not None

    def test_validate_with_tests(self):
        """Test validating code with test cases."""
        validator = Validator()
        code = "def add(a, b): return a + b"
        tests = ["assert add(1, 2) == 3", "assert add(0, 0) == 0"]

        result = validator.validate_with_tests(code, tests)
        assert result.passed is True


class TestSolidifier:
    """Test gene solidification service."""

    def test_solidify_creates_gene(self):
        """Test solidifying validated mutation creates gene."""
        solidifier = Solidifier()
        mutation = MutationResult(
            success=True,
            code="def safe_connect(): pass",
            description="Safe database connection",
        )
        validation = ValidationResult(passed=True)

        gene_data = solidifier.solidify(mutation, validation)
        assert gene_data is not None
        assert gene_data["name"] is not None
        assert gene_data["implementation"] == mutation.code
        assert gene_data["status"] == "validated"


class TestGEPLoop:
    """Test full GEP loop integration."""

    def test_gep_loop_initialization(self):
        """Test GEP loop can be initialized."""
        loop = GEPLoop()
        assert loop is not None

    def test_gep_loop_process_error(self):
        """Test processing an error through the loop."""
        loop = GEPLoop()
        error_log = {
            "level": "ERROR",
            "message": "KeyError: 'missing_key' in config",
        }

        result = loop.process(error_log)
        assert result is not None
        assert result.status in ["success", "failed", "skipped"]
