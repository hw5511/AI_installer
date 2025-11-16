"""
System Explorer Module
System-wide exploration and configuration reading
Brain Module System v4.0
"""

import os
import subprocess
import winreg
from typing import List, Dict, Any, Optional
from .checker_utils import _config


class SystemExplorer:
    """Explores system for installed tools and configurations"""

    def __init__(self, timeout: int = 5):
        """
        Initialize SystemExplorer

        Args:
            timeout: Default timeout for system operations in seconds
        """
        self.timeout = timeout

    def find_git_installations(self) -> List[Dict[str, Any]]:
        """
        Find all Git installations on the system

        Returns:
            List of dictionaries containing Git installation paths
            Each dictionary has: 'base', 'cmd', 'bin' keys
        """
        git_locations = []

        common_paths = [
            r"C:\Program Files\Git",
            r"C:\Program Files (x86)\Git",
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Git'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Programs', 'Git'),
        ]

        for base_path in common_paths:
            if os.path.exists(base_path):
                cmd_path = os.path.join(base_path, 'cmd')
                bin_path = os.path.join(base_path, 'bin')

                if os.path.exists(os.path.join(cmd_path, 'git.exe')):
                    git_locations.append({
                        'base': base_path,
                        'cmd': cmd_path,
                        'bin': bin_path if os.path.exists(bin_path) else None
                    })
                elif os.path.exists(os.path.join(bin_path, 'git.exe')):
                    git_locations.append({
                        'base': base_path,
                        'cmd': None,
                        'bin': bin_path
                    })

        # Search additional drives
        for drive in ['C:', 'D:', 'E:']:
            search_paths = [
                os.path.join(drive, 'Git'),
                os.path.join(drive, 'Program Files', 'Git'),
                os.path.join(drive, 'Program Files (x86)', 'Git'),
            ]
            for base_path in search_paths:
                if os.path.exists(base_path):
                    cmd_path = os.path.join(base_path, 'cmd')
                    bin_path = os.path.join(base_path, 'bin')

                    if (os.path.exists(os.path.join(cmd_path, 'git.exe')) or
                        os.path.exists(os.path.join(bin_path, 'git.exe'))):
                        if base_path not in [loc['base'] for loc in git_locations]:
                            git_locations.append({
                                'base': base_path,
                                'cmd': cmd_path if os.path.exists(os.path.join(cmd_path, 'git.exe')) else None,
                                'bin': bin_path if os.path.exists(os.path.join(bin_path, 'git.exe')) else None
                            })

        return git_locations

    def find_nodejs_installations(self) -> List[Dict[str, Any]]:
        """
        Find all Node.js installations on the system

        Returns:
            List of dictionaries containing Node.js installation paths
            Each dictionary has: 'base', 'node_exe', 'npm_cmd', 'npm_modules' keys
        """
        nodejs_locations = []

        common_paths = [
            r"C:\Program Files\nodejs",
            r"C:\Program Files (x86)\nodejs",
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'nodejs'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'nodejs'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'nodejs'),
            os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Programs', 'nodejs'),
        ]

        for base_path in common_paths:
            if os.path.exists(base_path):
                node_exe = os.path.join(base_path, 'node.exe')
                npm_cmd = os.path.join(base_path, 'npm.cmd')
                npm_cli = os.path.join(base_path, 'node_modules', 'npm')

                if os.path.exists(node_exe):
                    nodejs_locations.append({
                        'base': base_path,
                        'node_exe': node_exe,
                        'npm_cmd': npm_cmd if os.path.exists(npm_cmd) else None,
                        'npm_modules': npm_cli if os.path.exists(npm_cli) else None
                    })

        # Search additional drives
        for drive in ['C:', 'D:', 'E:']:
            search_paths = [
                os.path.join(drive, 'nodejs'),
                os.path.join(drive, 'Program Files', 'nodejs'),
                os.path.join(drive, 'Program Files (x86)', 'nodejs'),
            ]
            for base_path in search_paths:
                if os.path.exists(base_path):
                    node_exe = os.path.join(base_path, 'node.exe')
                    if os.path.exists(node_exe):
                        if base_path not in [loc['base'] for loc in nodejs_locations]:
                            nodejs_locations.append({
                                'base': base_path,
                                'node_exe': node_exe,
                                'npm_cmd': os.path.join(base_path, 'npm.cmd'),
                                'npm_modules': os.path.join(base_path, 'node_modules', 'npm')
                            })

        return nodejs_locations

    def get_system_path(self) -> List[str]:
        """
        Get system PATH environment variable from Windows registry

        Returns:
            List of paths in system PATH (lowercase)
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                0,
                winreg.KEY_READ
            )

            try:
                system_path, _ = winreg.QueryValueEx(key, 'Path')
                path_list = [p.strip().lower() for p in system_path.split(';') if p.strip()]
                return path_list
            except:
                return []
            finally:
                winreg.CloseKey(key)
        except:
            return []

    def get_user_path(self) -> List[str]:
        """
        Get user PATH environment variable from Windows registry

        Returns:
            List of paths in user PATH (lowercase)
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Environment',
                0,
                winreg.KEY_READ
            )

            try:
                user_path, _ = winreg.QueryValueEx(key, 'Path')
                path_list = [p.strip().lower() for p in user_path.split(';') if p.strip()]
                return path_list
            except:
                return []
            finally:
                winreg.CloseKey(key)
        except:
            return []

    def find_npm_global_packages(self) -> List[str]:
        """
        Get list of globally installed npm packages

        Returns:
            List of package names with versions
        """
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
                for line in lines[1:]:  # Skip first line
                    if 'tree──' in line or 'line──' in line:
                        package = line.replace('tree──', '').replace('line──', '').strip()
                        packages.append(package)
        except:
            pass
        return packages


class ConfigReader:
    """Reads configuration files from installed tools"""

    def __init__(self, timeout: int = 5):
        """
        Initialize ConfigReader

        Args:
            timeout: Default timeout for config operations in seconds
        """
        self.timeout = timeout

    def read_git_config(self) -> Dict[str, str]:
        """
        Get Git global configuration

        Returns:
            Dictionary of Git config key-value pairs
        """
        config = {}
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['git', 'config', '--global', '--list'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=self.timeout,
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

    def read_npm_config(self) -> Dict[str, str]:
        """
        Get npm configuration

        Returns:
            Dictionary of npm config key-value pairs
        """
        config = {}
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['npm', 'config', 'list'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=self.timeout,
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

    def get_npm_prefix(self) -> Optional[str]:
        """
        Get npm global installation prefix

        Returns:
            npm prefix path or None
        """
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['npm', 'config', 'get', 'prefix'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=self.timeout,
                creationflags=creationflags
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None


__all__ = ['SystemExplorer', 'ConfigReader']
