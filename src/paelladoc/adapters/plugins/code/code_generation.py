from paelladoc.domain.core_logic import mcp
import logging


# Extracted behavior configuration from the original MDC file
BEHAVIOR_CONFIG = {
    "abort_if_documentation_incomplete": True,
    "code_after_documentation": True,
    "confirm_each_parameter": True,
    "conversation_required": True,
    "documentation_first": True,
    "documentation_verification_path": "/docs/{project_name}/.memory.json",
    "enforce_one_question_rule": True,
    "extract_from_complete_documentation": True,
    "force_single_question_mode": True,
    "guide_to_continue_command": True,
    "interactive": True,
    "max_questions_per_message": 1,
    "one_parameter_at_a_time": True,
    "prevent_web_search": True,
    "prohibit_multiple_questions": True,
    "require_complete_documentation": True,
    "require_step_confirmation": True,
    "required_documentation_sections": [
        "project_definition",
        "market_research",
        "user_research",
        "problem_definition",
        "product_definition",
        "architecture_decisions",
        "product_roadmap",
        "user_stories",
        "technical_architecture",
        "technical_specifications",
        "api_specification",
        "database_design",
    ],
    "sequential_questions": True,
    "single_question_mode": True,
    "strict_parameter_sequence": True,
    "strict_question_sequence": True,
    "verify_documentation_completeness": True,
    "wait_for_response": True,
    "wait_for_user_response": True,
}

# TODO: Review imports and add any other necessary modules


@mcp.tool(
    name="code_generation",
    description="The command uses the script at `.cursor/rules/scripts/extract_repo_content.py` to perform the repository extraction, which leverages repopack-py to convert the codebase to text.",
)
def code_code_generation() -> dict:
    """The command uses the script at `.cursor/rules/scripts/extract_repo_content.py` to perform the repository extraction, which leverages repopack-py to convert the codebase to text.

    Behavior Config: this tool has associated behavior configuration extracted
    from the MDC file. See the `BEHAVIOR_CONFIG` variable in the source code.
    """

    # TODO: Implement the actual logic of the command here
    # Access parameters using their variable names (e.g., param)
    # Access behavior config using BEHAVIOR_CONFIG dict (if present)
    logging.info("Executing stub for code.code_generation...")

    # Example: Print parameters
    local_vars = locals()
    param_values = {}
    logging.info(f"Parameters received: {param_values}")

    # Replace with actual return value based on command logic
    return {
        "status": "ok",
        "message": "Successfully executed stub for code.code_generation",
    }
