"""
PATH Repair Module for AI Setup Tool - Facade Pattern
Automatically detects and repairs PATH issues for installed tools
Brain Module System v4.0
"""

from typing import Callable, Optional

# Import from separated modules
from .repair_components.path_discovery import PathDiscovery, TOOL_PATHS
from .repair_components.path_registry import PathRegistry
from .repair_components.path_repair_core import PathRepairManager


# Re-export for backward compatibility
__all__ = [
    'PathRepairManager',
    'PathDiscovery',
    'PathRegistry',
    'TOOL_PATHS',
    'quick_path_repair'
]


# Convenience function for quick repair
def quick_path_repair(log_callback: Optional[Callable] = None) -> bool:
    """
    Quick function to diagnose and repair all PATH issues

    Args:
        log_callback: Optional callback for logging

    Returns:
        bool: True if all repairs successful
    """
    manager = PathRepairManager(log_callback)
    success, results = manager.auto_repair_all()
    return success