"""Solidifier service for creating genes from validated mutations."""
import hashlib
from datetime import datetime
from typing import Optional

from app.services.mutator import MutationResult
from app.services.validator import ValidationResult


class Solidifier:
    """Solidifies validated mutations into genes."""

    def __init__(self, prefix: str = "auto"):
        """Initialize solidifier.

        Args:
            prefix: Prefix for auto-generated gene names.
        """
        self.prefix = prefix
        self._counter = 0

    def solidify(
        self,
        mutation: MutationResult,
        validation: ValidationResult,
        name: Optional[str] = None,
    ) -> Optional[dict]:
        """Create gene data from validated mutation.

        Args:
            mutation: Successful mutation result.
            validation: Passed validation result.
            name: Optional name for the gene.

        Returns:
            Dictionary with gene data or None if invalid.
        """
        if not mutation.success or not validation.passed:
            return None

        # Generate unique name if not provided
        if not name:
            self._counter += 1
            name = f"{self.prefix}_gene_{self._counter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Generate ID from content hash
        content = (mutation.code or "") + (mutation.prompt or "")
        gene_id = hashlib.sha256(content.encode()).hexdigest()[:16]

        # Create gene data
        gene_data = {
            "id": f"gene_{gene_id}",
            "name": name,
            "description": mutation.description,
            "implementation": mutation.code,
            "prompt_template": mutation.prompt,
            "status": "validated",
            "success_rate": self._calculate_success_rate(validation),
            "context_tags": self._extract_tags(mutation),
        }

        return gene_data

    def _calculate_success_rate(self, validation: ValidationResult) -> float:
        """Calculate success rate from validation results.

        Args:
            validation: Validation result.

        Returns:
            Success rate between 0 and 1.
        """
        if not validation.test_results:
            # No tests = assume 1.0 for simple validation
            return 1.0 if validation.passed else 0.0

        passed = sum(1 for t in validation.test_results if t.get("passed"))
        total = len(validation.test_results)

        return passed / total if total > 0 else 0.0

    def _extract_tags(self, mutation: MutationResult) -> list[str]:
        """Extract context tags from mutation.

        Args:
            mutation: Mutation result.

        Returns:
            List of context tags.
        """
        tags = ["auto-generated"]

        if mutation.code:
            tags.append("code")

        if mutation.prompt:
            tags.append("prompt")

        # Extract from description
        desc_lower = mutation.description.lower()
        if "fix" in desc_lower or "repair" in desc_lower:
            tags.append("fix")
        if "optimize" in desc_lower:
            tags.append("optimization")
        if "retry" in desc_lower:
            tags.append("resilience")
        if "timeout" in desc_lower:
            tags.append("timeout-handling")

        return list(set(tags))
