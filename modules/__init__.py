"""
Modules Package - Brain Module System v4.0
Main package containing core, ui, and utils modules
"""

from .core import Config, Installer, StatusChecker
from .ui import UIBuilder, themes
from .utils import (
    LogManager,
    is_admin,
    run_as_admin,
    add_to_system_path,
    add_to_path_immediate,
    PathOperations,
    RegistryOperations,
    BroadcastManager,
    PowerShellIntegration
)

__all__ = [
    # Core modules
    'Config',
    'Installer',
    'StatusChecker',
    # UI modules
    'UIBuilder',
    'themes',
    # Utils
    'LogManager',
    'is_admin',
    'run_as_admin',
    'add_to_system_path',
    'add_to_path_immediate',
    'PathOperations',
    'RegistryOperations',
    'BroadcastManager',
    'PowerShellIntegration'
]
