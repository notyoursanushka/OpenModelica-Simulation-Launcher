"""
test_validators.py
------------------
Unit tests for the validators module.
"""

import pytest
from app.validators import validate_times


class TestValidateTimes:
    """Tests for validate_times function."""

    def test_valid_inputs(self):
        """Valid start and stop times should pass."""
        is_valid, msg = validate_times("0", "3")
        assert is_valid is True
        assert msg == ""

    def test_valid_boundary(self):
        """Start=0, Stop=4 is the maximum valid range."""
        is_valid, msg = validate_times("0", "4")
        assert is_valid is True

    def test_non_integer_start(self):
        """Non-integer start time should fail."""
        is_valid, msg = validate_times("abc", "3")
        assert is_valid is False
        assert "integers" in msg.lower()

    def test_non_integer_stop(self):
        """Non-integer stop time should fail."""
        is_valid, msg = validate_times("0", "xyz")
        assert is_valid is False

    def test_negative_start(self):
        """Negative start time should fail."""
        is_valid, msg = validate_times("-1", "3")
        assert is_valid is False
        assert ">= 0" in msg

    def test_stop_equal_to_5(self):
        """Stop time equal to 5 should fail."""
        is_valid, msg = validate_times("0", "5")
        assert is_valid is False
        assert "< 5" in msg

    def test_stop_greater_than_5(self):
        """Stop time greater than 5 should fail."""
        is_valid, msg = validate_times("0", "10")
        assert is_valid is False

    def test_start_equal_to_stop(self):
        """Start equal to stop should fail."""
        is_valid, msg = validate_times("2", "2")
        assert is_valid is False
        assert "less than" in msg.lower()

    def test_start_greater_than_stop(self):
        """Start greater than stop should fail."""
        is_valid, msg = validate_times("3", "1")
        assert is_valid is False

    def test_float_inputs(self):
        """Float inputs should fail as not integers."""
        is_valid, msg = validate_times("1.5", "3.5")
        assert is_valid is False