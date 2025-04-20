"""
Unit tests for the BehaviorEnforcer utility.
"""

import unittest
import sys
from pathlib import Path
from typing import Set, Optional

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Module to test
from paelladoc.application.utils.behavior_enforcer import (
    BehaviorEnforcer,
    BehaviorViolationError,
)


# Mock context object for tests
class MockContext:
    def __init__(self, collected_params: Optional[Set[str]] = None):
        self.progress = {
            "collected_params": collected_params
            if collected_params is not None
            else set()
        }


class TestBehaviorEnforcer(unittest.TestCase):
    """Unit tests for the BehaviorEnforcer."""

    def setUp(self):
        self.tool_name = "test.tool"
        self.sequence = ["param1", "param2", "param3"]
        self.behavior_config = {"fixed_question_order": self.sequence}

    def test_enforce_no_config(self):
        """Test that enforcement passes if no behavior_config is provided."""
        try:
            BehaviorEnforcer.enforce(self.tool_name, None, MockContext(), {"arg": 1})
        except BehaviorViolationError:
            self.fail("Enforcement should pass when no config is given.")

    def test_enforce_no_fixed_order(self):
        """Test enforcement passes if 'fixed_question_order' is not in config."""
        config = {"other_rule": True}
        try:
            BehaviorEnforcer.enforce(
                self.tool_name, config, MockContext(), {"param1": "value"}
            )
        except BehaviorViolationError:
            self.fail(
                "Enforcement should pass when fixed_question_order is not defined."
            )

    def test_enforce_no_context_or_args(self):
        """Test enforcement passes (logs warning) if context or args are missing."""
        # Note: Current implementation returns None (passes), might change behavior later.
        try:
            BehaviorEnforcer.enforce(self.tool_name, self.behavior_config, None, None)
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, MockContext(), None
            )
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, None, {"param1": "a"}
            )
        except BehaviorViolationError:
            self.fail("Enforcement should pass when context or args are missing.")

    def test_enforce_no_new_params_provided(self):
        """Test enforcement passes if no *new* parameters are provided."""
        ctx = MockContext(collected_params={"param1"})
        # Providing only already collected param
        provided_args = {"param1": "new_value", "param2": None}
        try:
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, ctx, provided_args
            )
        except BehaviorViolationError as e:
            self.fail(
                f"Enforcement should pass when only old params are provided. Raised: {e}"
            )

    def test_enforce_correct_first_param(self):
        """Test enforcement passes when the correct first parameter is provided."""
        ctx = MockContext()
        provided_args = {"param1": "value1"}
        try:
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, ctx, provided_args
            )
        except BehaviorViolationError as e:
            self.fail(f"Enforcement failed for correct first param. Raised: {e}")

    def test_enforce_correct_second_param(self):
        """Test enforcement passes when the correct second parameter is provided."""
        ctx = MockContext(collected_params={"param1"})
        provided_args = {
            "param1": "value1",
            "param2": "value2",
        }  # param1 is old, param2 is new
        try:
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, ctx, provided_args
            )
        except BehaviorViolationError as e:
            self.fail(f"Enforcement failed for correct second param. Raised: {e}")

    def test_enforce_incorrect_first_param(self):
        """Test enforcement fails when the wrong first parameter is provided."""
        ctx = MockContext()
        provided_args = {"param2": "value2"}  # Should be param1
        with self.assertRaisesRegex(
            BehaviorViolationError,
            "Expected next: 'param1'. Got unexpected new parameter: 'param2'",
        ):
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, ctx, provided_args
            )

    def test_enforce_incorrect_second_param(self):
        """Test enforcement fails when the wrong second parameter is provided."""
        ctx = MockContext(collected_params={"param1"})
        provided_args = {"param1": "val1", "param3": "value3"}  # Should be param2
        with self.assertRaisesRegex(
            BehaviorViolationError,
            "Expected next: 'param2'. Got unexpected new parameter: 'param3'",
        ):
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, ctx, provided_args
            )

    def test_enforce_multiple_new_params_fails(self):
        """Test enforcement fails when multiple new parameters are provided at once."""
        ctx = MockContext()
        provided_args = {"param1": "value1", "param2": "value2"}  # Both are new
        # Adjust regex to match the more detailed error message
        expected_regex = (
            r"Tool 'test.tool' expects parameters sequentially. "
            r"Expected next: 'param1'. "
            # Use regex to handle potential set order variations {'param1', 'param2'} or {'param2', 'param1'}
            r"Provided multiple new parameters: {('param1', 'param2'|'param2', 'param1')}. "
            r"Collected so far: set\(\)."
        )
        with self.assertRaisesRegex(BehaviorViolationError, expected_regex):
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, ctx, provided_args
            )

    def test_enforce_multiple_new_params_later_fails(self):
        """Test enforcement fails when multiple new params are provided later in sequence."""
        ctx = MockContext(collected_params={"param1"})
        provided_args = {
            "param1": "v1",
            "param2": "value2",
            "param3": "value3",
        }  # param2 and param3 are new
        # Adjust regex to match the more detailed error message
        expected_regex = (
            r"Tool 'test.tool' expects parameters sequentially. "
            r"Expected next: 'param2'. "
            # Use regex to handle potential set order variations
            r"Provided multiple new parameters: {('param2', 'param3'|'param3', 'param2')}. "
            r"Collected so far: {'param1'}."
        )
        with self.assertRaisesRegex(BehaviorViolationError, expected_regex):
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, ctx, provided_args
            )

    def test_enforce_params_after_sequence_complete_passes(self):
        """Test enforcement passes when providing args after the sequence is complete."""
        ctx = MockContext(collected_params={"param1", "param2", "param3"})
        provided_args = {
            "param1": "v1",
            "param2": "v2",
            "param3": "v3",
            "optional_param": "opt",
        }
        try:
            BehaviorEnforcer.enforce(
                self.tool_name, self.behavior_config, ctx, provided_args
            )
        except BehaviorViolationError as e:
            self.fail(
                f"Enforcement should pass for args after sequence complete. Raised: {e}"
            )


# if __name__ == "__main__":
#     unittest.main()
