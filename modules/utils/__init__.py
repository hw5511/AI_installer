"""
Utils Module Package for AI Setup Application
Provides system utilities, path management, and logging functionality
"""

# Import key classes and functions for easy access
from .logger import LogManager
from .system_utils import (
    is_admin, run_as_admin, restart_as_admin,
    check_software_installed, check_package_manager,
    run_command_with_timeout, check_multiple_software_installations,
    find_executable_in_common_paths, search_drives_for_executable,
    ensure_directory_exists, get_windows_version
)
from .path_manager import (
    # Basic functions
    add_to_system_path, add_multiple_paths_to_system_path,
    get_system_path_from_registry, get_user_path_from_registry,
    refresh_environment_variables, broadcast_environment_change,
    set_environment_variable, check_path_in_environment,
    # Enhanced functions
    add_to_path_immediate, check_and_set_powershell_execution_policy,
    # Classes
    PathOperations, RegistryOperations, BroadcastManager, PowerShellIntegration
)

__all__ = [
    # Logger
    'LogManager',

    # System utilities
    'is_admin', 'run_as_admin', 'restart_as_admin',
    'check_software_installed', 'check_package_manager',
    'run_command_with_timeout', 'check_multiple_software_installations',
    'find_executable_in_common_paths', 'search_drives_for_executable',
    'ensure_directory_exists', 'get_windows_version',

    # Path management (basic)
    'add_to_system_path', 'add_multiple_paths_to_system_path',
    'get_system_path_from_registry', 'get_user_path_from_registry',
    'refresh_environment_variables', 'broadcast_environment_change',
    'set_environment_variable', 'check_path_in_environment',

    # Path management (enhanced)
    'add_to_path_immediate', 'check_and_set_powershell_execution_policy',

    # Path management (classes)
    'PathOperations', 'RegistryOperations', 'BroadcastManager', 'PowerShellIntegration'
]