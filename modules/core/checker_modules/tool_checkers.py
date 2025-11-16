"""
Tool-specific checkers (Git, Node.js, Package Managers)
Brain Module System v4.0
"""

import subprocess
import os
from typing import Optional, Dict, Any
from .checker_utils import _config


class GitChecker:
    """Git installation checker"""

    def __init__(self, config=None):
        from modules.core.config import Config
        self.config = config or Config()

    def is_installed(self) -> bool:
        """Check if Git is installed"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags
            )
            return result.returncode == 0
        except:
            return False

    def get_version(self) -> Optional[str]:
        """Get Git version"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags
            )
            if result.returncode == 0:
                return result.stdout.strip().replace('git version ', '')
            return None
        except:
            return None

    def get_config(self) -> Dict[str, str]:
        """Get Git global configuration"""
        config = {}
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['git', 'config', '--global', '--list'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5,
                creationflags=creationflags
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value
        except:
            pass
        return config


class NodeJsChecker:
    """Node.js installation checker"""

    def __init__(self, config=None):
        from modules.core.config import Config
        self.config = config or Config()

    def is_installed(self) -> bool:
        """Check if Node.js is installed"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags
            )
            return result.returncode == 0
        except:
            return False

    def get_version(self) -> Optional[str]:
        """Get Node.js version"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None


class PackageManagerChecker:
    """Package manager checker (npm, Chocolatey, Winget)"""

    def __init__(self, config=None):
        from modules.core.config import Config
        self.config = config or Config()

    def is_npm_installed(self) -> bool:
        """Check if npm is installed"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['npm', '--version'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=timeout,
                creationflags=creationflags
            )
            return result.returncode == 0
        except:
            return False

    def get_npm_version(self) -> Optional[str]:
        """Get npm version"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['npm', '--version'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=timeout,
                creationflags=creationflags
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None

    def get_npm_config(self) -> Dict[str, str]:
        """Get npm configuration"""
        config = {}
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['npm', 'config', 'list'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5,
                creationflags=creationflags
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if '=' in line and not line.startswith(';'):
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except:
            pass
        return config

    def get_npm_global_packages(self):
        """Get globally installed npm packages"""
        packages = []
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['npm', 'list', '-g', '--depth=0'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=10,
                creationflags=creationflags
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines[1:]:
                    if 'tree──' in line or 'line──' in line:
                        package = line.replace('tree──', '').replace('line──', '').strip()
                        packages.append(package)
        except:
            pass
        return packages

    def is_chocolatey_installed(self) -> bool:
        """Check if Chocolatey is installed"""
        choco_paths = [
            r'C:\ProgramData\chocolatey\bin\choco.exe',
            r'C:\ProgramData\chocolatey\choco.exe',
        ]

        for path in choco_paths:
            if os.path.exists(path):
                return True

        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['choco', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=True,
                creationflags=creationflags
            )
            return result.returncode == 0
        except:
            return False

    def get_chocolatey_version(self) -> Optional[str]:
        """Get Chocolatey version"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['choco', '--version'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=timeout,
                creationflags=creationflags
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None

    def is_winget_installed(self) -> bool:
        """Check if Winget is installed"""
        from .checker_utils import check_command_exists
        exists, _ = check_command_exists('winget --version')
        return exists

    def get_winget_version(self) -> Optional[str]:
        """Get Winget version"""
        from .checker_utils import check_command_exists
        exists, version = check_command_exists('winget --version')
        return version if exists else None


class PythonChecker:
    """Python installation checker"""

    def __init__(self, config=None):
        from modules.core.config import Config
        self.config = config or Config()

    def is_installed(self) -> bool:
        """Check if Python is installed"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['python', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags
            )
            return result.returncode == 0
        except:
            return False

    def get_version(self) -> Optional[str]:
        """Get Python version"""
        try:
            timeout = self.config.get_timeout('command_check')
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['python', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags
            )
            if result.returncode == 0:
                return result.stdout.strip().replace('Python ', '')
            return None
        except:
            return None
