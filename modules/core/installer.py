"""
Installer Module - Facade Pattern
Unified installation interface
Brain Module System v4.0
"""

from typing import Optional, Callable, Dict, Tuple

from modules.core.config import Config
from modules.core.installer_components.package_manager_detector import PackageManagerDetector
from modules.core.installer_components.software_installer import SoftwareInstaller
from modules.core.installer_components.installation_verifier import InstallationVerifier
from modules.core.installer_components.tool_installer import ToolInstaller


class Installer:
    """
    Unified installer - Facade pattern
    통합 설치 인터페이스
    의존성 주입 패턴으로 구성 요소 조합
    """

    def __init__(self, config: Optional[Config] = None, log_callback: Optional[Callable] = None):
        """
        Initialize installer with dependency injection

        Args:
            config: Configuration object (default: new Config instance)
            log_callback: Logging callback function (default: print)
        """
        self.config = config or Config()
        self.log_callback = log_callback or print

        # Initialize all installer components
        self.pm_detector = PackageManagerDetector(self.config, self.log_callback)
        self.sw_installer = SoftwareInstaller(self.config, self.log_callback)
        self.verifier = InstallationVerifier(self.config, self.log_callback)
        self.tool_installer = ToolInstaller(
            self.pm_detector,
            self.sw_installer,
            self.verifier,
            self.config
        )

    def install_git(self, method: str = 'auto') -> Tuple[bool, str]:
        """
        Install Git via winget or chocolatey

        Args:
            method: Installation method ('auto', 'winget', 'chocolatey')

        Returns:
            Tuple of (success: bool, message: str)
        """
        return self.tool_installer.install_git(method)

    def install_nodejs(self, method: str = 'auto') -> Tuple[bool, str]:
        """
        Install Node.js via winget or chocolatey

        Args:
            method: Installation method ('auto', 'winget', 'chocolatey')

        Returns:
            Tuple of (success: bool, message: str)
        """
        return self.tool_installer.install_nodejs(method)

    def install_python(self, method: str = 'auto') -> Tuple[bool, str]:
        """
        Install Python 3.12 via package manager (Facade)

        Args:
            method: Installation method ('auto', 'winget', 'chocolatey')

        Returns:
            Tuple of (success: bool, message: str)
        """
        return self.tool_installer.install_python(method)

    def install_claude_cli(self) -> Tuple[bool, str]:
        """
        Install Claude CLI via npm

        Returns:
            Tuple of (success: bool, message: str)
        """
        return self.tool_installer.install_claude_cli()

    def install_gemini_cli(self) -> Tuple[bool, str]:
        """
        Install Gemini CLI via npm

        Returns:
            Tuple of (success: bool, message: str)
        """
        return self.tool_installer.install_gemini_cli()

    def install_chocolatey(self) -> Tuple[bool, str]:
        """
        Install Chocolatey package manager

        Returns:
            Tuple of (success: bool, message: str)
        """
        if self.pm_detector.check_chocolatey_available():
            message = "Chocolatey가 이미 설치되어 있습니다"
            self.log_callback(message)
            return True, message

        return self.sw_installer.install_chocolatey_itself()

    def get_installation_status(self) -> Dict[str, bool]:
        """
        Get installation status of all supported software

        Returns:
            Dictionary mapping software names to installation status
        """
        return {
            'winget': self.pm_detector.check_winget_available(),
            'chocolatey': self.pm_detector.check_chocolatey_available(),
            'git': self.verifier._check_software_installed('git'),
            'nodejs': self.verifier._check_software_installed('nodejs'),
            'npm': self.verifier._check_software_installed('npm'),
            'python': self.verifier._check_software_installed('python'),
            'claude': self.verifier._check_software_installed('claude'),
            'gemini': self.verifier._check_software_installed('gemini')
        }

    def install_all(self) -> Dict[str, Tuple[bool, str]]:
        """
        Install all required software

        Returns:
            Dictionary of installation results with (success, message) tuples
        """
        results = {}

        # Install Git
        try:
            results['git'] = self.install_git()
        except Exception as e:
            results['git'] = (False, str(e))

        # Install Node.js
        try:
            results['nodejs'] = self.install_nodejs()
        except Exception as e:
            results['nodejs'] = (False, str(e))

        # Install Claude CLI
        try:
            if results.get('nodejs', (False, ''))[0] or self.verifier._check_software_installed('npm'):
                results['claude'] = self.install_claude_cli()
            else:
                results['claude'] = (False, "Claude CLI를 위해 Node.js 설치가 필요합니다")
        except Exception as e:
            results['claude'] = (False, str(e))

        # Install Gemini CLI
        try:
            if results.get('nodejs', (False, ''))[0] or self.verifier._check_software_installed('npm'):
                results['gemini'] = self.install_gemini_cli()
            else:
                results['gemini'] = (False, "Gemini CLI를 위해 Node.js 설치가 필요합니다")
        except Exception as e:
            results['gemini'] = (False, str(e))

        return results


__all__ = ['Installer']
