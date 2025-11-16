"""
Registry Checker Module
Windows registry PATH verification
Brain Module System v4.0
"""

import winreg
import os
from typing import List, Dict, Tuple, Optional


class RegistryChecker:
    """Checks PATH in Windows registry"""

    def __init__(self, log_callback=None):
        """
        Initialize the registry checker

        Args:
            log_callback: Optional callback for logging
        """
        self.log_callback = log_callback

    def log(self, message: str):
        """Log a message"""
        if self.log_callback:
            self.log_callback(message)

    def expand_env_vars(self, path: str) -> str:
        """
        환경변수를 실제 경로로 확장합니다.

        Args:
            path: 확장할 경로 (예: "%APPDATA%\\npm")

        Returns:
            확장된 경로 (예: "C:\\Users\\username\\AppData\\Roaming\\npm")
        """
        expanded = os.path.expandvars(path)
        self.log(f"환경변수 확장: {path} → {expanded}")
        return expanded.lower()

    def get_machine_path(self) -> List[str]:
        """
        Get Machine-level PATH from registry

        Returns:
            list: List of machine-level PATH entries
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                0,
                winreg.KEY_READ
            )
            machine_path, _ = winreg.QueryValueEx(key, 'PATH')
            winreg.CloseKey(key)
            # 각 경로에 대해 환경변수 확장 적용
            expanded_paths = []
            for p in machine_path.split(';'):
                if p.strip():
                    expanded = self.expand_env_vars(p.strip())
                    expanded_paths.append(expanded)
            return expanded_paths
        except Exception as e:
            self.log(f"Warning: Could not read Machine PATH from registry: {e}")
            return []

    def get_user_path(self) -> List[str]:
        """
        Get User-level PATH from registry

        Returns:
            list: List of user-level PATH entries
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Environment',
                0,
                winreg.KEY_READ
            )
            user_path, _ = winreg.QueryValueEx(key, 'PATH')
            winreg.CloseKey(key)
            # 각 경로에 대해 환경변수 확장 적용
            expanded_paths = []
            for p in user_path.split(';'):
                if p.strip():
                    expanded = self.expand_env_vars(p.strip())
                    expanded_paths.append(expanded)
            return expanded_paths
        except Exception:
            # User PATH might not exist, which is OK
            return []

    def get_registry_paths(self) -> Dict[str, List[str]]:
        """
        Get PATH entries directly from Windows Registry

        Returns:
            dict: Machine and User PATH entries from registry
        """
        return {
            'Machine': self.get_machine_path(),
            'User': self.get_user_path()
        }

    def check_executable_exists(self, tool_name: str, paths: List[str]) -> Tuple[bool, Optional[str]]:
        """
        Check if executable exists in given paths

        Args:
            tool_name: Name of the executable to find
            paths: List of directory paths to search

        Returns:
            tuple: (found, executable_path)
        """
        for path_dir in paths:
            if os.path.isdir(path_dir):
                # Check for common executable extensions on Windows
                for ext in ['', '.exe', '.cmd', '.bat']:
                    exe_path = os.path.join(path_dir, tool_name + ext)
                    if os.path.isfile(exe_path):
                        return True, exe_path
        return False, None

    def find_tool_paths(self, expected_paths: List[str], registry_paths: List[str]) -> List[str]:
        """
        Find paths that match expected patterns

        Args:
            expected_paths: List of expected path patterns
            registry_paths: List of actual registry PATH entries

        Returns:
            list: Matching paths
        """
        found_paths = []
        for registry_path in registry_paths:
            for expected in expected_paths:
                if expected.lower() in registry_path.lower():
                    found_paths.append(registry_path)
        return found_paths

    def check_tool_in_registry(self, tool_name: str, command_info: Dict) -> Dict:
        """
        Check if tool exists in registry PATH

        Args:
            tool_name: Name of the tool
            command_info: Tool config with 'command' and 'expected_paths'

        Returns:
            {
                'tool': str,
                'in_registry': bool,
                'found_paths': List[str],
                'executable_found': bool,
                'executable_path': str or None,
                'machine_paths': List[str],
                'user_paths': List[str]
            }
        """
        registry_paths = self.get_registry_paths()
        all_paths = registry_paths['Machine'] + registry_paths['User']

        expected_paths = command_info.get('expected_paths', [])
        found_paths = self.find_tool_paths(expected_paths, all_paths)

        # Check for executable file
        command = command_info['command']
        executable_found, executable_path = self.check_executable_exists(command, all_paths)

        return {
            'tool': tool_name,
            'in_registry': len(found_paths) > 0 or executable_found,
            'found_paths': found_paths,
            'executable_found': executable_found,
            'executable_path': executable_path,
            'machine_paths': registry_paths['Machine'],
            'user_paths': registry_paths['User']
        }


__all__ = ['RegistryChecker']
