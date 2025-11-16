"""
CLI Checkers Module
Status checkers for AI CLI tools
Brain Module System v4.0
"""

import subprocess
import os
import winreg
from typing import Optional
from .checker_utils import check_command_exists, _config


class ClaudeCliChecker:
    """
    Claude CLI installation status checker

    Provides comprehensive installation detection with multiple fallback methods:
    - npm global package directory check
    - User local binary directory check
    - Windows 'where' command lookup
    - Direct version command execution

    Attributes:
        None

    Methods:
        is_installed(): Check if Claude CLI is installed
        get_version(): Get the installed Claude CLI version
        _check_npm_global_install(): Check npm global directory
        _check_local_bin_install(): Check user's .local/bin directory
        _check_where_command(): Use Windows 'where' command
        _check_version_command(): Try 'claude --version' command
    """

    def __init__(self):
        """Initialize Claude CLI checker"""
        self._verbose = False  # Enable for detailed logging

    def _log(self, message: str):
        """Log message if verbose mode is enabled"""
        if self._verbose:
            print(f"[ClaudeCliChecker] {message}")

    def is_installed(self) -> bool:
        """
        Check if Claude CLI is installed with 3-stage verification

        Verification stages:
        1. File existence check (npm global or .local/bin)
        2. User PATH registry check
        3. Execution test in new process

        Returns:
            bool: True if all three stages pass, False otherwise

        Examples:
            >>> checker = ClaudeCliChecker()
            >>> if checker.is_installed():
            ...     print("Claude CLI is installed")

        Note:
            All three stages must pass for complete verification
        """
        # Stage 1: File existence check
        file_exists = self._check_file_exists()

        # Stage 2: User PATH registry check
        in_user_path = self._check_user_path()

        # Stage 3: Execution test
        execution_success = self._check_execution()

        # Log results
        self._log("Claude CLI verification results:")
        self._log(f"  File exists: {file_exists}")
        self._log(f"  In User PATH: {in_user_path}")
        self._log(f"  Execution success: {execution_success}")

        # All three must pass
        result = file_exists and in_user_path and execution_success

        if not result:
            self._log("[WARNING] Claude CLI verification failed")

        return result

    def _check_file_exists(self) -> bool:
        """
        Stage 1: Check if Claude CLI files exist

        Checks multiple locations:
        - npm global directory
        - User's .local/bin directory

        Returns:
            bool: True if files exist, False otherwise
        """
        # Check npm global directory
        if self._check_npm_global_install():
            self._log("Claude CLI found in npm global directory")
            return True

        # Check user's .local/bin
        if self._check_local_bin_install():
            self._log("Claude CLI found in .local/bin directory")
            return True

        self._log("Claude CLI files not found")
        return False

    def _check_user_path(self) -> bool:
        """
        Stage 2: Check if npm path is in User PATH registry

        Verifies that the npm prefix is properly registered in the
        Windows User PATH environment variable (HKEY_CURRENT_USER).

        Returns:
            bool: True if npm path is in User PATH, False otherwise

        Note:
            - Reads from HKEY_CURRENT_USER\\Environment
            - Uses case-insensitive comparison
            - Handles both exact matches and partial path matches
        """
        try:
            # Get npm prefix
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['npm', 'config', 'get', 'prefix'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=10,
                creationflags=creationflags
            )

            if result.returncode != 0:
                self._log("npm config get prefix failed")
                return False

            npm_prefix = result.stdout.strip().lower()
            self._log(f"npm prefix: {npm_prefix}")

            # Read User PATH from registry
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Environment',
                0,
                winreg.KEY_READ
            )

            try:
                user_path, _ = winreg.QueryValueEx(key, 'Path')
                user_path_list = [p.strip().lower() for p in user_path.split(';') if p.strip()]

                self._log(f"User PATH entries: {len(user_path_list)}")

                # Check if npm prefix is in User PATH
                in_user_path = any(npm_prefix in p or p in npm_prefix for p in user_path_list)

                self._log(f"npm path in User PATH: {in_user_path}")

                if not in_user_path:
                    self._log("[WARNING] npm prefix not found in User PATH registry")
                    self._log(f"  Expected: {npm_prefix}")

                return in_user_path

            finally:
                winreg.CloseKey(key)

        except Exception as e:
            self._log(f"Error checking User PATH: {str(e)}")
            return False

    def _check_execution(self) -> bool:
        """
        Stage 3: Test execution in new process

        Attempts to execute Claude CLI commands to verify it's
        functional and accessible from a new process.

        Returns:
            bool: True if execution succeeds, False otherwise
        """
        # Try 'where' command first (fast)
        if self._check_where_command():
            self._log("Claude CLI found via 'where' command")
            return True

        # Try 'claude --version' as fallback
        if self._check_version_command():
            self._log("Claude CLI executed successfully")
            return True

        self._log("Claude CLI execution tests failed")
        return False

    def _check_npm_global_install(self) -> bool:
        """
        Check if Claude CLI is installed in npm global directory

        This method queries npm's global prefix and checks for the presence of
        claude executables (cmd, exe, or ps1) in that directory.

        Returns:
            bool: True if found in npm global directory, False otherwise

        Note:
            - Requires npm to be installed
            - Timeout is set to 5 seconds
            - Checks for .cmd, .exe, and .ps1 variants
        """
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            npm_prefix = subprocess.run(
                ['npm', 'config', 'get', 'prefix'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5,
                creationflags=creationflags
            ).stdout.strip()

            if npm_prefix:
                # Check all possible locations on Windows
                claude_cmd = os.path.join(npm_prefix, 'claude.cmd')
                claude_exe = os.path.join(npm_prefix, 'claude.exe')
                claude_ps1 = os.path.join(npm_prefix, 'claude.ps1')

                if os.path.exists(claude_cmd) or os.path.exists(claude_exe) or os.path.exists(claude_ps1):
                    return True
        except Exception:
            pass

        return False

    def _check_local_bin_install(self) -> bool:
        """
        Check if Claude CLI is installed in user's .local/bin directory

        This method checks the user's home directory for a native installation
        in the standard Unix-style .local/bin location.

        Returns:
            bool: True if found in .local/bin, False otherwise

        Note:
            - Checks for claude.exe in ~/.local/bin
            - Common for native/manual installations
        """
        try:
            user_home = os.path.expanduser("~")
            local_claude = os.path.join(user_home, '.local', 'bin', 'claude.exe')
            if os.path.exists(local_claude):
                return True
        except Exception:
            pass

        return False

    def _check_where_command(self) -> bool:
        """
        Use Windows 'where' command to find claude executable

        The 'where' command searches the PATH environment variable for the
        specified executable. This is useful for detecting installations
        that have been added to the system PATH.

        Returns:
            bool: True if 'where' command finds claude, False otherwise

        Note:
            - Only runs on Windows (os.name == 'nt')
            - Timeout is set to 5 seconds
            - Requires claude to be in PATH
        """
        try:
            # Use where command on Windows to find claude
            if os.name == 'nt':
                creationflags = _config.get_subprocess_flags() if _config else 0
                where_result = subprocess.run(
                    ['where', 'claude'],
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=5,
                    creationflags=creationflags
                )
                if where_result.returncode == 0:
                    return True
        except Exception:
            pass

        return False

    def _check_version_command(self) -> bool:
        """
        Try running 'claude --version' command

        This is the most direct method to check if Claude CLI is installed
        and functional. It attempts to execute the version command with an
        extended timeout to accommodate slower systems.

        Returns:
            bool: True if version command succeeds, False otherwise

        Note:
            - Extended timeout of 15 seconds for slower systems
            - May return False on timeout even if installed
            - Most reliable method if succeeds
        """
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=15,  # Increased timeout for slower systems
                creationflags=creationflags
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            # Claude might be installed but slow to respond
            return False
        except Exception:
            return False

    def get_version(self) -> Optional[str]:
        """
        Get Claude CLI version with extended timeout

        Attempts to retrieve the version string by running 'claude --version'.
        Returns a special message if the command times out but Claude is installed.

        Returns:
            Optional[str]: Version string, timeout message, or None if not installed

        Examples:
            >>> checker = ClaudeCliChecker()
            >>> version = checker.get_version()
            >>> if version:
            ...     print(f"Claude CLI version: {version}")

        Note:
            - Timeout is set to 10 seconds
            - Returns Korean message on timeout
            - Returns None if command fails
        """
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=10,  # Claude CLI specific timeout
                creationflags=creationflags
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except subprocess.TimeoutExpired:
            return "설치됨 (버전 확인 시간 초과)"
        except Exception:
            return None


class GeminiCliChecker:
    """
    Gemini CLI installation status checker

    Provides comprehensive installation detection with multiple fallback methods:
    - npm global package directory check
    - User local binary directory check
    - Windows 'where' command lookup
    - Direct version command execution

    Attributes:
        None

    Methods:
        is_installed(): Check if Gemini CLI is installed
        get_version(): Get the installed Gemini CLI version
        _check_npm_global_install(): Check npm global directory
        _check_local_bin_install(): Check user's .local/bin directory
        _check_where_command(): Use Windows 'where' command
        _check_version_command(): Try 'gemini --version' command
    """

    def __init__(self):
        """Initialize Gemini CLI checker"""
        self._verbose = False  # Enable for detailed logging

    def _log(self, message: str):
        """Log message if verbose mode is enabled"""
        if self._verbose:
            print(f"[GeminiCliChecker] {message}")

    def is_installed(self) -> bool:
        """
        Check if Gemini CLI is installed with 3-stage verification

        Verification stages:
        1. File existence check (npm global or .local/bin)
        2. User PATH registry check
        3. Execution test in new process

        Returns:
            bool: True if all three stages pass, False otherwise

        Examples:
            >>> checker = GeminiCliChecker()
            >>> if checker.is_installed():
            ...     print("Gemini CLI is installed")

        Note:
            All three stages must pass for complete verification
        """
        # Stage 1: File existence check
        file_exists = self._check_file_exists()

        # Stage 2: User PATH registry check
        in_user_path = self._check_user_path()

        # Stage 3: Execution test
        execution_success = self._check_execution()

        # Log results
        self._log("Gemini CLI verification results:")
        self._log(f"  File exists: {file_exists}")
        self._log(f"  In User PATH: {in_user_path}")
        self._log(f"  Execution success: {execution_success}")

        # All three must pass
        result = file_exists and in_user_path and execution_success

        if not result:
            self._log("[WARNING] Gemini CLI verification failed")

        return result

    def _check_file_exists(self) -> bool:
        """
        Stage 1: Check if Gemini CLI files exist

        Checks multiple locations:
        - npm global directory
        - User's .local/bin directory

        Returns:
            bool: True if files exist, False otherwise
        """
        # Check npm global directory
        if self._check_npm_global_install():
            self._log("Gemini CLI found in npm global directory")
            return True

        # Check user's .local/bin
        if self._check_local_bin_install():
            self._log("Gemini CLI found in .local/bin directory")
            return True

        self._log("Gemini CLI files not found")
        return False

    def _check_user_path(self) -> bool:
        """
        Stage 2: Check if npm path is in User PATH registry

        Verifies that the npm prefix is properly registered in the
        Windows User PATH environment variable (HKEY_CURRENT_USER).

        Returns:
            bool: True if npm path is in User PATH, False otherwise

        Note:
            - Reads from HKEY_CURRENT_USER\\Environment
            - Uses case-insensitive comparison
            - Handles both exact matches and partial path matches
        """
        try:
            # Get npm prefix
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['npm', 'config', 'get', 'prefix'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=10,
                creationflags=creationflags
            )

            if result.returncode != 0:
                self._log("npm config get prefix failed")
                return False

            npm_prefix = result.stdout.strip().lower()
            self._log(f"npm prefix: {npm_prefix}")

            # Read User PATH from registry
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Environment',
                0,
                winreg.KEY_READ
            )

            try:
                user_path, _ = winreg.QueryValueEx(key, 'Path')
                user_path_list = [p.strip().lower() for p in user_path.split(';') if p.strip()]

                self._log(f"User PATH entries: {len(user_path_list)}")

                # Check if npm prefix is in User PATH
                in_user_path = any(npm_prefix in p or p in npm_prefix for p in user_path_list)

                self._log(f"npm path in User PATH: {in_user_path}")

                if not in_user_path:
                    self._log("[WARNING] npm prefix not found in User PATH registry")
                    self._log(f"  Expected: {npm_prefix}")

                return in_user_path

            finally:
                winreg.CloseKey(key)

        except Exception as e:
            self._log(f"Error checking User PATH: {str(e)}")
            return False

    def _check_execution(self) -> bool:
        """
        Stage 3: Test execution in new process

        Attempts to execute Gemini CLI commands to verify it's
        functional and accessible from a new process.

        Returns:
            bool: True if execution succeeds, False otherwise
        """
        # Try 'where' command first (fast)
        if self._check_where_command():
            self._log("Gemini CLI found via 'where' command")
            return True

        # Try 'gemini --version' as fallback
        if self._check_version_command():
            self._log("Gemini CLI executed successfully")
            return True

        self._log("Gemini CLI execution tests failed")
        return False

    def _check_npm_global_install(self) -> bool:
        """
        Check if Gemini CLI is installed in npm global directory

        This method queries npm's global prefix and checks for the presence of
        gemini executables (cmd, exe, or ps1) in that directory.

        Returns:
            bool: True if found in npm global directory, False otherwise

        Note:
            - Requires npm to be installed
            - Timeout is set to 5 seconds
            - Checks for .cmd, .exe, and .ps1 variants
        """
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            npm_prefix = subprocess.run(
                ['npm', 'config', 'get', 'prefix'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=5,
                creationflags=creationflags
            ).stdout.strip()

            if npm_prefix:
                # Check all possible locations on Windows
                gemini_cmd = os.path.join(npm_prefix, 'gemini.cmd')
                gemini_exe = os.path.join(npm_prefix, 'gemini.exe')
                gemini_ps1 = os.path.join(npm_prefix, 'gemini.ps1')

                if os.path.exists(gemini_cmd) or os.path.exists(gemini_exe) or os.path.exists(gemini_ps1):
                    return True
        except Exception:
            pass

        return False

    def _check_local_bin_install(self) -> bool:
        """
        Check if Gemini CLI is installed in user's .local/bin directory

        This method checks the user's home directory for a native installation
        in the standard Unix-style .local/bin location.

        Returns:
            bool: True if found in .local/bin, False otherwise

        Note:
            - Checks for gemini.exe in ~/.local/bin
            - Common for native/manual installations
        """
        try:
            user_home = os.path.expanduser("~")
            local_gemini = os.path.join(user_home, '.local', 'bin', 'gemini.exe')
            if os.path.exists(local_gemini):
                return True
        except Exception:
            pass

        return False

    def _check_where_command(self) -> bool:
        """
        Use Windows 'where' command to find gemini executable

        The 'where' command searches the PATH environment variable for the
        specified executable. This is useful for detecting installations
        that have been added to the system PATH.

        Returns:
            bool: True if 'where' command finds gemini, False otherwise

        Note:
            - Only runs on Windows (os.name == 'nt')
            - Timeout is set to 5 seconds
            - Requires gemini to be in PATH
        """
        try:
            # Use where command on Windows to find gemini
            if os.name == 'nt':
                creationflags = _config.get_subprocess_flags() if _config else 0
                where_result = subprocess.run(
                    ['where', 'gemini'],
                    capture_output=True,
                    text=True,
                    shell=True,
                    timeout=5,
                    creationflags=creationflags
                )
                if where_result.returncode == 0:
                    return True
        except Exception:
            pass

        return False

    def _check_version_command(self) -> bool:
        """
        Try running 'gemini --version' command

        This is the most direct method to check if Gemini CLI is installed
        and functional. It attempts to execute the version command with an
        extended timeout to accommodate slower systems.

        Returns:
            bool: True if version command succeeds, False otherwise

        Note:
            - Extended timeout of 15 seconds for slower systems
            - May return False on timeout even if installed
            - Most reliable method if succeeds
        """
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['gemini', '--version'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=15,  # Increased timeout for slower systems
                creationflags=creationflags
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False

    def get_version(self) -> Optional[str]:
        """
        Get Gemini CLI version with extended timeout

        Attempts to retrieve the version string by running 'gemini --version'.
        Returns a special message if the command times out but Gemini is installed.

        Returns:
            Optional[str]: Version string, timeout message, or None if not installed

        Examples:
            >>> checker = GeminiCliChecker()
            >>> version = checker.get_version()
            >>> if version:
            ...     print(f"Gemini CLI version: {version}")

        Note:
            - Timeout is set to 10 seconds
            - Returns Korean message on timeout
            - Returns None if command fails
        """
        try:
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['gemini', '--version'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=10,
                creationflags=creationflags
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except subprocess.TimeoutExpired:
            return "설치됨 (버전 확인 시간 초과)"
        except Exception:
            return None


__all__ = ['ClaudeCliChecker', 'GeminiCliChecker']
