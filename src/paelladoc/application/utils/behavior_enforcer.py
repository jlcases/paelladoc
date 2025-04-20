"""
Utility for enforcing behavior rules defined in tool configurations.
"""

import logging
from typing import Dict, Any, Set, Optional

# Assuming MCPContext structure or relevant parts are accessible
# from mcp.context import Context as MCPContext # Or use Any for now

logger = logging.getLogger(__name__)

class BehaviorViolationError(Exception):
    """Custom exception raised when a behavior rule is violated."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BehaviorEnforcer:
    """Enforces conversational behavior based on tool config and context."""

    @staticmethod
    def enforce(
        tool_name: str,
        behavior_config: Optional[Dict[str, Any]], 
        ctx: Optional[Any], # Replace Any with actual MCPContext type if available
        provided_args: Optional[Dict[str, Any]]
    ):
        """Checks current context and arguments against behavior rules.
        
        Args:
            tool_name: The name of the tool being called.
            behavior_config: The BEHAVIOR_CONFIG dictionary for the tool.
            ctx: The current MCP context object (expected to have ctx.progress).
            provided_args: The arguments passed to the tool function in the current call.
            
        Raises:
            BehaviorViolationError: If a rule is violated.
        """
        if not behavior_config:
            logger.debug(f"No behavior config for tool '{tool_name}', skipping enforcement.")
            return
        
        if not ctx or not hasattr(ctx, 'progress') or not provided_args:
            logger.warning(f"Behavior enforcement skipped for '{tool_name}': missing context or args.")
            # Decide if this should be an error or just skipped
            return 

        # --- Enforce fixed_question_order --- 
        if "fixed_question_order" in behavior_config:
            sequence = behavior_config["fixed_question_order"]
            if not isinstance(sequence, list):
                 logger.warning(f"Invalid 'fixed_question_order' in config for {tool_name}. Skipping check.")
                 return

            # Assume ctx.progress['collected_params'] holds previously gathered arguments
            collected_params: Set[str] = ctx.progress.get("collected_params", set())
            
            # Identify arguments provided in *this* specific call (non-None values)
            current_call_args = {k for k, v in provided_args.items() if v is not None}
            
            # Identify which of the currently provided args are *new* (not already collected)
            newly_provided_params = current_call_args - collected_params

            if not newly_provided_params:
                # No *new* parameters were provided in this call. 
                # This might be okay if just confirming or if sequence is done.
                # Or maybe it should error if the sequence is *not* done?
                # For now, allow proceeding. Behavior could be refined.
                logger.debug(f"Tool '{tool_name}': No new parameters provided, sequence check passes by default.")
                return

            # Find the first parameter in the defined sequence that hasn't been collected yet
            expected_next_param = None
            for param in sequence:
                if param not in collected_params:
                    expected_next_param = param
                    break

            if expected_next_param is None:
                # The defined sequence is complete.
                # Should we allow providing *other* (optional?) parameters now?
                # If strict_parameter_sequence is True, maybe disallow?
                # For now, allow extra parameters after the main sequence.
                logger.debug(f"Tool '{tool_name}': Sequence complete, allowing provided args: {newly_provided_params}")
                return

            # --- Enforce one_parameter_at_a_time (implicitly for sequence) --- 
            # Check if exactly one *new* parameter was provided and if it's the expected one.
            if len(newly_provided_params) > 1:
                 raise BehaviorViolationError(
                     f"Tool '{tool_name}' expects parameters sequentially. "
                     f"Expected next: '{expected_next_param}'. "
                     f"Provided multiple new parameters: {newly_provided_params}. "
                     f"Collected so far: {collected_params}."
                 )
                 
            provided_param = list(newly_provided_params)[0]
            if provided_param != expected_next_param:
                 raise BehaviorViolationError(
                     f"Tool '{tool_name}' expects parameters sequentially. "
                     f"Expected next: '{expected_next_param}'. "
                     f"Got unexpected new parameter: '{provided_param}'. "
                     f"Collected so far: {collected_params}."
                 )

            # If we reach here, exactly one new parameter was provided and it was the expected one.
            logger.debug(f"Tool '{tool_name}': Correct sequential parameter '{provided_param}' provided.")
            
        # --- Add other rule checks here as needed --- 
        # e.g., max_questions_per_message (more complex, needs turn context)
        # e.g., documentation_first (likely better as separate middleware/check)

        # If all checks pass
        return 