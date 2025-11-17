"""
Tool Installer Module
Tool-specific installation logic
Brain Module System v4.0
"""

import subprocess
import os
from typing import Optional, Callable, Tuple, Dict

from .package_manager_detector import PackageManagerDetector
from .software_installer import SoftwareInstaller
from .installation_verifier import InstallationVerifier
from modules.core.exceptions import ToolInstallationError, ChocolateyNotFoundError
from modules.utils.path_manager import check_and_set_powershell_execution_policy, add_to_user_path_immediate


class ToolInstaller:
    """Manages tool-specific installation workflows"""

    def __init__(self, pm_detector: PackageManagerDetector,
                 sw_installer: SoftwareInstaller,
                 verifier: InstallationVerifier,
                 config=None,
                 error_logger=None):
        """
        Initialize with component instances

        Args:
            pm_detector: Package manager detector instance
            sw_installer: Software installer instance
            verifier: Installation verifier instance
            config: Configuration object for subprocess flags and timeouts
            error_logger: Optional error logger instance
        """
        self.pm_detector = pm_detector
        self.sw_installer = sw_installer
        self.verifier = verifier
        self.config = config
        self.log_callback = verifier.log_callback
        self.error_logger = error_logger

        # Package configuration data
        self.package_configs = {
            'git': {
                'winget_id': 'Git.Git',
                'choco_name': 'git',
                'software_name': 'git',
                'display_name': 'Git'
            },
            'nodejs': {
                'winget_id': 'OpenJS.NodeJS',
                'choco_name': 'nodejs',
                'software_name': 'nodejs',
                'display_name': 'Node.js'
            },
            'python': {
                'winget_id': 'Python.Python.3.12',
                'choco_name': 'python312',
                'software_name': 'python',
                'display_name': 'Python 3.12'
            },
            'claude_cli': {
                'npm_package': '@anthropic-ai/claude-code',
                'software_name': 'claude',
                'display_name': 'Claude CLI'
            },
            'gemini_cli': {
                'npm_package': '@google/gemini-cli',
                'software_name': 'gemini',
                'display_name': 'Gemini CLI'
            }
        }

    def _log(self, message: str) -> None:
        """Log message using injected callback"""
        self.log_callback(message)

    def install_git(self, method: str = 'auto') -> Tuple[bool, str]:
        """
        Install Git via winget or chocolatey with detailed diagnostics

        Args:
            method: Installation method ('auto', 'winget', 'chocolatey')

        Returns:
            Tuple of (success: bool, message: str)
        """
        self._log("--- Git 설치를 시작합니다 ---")
        self._log(f"[DEBUG] 요청된 설치 방법: {method}")

        config = self.package_configs['git']

        # Check if already installed
        if self.verifier._check_software_installed(config['software_name']):
            message = f"{config['display_name']}이 이미 설치되어 있습니다"
            self._log(message)
            return True, message

        # Check PowerShell execution policy (affects Chocolatey)
        self._check_powershell_policy()

        # Check system environment
        self._log(f"[DEBUG] Running as admin: {self.pm_detector.check_admin_rights()}")
        self._log(f"[DEBUG] System PATH entries count: {len(os.environ.get('PATH', '').split(';'))}")

        # Determine installation method
        if method == 'auto':
            method = self._auto_detect_package_manager()

        # Install based on method
        try:
            if method == 'winget' and self.pm_detector.check_winget_available():
                success, message = self.sw_installer.install_via_winget(config['winget_id'])
            elif method == 'chocolatey' and self.pm_detector.check_chocolatey_available():
                success, message = self.sw_installer.install_via_chocolatey(config['choco_name'])
            else:
                error_msg = f"설치 방법 '{method}'를 사용할 수 없습니다"
                self._log(error_msg)
                return False, error_msg

            if success:
                return self.verifier.verify_installation(config['software_name'])
            else:
                raise ToolInstallationError(f"{config['display_name']} 설치에 실패했습니다: {message}")

        except Exception as e:
            error_msg = f"{config['display_name']} 설치 오류: {str(e)}"
            self._log(error_msg)
            return False, error_msg

    def install_nodejs(self, method: str = 'auto') -> Tuple[bool, str]:
        """
        Install Node.js via winget or chocolatey

        Args:
            method: Installation method ('auto', 'winget', 'chocolatey')

        Returns:
            Tuple of (success: bool, message: str)
        """
        config = self.package_configs['nodejs']

        # Check if already installed
        if (self.verifier._check_software_installed(config['software_name']) and
            self.verifier._check_software_installed('npm')):
            message = f"{config['display_name']}와 npm이 이미 설치되어 있습니다"
            self._log(message)
            return True, message

        # Determine installation method
        if method == 'auto':
            method = self._auto_detect_package_manager()

        # Install based on method
        try:
            if method == 'winget' and self.pm_detector.check_winget_available():
                success, message = self.sw_installer.install_via_winget(config['winget_id'])
            elif method == 'chocolatey' and self.pm_detector.check_chocolatey_available():
                success, message = self.sw_installer.install_via_chocolatey(config['choco_name'])
            else:
                error_msg = f"설치 방법 '{method}'를 사용할 수 없습니다"
                self._log(error_msg)
                return False, error_msg

            if success:
                # Verify both Node.js and npm
                nodejs_success, nodejs_msg = self.verifier.verify_installation(config['software_name'])
                npm_success, npm_msg = self.verifier.verify_installation('npm')

                if nodejs_success and npm_success:
                    return True, f"{config['display_name']}와 npm이 성공적으로 설치되고 확인되었습니다"
                elif nodejs_success:
                    return True, f"{config['display_name']}가 성공적으로 설치되었습니다. npm 상태: {npm_msg}"
                else:
                    return False, f"{config['display_name']} 설치 문제: {nodejs_msg}"
            else:
                raise ToolInstallationError(f"{config['display_name']} 설치에 실패했습니다: {message}")

        except Exception as e:
            error_msg = f"{config['display_name']} 설치 오류: {str(e)}"
            self._log(error_msg)
            return False, error_msg

    def install_python(self, method: str = 'auto') -> Tuple[bool, str]:
        """
        Install Python 3.12 via package manager

        Args:
            method: Installation method ('auto', 'winget', 'chocolatey')

        Returns:
            Tuple of (success: bool, message: str)
        """
        config = self.package_configs['python']

        # Check if already installed
        if self.verifier._check_software_installed(config['software_name']):
            message = f"{config['display_name']}이 이미 설치되어 있습니다"
            self._log(message)
            return True, message

        # Determine installation method
        if method == 'auto':
            method = self._auto_detect_package_manager()

        # Install based on method
        try:
            if method == 'chocolatey' and self.pm_detector.check_chocolatey_available():
                success, message = self.sw_installer.install_via_chocolatey(config['choco_name'])
            elif method == 'winget' and self.pm_detector.check_winget_available():
                success, message = self.sw_installer.install_via_winget(config['winget_id'])
            else:
                error_msg = f"설치 방법 '{method}'를 사용할 수 없습니다"
                self._log(error_msg)
                return False, error_msg

            if success:
                return self.verifier.verify_installation(config['software_name'])
            else:
                raise ToolInstallationError(f"{config['display_name']} 설치에 실패했습니다: {message}")

        except Exception as e:
            error_msg = f"{config['display_name']} 설치 오류: {str(e)}"
            self._log(error_msg)
            return False, error_msg

    def install_claude_cli(self) -> Tuple[bool, str]:
        """
        Install Claude CLI via npm

        Returns:
            Tuple of (success: bool, message: str)
        """
        config = self.package_configs['claude_cli']

        # First check and set PowerShell execution policy for npm
        self._log("npm을 위한 PowerShell 실행 정책을 확인하는 중...")
        check_and_set_powershell_execution_policy()

        # Check npm availability
        if not self.verifier._check_software_installed('npm'):
            error_msg = "npm이 설치되어 있지 않습니다. 먼저 Node.js를 설치하세요."
            self._log(f"오류: {error_msg}")
            return False, error_msg

        # Check if already installed
        if self.verifier._check_software_installed(config['software_name']):
            message = f"{config['display_name']}가 이미 설치되어 있습니다"
            self._log(message)
            return True, message

        self._log(f"npm으로 {config['display_name']}를 설치하는 중...")

        try:
            # Install via npm
            cmd = ['npm', 'install', '-g', config['npm_package']]
            timeout = self.config.COMMAND_TIMEOUTS['package_install'] if self.config else 300
            success, message = self.sw_installer.execute_command(
                cmd,
                timeout=timeout,
                shell=True
            )

            if success:
                self._log(f"{config['display_name']}가 성공적으로 설치되었습니다!")

                # Get npm global bin directory and add to PATH
                self._add_npm_bin_to_path()

                # Verify installation
                return self.verifier.verify_installation(config['software_name'])
            else:
                # Provide helpful error messages
                self._log(f"[오류] {config['display_name']} 설치에 실패했습니다.")
                self._log("[정보] 네트워크 문제나 npm 레지스트리 문제일 수 있습니다.")
                self._log("[정보] 대체 설치 방법:")
                self._log("[정보] 1. PowerShell: irm https://claude.ai/install.ps1 | iex")
                self._log("[정보] 2. 수동: https://claude.ai/download 방문")
                self._log("[정보] 3. npm 전역 경로가 PATH 환경 변수에 있는지 확인하세요")

                error_msg = f"{config['display_name']} 설치에 실패했습니다. 네트워크 연결을 확인하고 다시 시도하세요."
                self._log(error_msg)
                return False, error_msg

        except Exception as e:
            error_msg = f"{config['display_name']} 설치 중 오류 발생: {str(e)}"
            self._log(error_msg)
            return False, error_msg

    def install_gemini_cli(self) -> Tuple[bool, str]:
        """
        Install Gemini CLI via npm

        Returns:
            Tuple of (success: bool, message: str)
        """
        config = self.package_configs['gemini_cli']

        # First check and set PowerShell execution policy for npm
        self._log("npm을 위한 PowerShell 실행 정책을 확인하는 중...")
        check_and_set_powershell_execution_policy()

        # Check npm availability
        if not self.verifier._check_software_installed('npm'):
            error_msg = "npm이 설치되어 있지 않습니다. 먼저 Node.js를 설치하세요."
            self._log(f"오류: {error_msg}")
            return False, error_msg

        # Check if already installed
        if self.verifier._check_software_installed(config['software_name']):
            message = f"{config['display_name']}가 이미 설치되어 있습니다"
            self._log(message)
            return True, message

        self._log(f"npm으로 {config['display_name']}를 설치하는 중...")

        try:
            # Install via npm
            cmd = ['npm', 'install', '-g', config['npm_package']]
            timeout = self.config.COMMAND_TIMEOUTS['package_install'] if self.config else 300
            success, message = self.sw_installer.execute_command(
                cmd,
                timeout=timeout,
                shell=True
            )

            if success:
                self._log(f"{config['display_name']}가 성공적으로 설치되었습니다!")

                # Get npm global bin directory and add to User PATH
                try:
                    creationflags = self.config.get_subprocess_flags() if self.config else 0
                    npm_prefix_result = subprocess.run(
                        ['npm', 'config', 'get', 'prefix'],
                        capture_output=True,
                        text=True,
                        shell=True,
                        timeout=self.config.COMMAND_TIMEOUTS.get('npm_config_check', 30) if self.config else 30,
                        creationflags=creationflags
                    )

                    if npm_prefix_result.returncode == 0:
                        npm_prefix = npm_prefix_result.stdout.strip()
                        npm_bin = npm_prefix if os.name == 'nt' else os.path.join(npm_prefix, 'bin')

                        self._log(f"Detected npm global path: {npm_bin}")

                        # Add to User PATH (not System PATH!)
                        if add_to_user_path_immediate([npm_bin]):
                            self._log(f"Successfully added npm path to User PATH: {npm_bin}")
                        else:
                            error_msg = f"Failed to add npm path to User PATH: {npm_bin}"
                            self._log(f"[ERROR] {error_msg}")
                            raise Exception(error_msg)
                    else:
                        error_msg = f"npm config get prefix failed: {npm_prefix_result.stderr}"
                        self._log(f"[ERROR] {error_msg}")
                        raise Exception(error_msg)

                except Exception as e:
                    self._log(f"[ERROR] Error during npm PATH setup: {str(e)}")
                    # Log to error logger if available
                    if hasattr(self, 'error_logger') and self.error_logger:
                        import traceback
                        self.error_logger.add_error_detail(
                            step="Gemini CLI npm PATH addition",
                            error_message=str(e),
                            traceback_info=traceback.format_exc()
                        )
                    # Continue installation (CLI is installed but PATH failed)
                    self._log("[WARNING] Gemini CLI installed but PATH addition failed - manual setup may be required")

                # Verify installation
                return self.verifier.verify_installation(config['software_name'])
            else:
                error_msg = f"{config['display_name']} 설치에 실패했습니다: {message}"
                self._log(error_msg)
                return False, error_msg

        except Exception as e:
            error_msg = f"{config['display_name']} 설치 중 오류 발생: {str(e)}"
            self._log(error_msg)
            return False, error_msg

    def _check_powershell_policy(self) -> None:
        """Check PowerShell execution policy (affects Chocolatey)"""
        try:
            creationflags = self.config.get_subprocess_flags() if self.config else 0
            ps_result = subprocess.run(
                ['powershell', '-Command', 'Get-ExecutionPolicy'],
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=creationflags
            )
            if ps_result.returncode == 0:
                policy = ps_result.stdout.strip()
                self._log(f"[DEBUG] PowerShell Execution Policy: {policy}")
                if policy in ['Restricted', 'AllSigned']:
                    self._log("[WARNING] PowerShell execution policy may prevent Chocolatey from working properly")
        except Exception as e:
            self._log(f"[DEBUG] Could not check PowerShell execution policy: {e}")

    def _auto_detect_package_manager(self) -> str:
        """
        Auto-detect available package manager

        Returns:
            str: Package manager name ('winget' or 'chocolatey')

        Raises:
            ChocolateyNotFoundError: If no package manager is available
        """
        self._log("[DEBUG] Auto-detecting package manager...")

        winget_available = self.pm_detector.check_winget_available()
        choco_available = self.pm_detector.check_chocolatey_available()

        self._log(f"[DEBUG] Package manager availability summary:")
        self._log(f"[DEBUG]   Winget: {winget_available}")
        self._log(f"[DEBUG]   Chocolatey: {choco_available}")

        if choco_available:
            self._log("[DEBUG] Selected Chocolatey for installation")
            return 'chocolatey'
        elif winget_available:
            self._log("[DEBUG] Selected Winget for installation")
            return 'winget'
        else:
            # Try refreshing PATH and check again
            self._log("[DEBUG] No package manager found, attempting PATH refresh...")
            if self.pm_detector.refresh_environment():
                self._log("[DEBUG] Rechecking after PATH refresh...")
                choco_available = self.pm_detector.check_chocolatey_available()
                if choco_available:
                    self._log("[DEBUG] Chocolatey found after PATH refresh!")
                    return 'chocolatey'
                else:
                    winget_available = self.pm_detector.check_winget_available()
                    if winget_available:
                        self._log("[DEBUG] Winget found after PATH refresh!")
                        return 'winget'

            # Still no package manager found
            error_msg = "Winget과 Chocolatey 모두 사용할 수 없습니다"
            self._log(f"[오류] {error_msg}")
            self._log("[정보] 가능한 해결책:")
            self._log("  1. Chocolatey 설치 후 애플리케이션을 재시작하세요")
            self._log("  2. 관리자 권한으로 새 PowerShell/CMD 창을 여세요")
            self._log("  3. 수동으로 PATH 새로고침: $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine')")
            raise ChocolateyNotFoundError(error_msg)

    def _add_npm_bin_to_path(self) -> None:
        """Add npm global bin directory to User PATH"""
        try:
            creationflags = self.config.get_subprocess_flags() if self.config else 0
            timeout = self.config.COMMAND_TIMEOUTS.get('npm_config_check', 30) if self.config else 30

            npm_prefix_result = subprocess.run(
                ['npm', 'config', 'get', 'prefix'],
                capture_output=True,
                text=True,
                shell=True,
                timeout=timeout,
                creationflags=creationflags
            )

            if npm_prefix_result.returncode == 0:
                npm_prefix = npm_prefix_result.stdout.strip()
                npm_bin = npm_prefix if os.name == 'nt' else os.path.join(npm_prefix, 'bin')

                self._log(f"Detected npm global path: {npm_bin}")

                # Add to User PATH (not System PATH!)
                if add_to_user_path_immediate([npm_bin]):
                    self._log(f"Successfully added npm path to User PATH: {npm_bin}")
                else:
                    error_msg = f"Failed to add npm path to User PATH: {npm_bin}"
                    self._log(f"[ERROR] {error_msg}")
                    raise Exception(error_msg)
            else:
                error_msg = f"npm config get prefix failed: {npm_prefix_result.stderr}"
                self._log(f"[ERROR] {error_msg}")
                raise Exception(error_msg)

        except Exception as e:
            self._log(f"[ERROR] Error during npm PATH setup: {str(e)}")
            # Log to error logger if available
            if hasattr(self, 'error_logger') and self.error_logger:
                import traceback
                self.error_logger.add_error_detail(
                    step="Claude CLI npm PATH addition",
                    error_message=str(e),
                    traceback_info=traceback.format_exc()
                )
            # Continue installation (CLI is installed but PATH failed)
            self._log("[WARNING] Claude CLI installed but PATH addition failed - manual setup may be required")


__all__ = ['ToolInstaller']
