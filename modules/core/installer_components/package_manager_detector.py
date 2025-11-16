"""
Package Manager Detector Module
Detects Winget/Chocolatey availability and manages admin rights
Brain Module System v4.0
"""

import subprocess
import os
import ctypes
import winreg
from typing import Optional, Callable


class PackageManagerDetector:
    """Detects and validates package managers (Winget/Chocolatey)"""

    def __init__(self, config=None, log_callback: Optional[Callable] = None):
        """
        Initialize package manager detector

        Args:
            config: Configuration object with timeout settings
            log_callback: Logging callback function (default: print)
        """
        self.config = config
        self.log_callback = log_callback or print

    def _log(self, message: str) -> None:
        """Log message using injected callback"""
        self.log_callback(message)

    def check_admin_rights(self) -> bool:
        """
        Check if running with administrator privileges

        Returns:
            bool: True if running as admin, False otherwise
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def refresh_environment(self) -> bool:
        """
        Refresh PATH environment variable from system registry

        Returns:
            bool: True if refresh succeeded, False otherwise
        """
        try:
            self._log("[DEBUG] 레지스트리에서 환경 변수를 새로고침하는 중...")

            # Read system PATH from registry
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                              r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                system_path, _ = winreg.QueryValueEx(key, "Path")

            # Read user PATH from registry
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              r"Environment") as key:
                try:
                    user_path, _ = winreg.QueryValueEx(key, "Path")
                except:
                    user_path = ""

            # Combine paths
            combined_path = system_path
            if user_path:
                combined_path = f"{system_path};{user_path}"

            # Update current process PATH
            os.environ['PATH'] = combined_path
            self._log(f"[DEBUG] PATH가 {len(combined_path.split(';'))}개 항목으로 새로고침되었습니다")

            # Check if Chocolatey is now in PATH
            if 'chocolatey' in combined_path.lower():
                self._log("[DEBUG] 새로고침된 PATH에서 Chocolatey를 찾았습니다")
                choco_entries = [p for p in combined_path.split(';') if 'chocolatey' in p.lower()]
                for entry in choco_entries:
                    self._log(f"[DEBUG]   Chocolatey PATH: {entry}")

            return True
        except Exception as e:
            self._log(f"[DEBUG] 환경 변수 새로고침에 실패했습니다: {e}")
            return False

    def check_winget_available(self) -> bool:
        """
        Check if Winget is available with detailed logging

        Returns:
            bool: True if Winget is available, False otherwise
        """
        self._log("[DEBUG] Winget 사용 가능성 확인을 시작합니다...")

        try:
            self._log("[DEBUG] 'winget --version' 명령어를 시도하는 중...")

            # Get subprocess flags from config if available
            creationflags = self.config.get_subprocess_flags() if self.config else 0
            timeout = self.config.COMMAND_TIMEOUTS['version_check'] if self.config else 10

            result = subprocess.run(
                ['winget', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags
            )

            if result.returncode == 0:
                self._log(f"[DEBUG] Winget을 찾았습니다: {result.stdout.strip()}")
                return True
            else:
                self._log(f"[DEBUG] Winget 명령어가 코드 {result.returncode}로 실패했습니다")
                self._log(f"[DEBUG] 오류 출력: {result.stderr}")
                return False

        except FileNotFoundError as e:
            self._log(f"[DEBUG] Winget 명령어를 찾을 수 없습니다: {e}")
            return False
        except subprocess.TimeoutExpired:
            timeout = self.config.COMMAND_TIMEOUTS['version_check'] if self.config else 10
            self._log(f"[DEBUG] Winget command timed out after {timeout}s")
            return False
        except Exception as e:
            self._log(f"[DEBUG] Unexpected error checking Winget: {type(e).__name__}: {e}")
            return False

    def check_chocolatey_available(self) -> bool:
        """
        Check if Chocolatey is available with detailed logging

        Returns:
            bool: True if Chocolatey is available, False otherwise
        """
        self._log("[DEBUG] Starting Chocolatey availability check...")

        # Get subprocess flags and timeout from config if available
        creationflags = self.config.get_subprocess_flags() if self.config else 0
        timeout = self.config.COMMAND_TIMEOUTS['version_check'] if self.config else 10

        # Check 1: Direct command test
        try:
            self._log("[DEBUG] Attempting direct 'choco --version' command...")
            result = subprocess.run(
                ['choco', '--version'],
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=creationflags
            )

            if result.returncode == 0:
                self._log(f"[DEBUG] Chocolatey found via command: {result.stdout.strip()}")
                return True
            else:
                self._log(f"[DEBUG] Chocolatey command failed with code {result.returncode}")
                self._log(f"[DEBUG] stderr: {result.stderr}")

        except FileNotFoundError as e:
            self._log(f"[DEBUG] Chocolatey command not found in PATH: {e}")
        except subprocess.TimeoutExpired:
            self._log(f"[DEBUG] Chocolatey command timed out after {timeout}s")
        except Exception as e:
            self._log(f"[DEBUG] Unexpected error checking Chocolatey: {type(e).__name__}: {e}")

        # Check 2: Check common installation paths
        choco_paths = [
            r"C:\ProgramData\chocolatey\bin\choco.exe",
            r"C:\Chocolatey\bin\choco.exe"
        ]

        for path in choco_paths:
            if os.path.exists(path):
                self._log(f"[DEBUG] Chocolatey executable found at: {path}")

                # Try to run it directly
                try:
                    result = subprocess.run(
                        [path, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                        creationflags=creationflags
                    )

                    if result.returncode == 0:
                        self._log(f"[DEBUG] Chocolatey works from direct path: {result.stdout.strip()}")
                        self._log(f"[WARNING] Chocolatey exists but not in PATH - PATH update may be needed")
                        return True
                except Exception as e:
                    self._log(f"[DEBUG] Could not execute Chocolatey from {path}: {e}")

        # Check 3: Check current PATH
        current_path = os.environ.get('PATH', '')
        self._log(f"[DEBUG] Current PATH contains {len(current_path.split(';'))} entries")

        if 'chocolatey' in current_path.lower():
            self._log(f"[DEBUG] PATH contains 'chocolatey' but command still not working")
            choco_paths_in_path = [p for p in current_path.split(';') if 'chocolatey' in p.lower()]
            for p in choco_paths_in_path:
                self._log(f"[DEBUG]   Chocolatey PATH entry: {p}")

        self._log("[DEBUG] Chocolatey is not available")
        return False


__all__ = ['PackageManagerDetector']
