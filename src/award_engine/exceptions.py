"""
Custom exceptions for the Award Engine module.
"""


class AwardEngineError(Exception):
    """Base exception for all award engine errors."""
    pass


class InsufficientDataError(AwardEngineError):
    """Raised when there's insufficient data to generate a recommendation."""
    pass


class InvalidAwardeeInfoError(AwardEngineError):
    """Raised when awardee information is invalid or incomplete."""
    pass


class ScoringError(AwardEngineError):
    """Raised when there's an error during the scoring process."""
    pass


class ConfigurationError(AwardEngineError):
    """Raised when there's a configuration error."""
    pass