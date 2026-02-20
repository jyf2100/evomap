"""GEP Loop orchestrator - main evolution loop."""
from typing import Optional, Any
from dataclasses import dataclass

from app.services.scanner import Scanner, ScanResult
from app.services.signal import SignalGenerator, EvolutionSignal
from app.services.intent import IntentClassifier, Intent
from app.services.mutator import Mutator, MutationResult
from app.services.validator import Validator, ValidationResult
from app.services.solidifier import Solidifier


@dataclass
class LoopResult:
    """Result of processing a log through the GEP loop."""
    status: str  # success, failed, skipped
    scan_result: Optional[ScanResult] = None
    signal: Optional[EvolutionSignal] = None
    intent: Optional[Intent] = None
    mutation: Optional[MutationResult] = None
    validation: Optional[ValidationResult] = None
    gene_data: Optional[dict] = None
    error: Optional[str] = None


class GEPLoop:
    """Main GEP evolution loop orchestrator.

    Implements the Scan → Signal → Intent → Mutate → Validate → Solidify cycle.
    """

    def __init__(
        self,
        scanner: Optional[Scanner] = None,
        signal_generator: Optional[SignalGenerator] = None,
        intent_classifier: Optional[IntentClassifier] = None,
        mutator: Optional[Mutator] = None,
        validator: Optional[Validator] = None,
        solidifier: Optional[Solidifier] = None,
    ):
        """Initialize GEP loop with optional service overrides.

        Args:
            scanner: Log scanner service.
            signal_generator: Signal generation service.
            intent_classifier: Intent classification service.
            mutator: Mutation generation service.
            validator: Validation service.
            solidifier: Gene solidification service.
        """
        self.scanner = scanner or Scanner()
        self.signal_generator = signal_generator or SignalGenerator()
        self.intent_classifier = intent_classifier or IntentClassifier()
        self.mutator = mutator or Mutator()
        self.validator = validator or Validator()
        self.solidifier = solidifier or Solidifier()

    def process(self, log_entry: dict) -> LoopResult:
        """Process a log entry through the full GEP loop.

        Args:
            log_entry: Log entry to process.

        Returns:
            LoopResult with the outcome of processing.
        """
        try:
            # Phase 1: Scan
            scan_result = self.scanner.scan(log_entry)
            if not scan_result.has_issue:
                return LoopResult(
                    status="skipped",
                    scan_result=scan_result,
                    error="No issue detected in log entry",
                )

            # Phase 2: Signal
            signal = self.signal_generator.generate(scan_result)
            if signal.signal_type == "none":
                return LoopResult(
                    status="skipped",
                    scan_result=scan_result,
                    signal=signal,
                    error="No evolution signal generated",
                )

            # Phase 3: Intent
            intent = self.intent_classifier.classify(signal)

            # Phase 4: Mutate
            mutation = self.mutator.mutate(intent)
            if not mutation.success:
                return LoopResult(
                    status="failed",
                    scan_result=scan_result,
                    signal=signal,
                    intent=intent,
                    mutation=mutation,
                    error="Mutation generation failed",
                )

            # Phase 5: Validate
            if mutation.code:
                validation = self.validator.validate_code(mutation.code)
            elif mutation.prompt:
                validation = self.validator.validate_prompt(mutation.prompt)
            else:
                return LoopResult(
                    status="failed",
                    scan_result=scan_result,
                    signal=signal,
                    intent=intent,
                    mutation=mutation,
                    error="No code or prompt to validate",
                )

            if not validation.passed:
                return LoopResult(
                    status="failed",
                    scan_result=scan_result,
                    signal=signal,
                    intent=intent,
                    mutation=mutation,
                    validation=validation,
                    error=f"Validation failed: {validation.error}",
                )

            # Phase 6: Solidify
            gene_data = self.solidifier.solidify(mutation, validation)
            if not gene_data:
                return LoopResult(
                    status="failed",
                    scan_result=scan_result,
                    signal=signal,
                    intent=intent,
                    mutation=mutation,
                    validation=validation,
                    error="Failed to solidify gene",
                )

            return LoopResult(
                status="success",
                scan_result=scan_result,
                signal=signal,
                intent=intent,
                mutation=mutation,
                validation=validation,
                gene_data=gene_data,
            )

        except Exception as e:
            return LoopResult(
                status="failed",
                error=f"Exception in GEP loop: {type(e).__name__}: {e}",
            )

    def process_batch(self, log_entries: list[dict]) -> list[LoopResult]:
        """Process multiple log entries.

        Args:
            log_entries: List of log entries to process.

        Returns:
            List of LoopResults for each entry.
        """
        return [self.process(entry) for entry in log_entries]
