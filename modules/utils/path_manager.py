"""
PATH Manager Module - Facade Pattern
Unified PATH management with basic/enhanced modes
Brain Module System v4.0
"""

from typing import List, Optional, Dict
from .path_operations.registry_operations import RegistryOperations
from .path_operations.broadcast_manager import BroadcastManager
from .path_operations.powershell_integration import PowerShellIntegration
from .path_operations.path_operations import PathOperations


# Backward compatibility functions - re-export from PathOperations

def add_to_system_path(path: str) -> bool:
    """Add to system PATH - basic mode"""
    ops = PathOperations()
    return ops.add_to_system_path(path)


def add_multiple_paths_to_system_path(new_paths: List[str]) -> bool:
    """Add multiple paths to system PATH"""
    ops = PathOperations()
    return ops.add_multiple_paths_to_system_path(new_paths)


def add_to_path_immediate(paths) -> bool:
    """Add to PATH with immediate effect - enhanced mode"""
    ops = PathOperations()
    return ops.add_to_path_immediate(paths)


def add_to_user_path_immediate(paths) -> bool:
    """Add to user PATH with immediate effect - enhanced mode"""
    ops = PathOperations()
    return ops.add_to_user_path_immediate(paths)


def remove_from_system_path(path: str) -> bool:
    """Remove from system PATH"""
    ops = PathOperations()
    return ops.remove_from_path(path)


def get_system_path_from_registry() -> List[str]:
    """Get current system PATH"""
    ops = PathOperations()
    return ops.get_current_path()


def get_user_path_from_registry() -> List[str]:
    """Get current user PATH"""
    reg_ops = RegistryOperations()
    return reg_ops.read_user_path()


def refresh_environment_variables() -> bool:
    """Refresh environment variables for current process"""
    ops = PathOperations()
    return ops.refresh_environment_variables()


def broadcast_environment_change() -> bool:
    """Broadcast environment variable changes to the system"""
    broadcast_mgr = BroadcastManager()
    return broadcast_mgr.broadcast_environment_change()


def check_path_in_environment(target_path: str, case_sensitive: bool = False) -> Dict:
    """Check if a path exists in environment PATH"""
    ops = PathOperations()
    return ops.check_path_in_environment(target_path, case_sensitive)


def set_environment_variable(name: str, value: str, user: bool = False) -> bool:
    """Set an environment variable in the registry"""
    reg_ops = RegistryOperations()
    if reg_ops.write_environment_variable(name, value, user):
        broadcast_mgr = BroadcastManager()
        broadcast_mgr.broadcast_environment_change()
        return True
    return False


def check_and_set_powershell_execution_policy() -> bool:
    """Check and set PowerShell execution policy to RemoteSigned if needed"""
    powershell = PowerShellIntegration()
    return powershell.ensure_execution_policy()


# Export all for backward compatibility
__all__ = [
    # Classes
    'PathOperations',
    'RegistryOperations',
    'BroadcastManager',
    'PowerShellIntegration',

    # Basic functions
    'add_to_system_path',
    'add_multiple_paths_to_system_path',
    'get_system_path_from_registry',
    'get_user_path_from_registry',
    'refresh_environment_variables',
    'broadcast_environment_change',
    'set_environment_variable',
    'check_path_in_environment',

    # Enhanced functions
    'add_to_path_immediate',
    'add_to_user_path_immediate',
    'check_and_set_powershell_execution_policy',
]
