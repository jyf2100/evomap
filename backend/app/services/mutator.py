"""Mutation generation service."""
from dataclasses import dataclass, field
from typing import Optional

from app.services.intent import Intent


@dataclass
class MutationResult:
    """Result of mutation generation."""
    success: bool = False
    code: Optional[str] = None
    prompt: Optional[str] = None
    description: str = ""
    changes: list[str] = field(default_factory=list)


class Mutator:
    """Generates code and prompt mutations based on intent."""

    # Template mutations for common fixes
    FIX_TEMPLATES = {
        "database_connection": {
            "code": '''def safe_connect(retries=3, delay=1):
    """Safe database connection with retry logic."""
    import time
    for attempt in range(retries):
        try:
            return connect_to_database()
        except ConnectionError as e:
            if attempt == retries - 1:
                raise
            time.sleep(delay * (attempt + 1))
''',
            "description": "Add retry logic for database connections",
        },
        "api_timeout": {
            "code": '''def call_with_timeout(api_func, timeout=30):
    """Call API with configurable timeout."""
    import signal

    def timeout_handler(signum, frame):
        raise TimeoutError(f"API call exceeded {timeout}s timeout")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        result = api_func()
    finally:
        signal.alarm(0)
    return result
''',
            "description": "Add timeout handling for API calls",
        },
        "data_access": {
            "code": '''def safe_get(data, *keys, default=None):
    """Safely access nested dictionary keys."""
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data
''',
            "description": "Add safe dictionary access utility",
        },
    }

    # Prompt templates for optimization
    PROMPT_TEMPLATES = {
        "optimize": {
            "prompt": """When processing {target}:
1. Cache results when possible
2. Use batch processing for multiple items
3. Implement early termination for failed cases
4. Log performance metrics for monitoring
""",
            "description": "Optimization prompt template",
        },
    }

    def mutate(self, intent: Intent) -> MutationResult:
        """Generate a mutation based on intent.

        Args:
            intent: Classified intent for evolution.

        Returns:
            MutationResult with code or prompt changes.
        """
        if intent.action == "fix":
            return self._generate_fix(intent)
        elif intent.action == "optimize":
            return self._generate_optimization(intent)
        elif intent.action == "explore":
            return self._generate_exploration(intent)

        return MutationResult(success=False, description="Unknown action type")

    def _generate_fix(self, intent: Intent) -> MutationResult:
        """Generate a fix mutation.

        Args:
            intent: Intent with fix action.

        Returns:
            MutationResult with fix code.
        """
        target = intent.target or "unknown"

        if target in self.FIX_TEMPLATES:
            template = self.FIX_TEMPLATES[target]
            return MutationResult(
                success=True,
                code=template["code"],
                description=template["description"],
                changes=[f"Added fix for {target}"],
            )

        # Generic fix template
        return MutationResult(
            success=True,
            code=f"# TODO: Implement fix for {target}\npass",
            description=f"Placeholder fix for {target}",
        )

    def _generate_optimization(self, intent: Intent) -> MutationResult:
        """Generate an optimization mutation.

        Args:
            intent: Intent with optimize action.

        Returns:
            MutationResult with optimization code/prompt.
        """
        target = intent.target or "general"

        if target in self.PROMPT_TEMPLATES:
            template = self.PROMPT_TEMPLATES[target]
            return MutationResult(
                success=True,
                prompt=template["prompt"].format(target=target),
                description=template["description"],
                changes=[f"Added optimization for {target}"],
            )

        return MutationResult(
            success=True,
            prompt=f"Optimize {target} for better performance",
            description=f"Generic optimization for {target}",
        )

    def _generate_exploration(self, intent: Intent) -> MutationResult:
        """Generate an exploration mutation.

        Args:
            intent: Intent with explore action.

        Returns:
            MutationResult with exploration prompt.
        """
        return MutationResult(
            success=True,
            prompt=f"""Explore new approaches for {intent.target or 'unknown'}:
1. Research alternative implementations
2. Identify potential improvements
3. Test experimental features
4. Document findings
""",
            description=f"Exploration task for {intent.target}",
            changes=["Added exploration task"],
        )
