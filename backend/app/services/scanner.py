"""Scanner service for log analysis and pattern detection."""
from dataclasses import dataclass, field
from typing import Optional
from collections import Counter


@dataclass
class ScanResult:
    """Result of scanning a log entry."""
    has_issue: bool = False
    issue_type: Optional[str] = None
    patterns: list[str] = field(default_factory=list)
    context: dict = field(default_factory=dict)
    raw_log: Optional[dict] = None


class Scanner:
    """Scans logs to detect errors and stagnation patterns."""

    # Known error patterns to detect
    ERROR_PATTERNS = [
        "ConnectionError",
        "TimeoutError",
        "KeyError",
        "ValueError",
        "NotFoundError",
        "Error",
        "Exception",
        "Failed",
        "Timeout",
        "ConnectionRefused",
        "NotFound",
    ]

    # Patterns that indicate stagnation when repeated
    STAGNATION_PATTERNS = [
        "TimeoutError",
        "ConnectionError",
        "RateLimitError",
    ]

    def __init__(self, stagnation_threshold: int = 3):
        """Initialize scanner.

        Args:
            stagnation_threshold: Number of repeated errors to consider stagnation.
        """
        self.stagnation_threshold = stagnation_threshold
        self._error_history: list[str] = []

    def scan(self, log_entry: dict) -> ScanResult:
        """Scan a single log entry for issues.

        Args:
            log_entry: Dictionary with log data (level, message, etc.)

        Returns:
            ScanResult with detected patterns and context.
        """
        level = log_entry.get("level", "").upper()
        message = log_entry.get("message", "")
        source = log_entry.get("source", "")

        # Check for error level
        if level == "ERROR":
            patterns = self._extract_patterns(message)
            return ScanResult(
                has_issue=True,
                issue_type="error",
                patterns=patterns,
                context={"source": source, "level": level},
                raw_log=log_entry,
            )

        # Check for warning with known patterns
        if level == "WARNING":
            patterns = self._extract_patterns(message)
            if patterns:
                return ScanResult(
                    has_issue=True,
                    issue_type="warning",
                    patterns=patterns,
                    context={"source": source, "level": level},
                    raw_log=log_entry,
                )

        # No issue detected
        return ScanResult(
            has_issue=False,
            raw_log=log_entry,
        )

    def detect_stagnation(self, logs: list[dict]) -> ScanResult:
        """Detect stagnation patterns from multiple log entries.

        Args:
            logs: List of log entries to analyze.

        Returns:
            ScanResult indicating if stagnation was detected.
        """
        error_messages = []
        for log in logs:
            if log.get("level") == "ERROR":
                error_messages.append(log.get("message", ""))

        # Count error patterns
        pattern_counter = Counter()
        for msg in error_messages:
            for pattern in self.STAGNATION_PATTERNS:
                if pattern in msg:
                    pattern_counter[pattern] += 1

        # Check for stagnation
        for pattern, count in pattern_counter.items():
            if count >= self.stagnation_threshold:
                return ScanResult(
                    has_issue=True,
                    issue_type="stagnation",
                    patterns=[pattern],
                    context={"count": count, "total_errors": len(error_messages)},
                )

        return ScanResult(has_issue=False)

    def _extract_patterns(self, message: str) -> list[str]:
        """Extract known error patterns from message.

        Args:
            message: Log message to analyze.

        Returns:
            List of detected patterns.
        """
        patterns = []
        for pattern in self.ERROR_PATTERNS:
            if pattern in message:
                patterns.append(pattern)
        return patterns
