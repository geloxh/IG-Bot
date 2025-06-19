"""
Instagram Bot Package

A professional Instagram automation tool with intelligent engagement,
analytics, and safety features.

Author: Instagram Bot Project
Version: 1.0.0
"""

from .instagram_bot import InstagramBot
from .engagement import EngagementStrategy
from .analytics import AnalyticsManager
from .utils import ConfigManager, Logger, RateLimiter

__version__ = "1.0.0"
__author__ = "Instagram Bot Project"

__all__ = [
    'InstagramBot',
    'EngagementStrategy', 
    'AnalyticsManager',
    'ConfigManager',
    'Logger',
    'RateLimiter'
]