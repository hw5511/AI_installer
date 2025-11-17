"""
Software Installer Module
Executes software installation via package managers
Brain Module System v4.0
"""

import subprocess
import os
from typing import Optional, Callable, Tuple


class SoftwareInstaller:
    """Executes software installation commands"""

    def __init__(self, config, log_callback: Optional[Callable] = None):
        """
        Initialize software installer

        Args:
            config: Configuration object for subprocess flags and timeouts
            log_callback: Logging callback function (default: print)
        """
        self.config = config
        self.log_callback = log_callback or print

    def _log(self, message: str) -> None:
        """Log message using injected callback"""
        self.log_callback(message)

    def execute_command(self, command: list, timeout: Optional[int] = None, shell: bool = False) -> Tuple[bool, str]:
        """
        Execute installation command with unified error handling

        Args:
            command: Command list to execute
            timeout: Command timeout (defaults to config.TIMEOUT_SECONDS)
            shell: Use shell execution

        Returns:
            Tuple of (success: bool, message: str)
        """
        timeout = timeout or self.config.TIMEOUT_SECONDS

        try:
            creationflags = self.config.get_subprocess_flags()
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=shell,
                creationflags=creationflags
            )

            if result.returncode == 0:
                return True, result.stdout.strip() if result.stdout else ""
            else:
                error_msg = (result.stderr.strip() if result.stderr else "") or (result.stdout.strip() if result.stdout else "Unknown error")
                return False, error_msg

        except subprocess.TimeoutExpired:
            error_msg = f"명령어가 {timeout}초 후 시간 초과되었습니다"
            self._log(f"명령어 시간 초과: {' '.join(command)}")
            return False, error_msg

        except Exception as e:
            error_msg = f"예상치 못한 오류: {str(e)}"
            self._log(f"명령어 오류: {error_msg}")
            return False, error_msg

    def install_via_winget(self, package_id: str) -> Tuple[bool, str]:
        """
        Install software via Winget

        Args:
            package_id: Winget package ID (e.g., 'Git.Git', 'OpenJS.NodeJS')

        Returns:
            Tuple of (success: bool, message: str)
        """
        self._log(f"Winget을 사용하여 {package_id}를 설치하는 중...")

        cmd = [
            'winget', 'install', '--id', package_id, '-e', '--silent',
            '--accept-package-agreements', '--accept-source-agreements'
        ]

        success, message = self.execute_command(
            cmd,
            timeout=self.config.COMMAND_TIMEOUTS['package_install']
        )

        if success:
            self._log(f"{package_id}가 Winget을 통해 성공적으로 설치되었습니다!")
            return True, f"{package_id}가 Winget을 통해 성공적으로 설치되었습니다"
        else:
            error_msg = f"Winget을 통한 {package_id} 설치에 실패했습니다: {message}"
            self._log(error_msg)
            return False, error_msg

    def install_via_chocolatey(self, package_name: str) -> Tuple[bool, str]:
        """
        Install software via Chocolatey

        Args:
            package_name: Chocolatey package name (e.g., 'git', 'nodejs')

        Returns:
            Tuple of (success: bool, message: str)
        """
        self._log(f"Chocolatey를 사용하여 {package_name}를 설치하는 중...")

        cmd = ['choco', 'install', package_name, '-y', '--no-progress', '--ignore-detected-reboot']

        success, message = self.execute_command(
            cmd,
            timeout=self.config.COMMAND_TIMEOUTS['package_install'],
            shell=True
        )

        if success:
            self._log(f"{package_name}가 Chocolatey를 통해 성공적으로 설치되었습니다!")

            # Refresh environment variables for Chocolatey
            try:
                creationflags = self.config.get_subprocess_flags()
                subprocess.run(
                    'refreshenv',
                    shell=True,
                    timeout=self.config.COMMAND_TIMEOUTS['environment_refresh'],
                    creationflags=creationflags
                )
            except:
                pass

            return True, f"{package_name}가 Chocolatey를 통해 성공적으로 설치되었습니다"
        else:
            error_msg = f"Chocolatey를 통한 {package_name} 설치에 실패했습니다: {message}"
            self._log(error_msg)
            return False, error_msg

    def install_chocolatey_itself(self) -> Tuple[bool, str]:
        """
        Install Chocolatey package manager

        Returns:
            Tuple of (success: bool, message: str)
        """
        self._log("Chocolatey 패키지 관리자를 설치하는 중...")
        self._log("몇 분 정도 소요될 수 있습니다...")

        try:
            # PowerShell script to install Chocolatey
            install_script = """
            Set-ExecutionPolicy Bypass -Scope Process -Force;
            [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
            iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            """

            # Run the installation command
            cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', install_script]
            success, message = self.execute_command(
                cmd,
                timeout=300  # 5 minutes timeout
            )

            if success:
                success_msg = "Chocolatey가 성공적으로 설치되었습니다"
                self._log(success_msg)
                return True, success_msg
            else:
                error_msg = f"Chocolatey 설치에 실패했습니다: {message}"
                self._log(error_msg)
                return False, error_msg

        except Exception as e:
            error_msg = f"Chocolatey 설치 중 오류 발생: {str(e)}"
            self._log(error_msg)
            return False, error_msg


__all__ = ['SoftwareInstaller']
