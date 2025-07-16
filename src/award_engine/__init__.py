"""
Coast Guard Award Engine Module

This module provides functionality for scoring achievements and recommending
appropriate Coast Guard awards based on various criteria.
"""

from .base import AwardEngine
from .exceptions import (
    AwardEngineError,
    InsufficientDataError,
    InvalidAwardeeInfoError,
    ScoringError
)

__all__ = [
    'AwardEngine',
    'AwardEngineError',
    'InsufficientDataError',
    'InvalidAwardeeInfoError',
    'ScoringError'
]