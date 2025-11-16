"""
Path Discovery Module
Tool installation path discovery and verification
Brain Module System v4.0
"""

import os
import subprocess
from typing import List, Callable, Optional

# Import Config for production mode detection
try:
    from modules.core.config import Config
    _config = Config()
except ImportError:
    _config = None


# Known installation paths for each tool
TOOL_PATHS = {
    'git': [
        r"C:\Program Files\Git\cmd",
        r"C:\Program Files\Git\bin",
        r"C:\Program Files (x86)\Git\cmd",
        r"C:\Program Files (x86)\Git\bin",
        r"C:\Git\cmd",
        r"C:\Git\bin",
        # Chocolatey installation path
        r"C:\ProgramData\chocolatey\lib\git.install\tools\cmd",
        r"C:\ProgramData\chocolatey\lib\git.install\tools\bin"
    ],
    'nodejs': [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        r"C:\nodejs",
        # Chocolatey installation path
        r"C:\ProgramData\chocolatey\lib\nodejs\tools",
        r"C:\ProgramData\chocolatey\lib\nodejs.install\tools"
    ],
    'npm': [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        r"C:\Users\%USERNAME%\AppData\Roaming\npm",
        r"C:\ProgramData\npm"
    ]
}


class PathDiscovery:
    """Handles tool path discovery and verification"""

    def __init__(self, log_callback: Optional[Callable] = None):
        """Initialize path discovery with optional logging callback"""
        self.log_callback = log_callback
        self.tool_paths = TOOL_PATHS

    def _log(self, message: str, level: str = "INFO"):
        """Log a message"""
        if self.log_callback:
            self.log_callback(f"[{level}] {message}")
        else:
            print(f"[{level}] {message}")

    def _expand_path(self, path: str) -> str:
        """Expand environment variables in path"""
        return os.path.expandvars(os.path.expanduser(path))

    def check_tool_in_path(self, tool_name: str) -> bool:
        """
        Check if a tool is accessible in PATH

        Args:
            tool_name: Name of the tool (e.g., 'git', 'node', 'npm')

        Returns:
            bool: True if tool is accessible
        """
        try:
            # Try to run the tool with --version
            cmd = f"{tool_name} --version"
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=creationflags
            )
            return result.returncode == 0
        except Exception:
            return False

    def find_tool_installation(self, tool_name: str) -> List[str]:
        """
        Find actual installation paths for a tool

        Args:
            tool_name: Name of the tool ('git', 'nodejs', 'npm')

        Returns:
            List of valid installation paths found
        """
        found_paths = []

        if tool_name not in self.tool_paths:
            self._log(f"알 수 없는 도구: {tool_name}", "WARNING")
            return found_paths

        # Check each possible path
        for path in self.tool_paths[tool_name]:
            expanded_path = self._expand_path(path)

            # Check if directory exists
            if os.path.exists(expanded_path):
                # Verify tool executable exists in the path
                if tool_name == 'git':
                    exe_path = os.path.join(expanded_path, 'git.exe')
                elif tool_name == 'nodejs':
                    exe_path = os.path.join(expanded_path, 'node.exe')
                elif tool_name == 'npm':
                    exe_path = os.path.join(expanded_path, 'npm.cmd')
                    if not os.path.exists(exe_path):
                        exe_path = os.path.join(expanded_path, 'npm.exe')
                else:
                    continue

                if os.path.exists(exe_path):
                    found_paths.append(expanded_path)
                    self._log(f"{tool_name}을(를) 다음 위치에서 찾았습니다: {expanded_path}", "DEBUG")

        return found_paths


__all__ = ['PathDiscovery', 'TOOL_PATHS']
