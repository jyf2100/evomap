"""Intent classification service."""
from dataclasses import dataclass, field
from typing import Optional

from app.services.signal import EvolutionSignal


@dataclass
class Intent:
    """Classified intent for evolution action."""
    action: str  # fix, optimize, innovate, explore
    target: Optional[str] = None
    context: dict = field(default_factory=dict)
    confidence: float = 1.0


class IntentClassifier:
    """Classifies evolution signals into actionable intents."""

    # Action mappings based on signal type
    ACTION_MAP = {
        "repair": "fix",
        "improve": "optimize",
        "innovate": "explore",
    }

    # Target inference from patterns
    TARGET_PATTERNS = {
        "ConnectionError": "database_connection",
        "TimeoutError": "api_timeout",
        "KeyError": "data_access",
        "ValueError": "data_validation",
        "NotFoundError": "resource_lookup",
    }

    def classify(self, signal: EvolutionSignal) -> Intent:
        """Classify an evolution signal into an intent.

        Args:
            signal: Evolution signal to classify.

        Returns:
            Intent with action, target, and context.
        """
        action = self.ACTION_MAP.get(signal.signal_type, "fix")

        # Infer target from patterns
        target = self._infer_target(signal.patterns)

        # Calculate confidence based on pattern match
        confidence = self._calculate_confidence(signal)

        return Intent(
            action=action,
            target=target,
            context={
                **signal.context,
                "patterns": signal.patterns,
                "priority": signal.priority,
            },
            confidence=confidence,
        )

    def _infer_target(self, patterns: list[str]) -> Optional[str]:
        """Infer target component from error patterns.

        Args:
            patterns: List of detected patterns.

        Returns:
            Inferred target or None.
        """
        for pattern in patterns:
            if pattern in self.TARGET_PATTERNS:
                return self.TARGET_PATTERNS[pattern]
        return "unknown"

    def _calculate_confidence(self, signal: EvolutionSignal) -> float:
        """Calculate confidence score for classification.

        Args:
            signal: Evolution signal.

        Returns:
            Confidence score between 0 and 1.
        """
        base_confidence = 0.7

        # More patterns = higher confidence
        pattern_bonus = min(len(signal.patterns) * 0.1, 0.2)

        # Higher priority = higher confidence
        priority_bonus = signal.priority * 0.01

        return min(base_confidence + pattern_bonus + priority_bonus, 1.0)
