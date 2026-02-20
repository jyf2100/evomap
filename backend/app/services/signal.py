"""Signal generation service."""
from dataclasses import dataclass, field
from typing import Optional

from app.services.scanner import ScanResult


@dataclass
class EvolutionSignal:
    """Signal for evolution action."""
    signal_type: str  # repair, improve, innovate
    patterns: list[str] = field(default_factory=list)
    context: dict = field(default_factory=dict)
    priority: int = 1
    source: Optional[str] = None


class SignalGenerator:
    """Generates evolution signals from scan results."""

    # Priority mappings
    PRIORITY_MAP = {
        "error": 10,
        "stagnation": 8,
        "warning": 5,
    }

    # Signal type mappings
    SIGNAL_TYPE_MAP = {
        "error": "repair",
        "stagnation": "repair",
        "warning": "improve",
    }

    def generate(self, scan_result: ScanResult) -> EvolutionSignal:
        """Generate an evolution signal from a scan result.

        Args:
            scan_result: Result from scanner service.

        Returns:
            EvolutionSignal with appropriate type and priority.
        """
        if not scan_result.has_issue:
            return EvolutionSignal(
                signal_type="none",
                priority=0,
            )

        issue_type = scan_result.issue_type or "error"
        signal_type = self.SIGNAL_TYPE_MAP.get(issue_type, "repair")
        priority = self.PRIORITY_MAP.get(issue_type, 1)

        # Boost priority for certain patterns
        if "ConnectionError" in scan_result.patterns:
            priority += 2
        if "TimeoutError" in scan_result.patterns:
            priority += 1

        return EvolutionSignal(
            signal_type=signal_type,
            patterns=scan_result.patterns.copy(),
            context=scan_result.context.copy(),
            priority=min(priority, 10),  # Cap at 10
            source=scan_result.context.get("source"),
        )
