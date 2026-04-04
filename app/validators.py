"""
validators.py
-------------
Utility functions for validating simulation parameters.
"""


def validate_times(start_time: str, stop_time: str) -> tuple:
    """
    Validate start and stop time inputs.

    Rules:
        - Both must be integers
        - 0 <= start_time < stop_time < 5

    Args:
        start_time: Raw string from the start time input field.
        stop_time:  Raw string from the stop time input field.

    Returns:
        (is_valid: bool, error_message: str)
    """
    # Check they are integers
    try:
        start = int(start_time)
        stop = int(stop_time)
    except ValueError:
        return False, "Start time and Stop time must be integers."

    # Check start is not negative
    if start < 0:
        return False, "Start time must be >= 0."

    # Check stop is less than 5
    if stop >= 5:
        return False, "Stop time must be < 5."

    # Check start is less than stop
    if start >= stop:
        return False, "Start time must be less than Stop time."

    return True, ""