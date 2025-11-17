"""
Unified Status Checker Module - Facade Pattern
Brain Module System v4.0 - Refactored for modularity
"""

from typing import Dict, Optional, Any
from modules.core.config import Config
from modules.core.exceptions import ToolCheckError

# Import from separated modules
from .checker_modules.checker_utils import check_command_exists
from .checker_modules.tool_checkers import GitChecker, NodeJsChecker, PackageManagerChecker
from .checker_modules.cli_checkers import ClaudeCliChecker, GeminiCliChecker
from .checker_modules.system_explorer import SystemExplorer


class StatusChecker:
    """
    Unified status checker - Facade pattern
    Delegates to specialized checker modules
    """

    def __init__(self, config=None):
        """
        Initialize StatusChecker with all checker components

        Args:
            config: Configuration object (optional, uses default if None)
        """
        self.config = config or Config()
        self._cache = {}
        self._cache_enabled = True

        # Initialize all checker components
        self.git_checker = GitChecker(self.config)
        self.nodejs_checker = NodeJsChecker(self.config)
        self.pm_checker = PackageManagerChecker(self.config)
        self.claude_checker = ClaudeCliChecker()
        self.gemini_checker = GeminiCliChecker()
        self.system_explorer = SystemExplorer()

    # Git delegation methods
    def is_git_installed(self) -> bool:
        """Delegate to GitChecker"""
        return self.git_checker.is_installed()

    def get_git_version(self) -> Optional[str]:
        """Delegate to GitChecker"""
        return self.git_checker.get_version()

    # Node.js delegation methods
    def is_nodejs_installed(self) -> bool:
        """Delegate to NodeJsChecker"""
        return self.nodejs_checker.is_installed()

    def get_nodejs_version(self) -> Optional[str]:
        """Delegate to NodeJsChecker"""
        return self.nodejs_checker.get_version()

    # npm delegation methods
    def is_npm_installed(self) -> bool:
        """Delegate to PackageManagerChecker"""
        return self.pm_checker.is_npm_installed()

    def get_npm_version(self) -> Optional[str]:
        """Delegate to PackageManagerChecker"""
        return self.pm_checker.get_npm_version()

    # Claude CLI delegation methods
    def is_claude_cli_installed(self) -> bool:
        """Delegate to ClaudeCliChecker"""
        return self.claude_checker.is_installed()

    def get_claude_cli_version(self) -> Optional[str]:
        """Delegate to ClaudeCliChecker"""
        return self.claude_checker.get_version()

    # Gemini CLI delegation methods
    def is_gemini_cli_installed(self) -> bool:
        """Delegate to GeminiCliChecker"""
        return self.gemini_checker.is_installed()

    def get_gemini_cli_version(self) -> Optional[str]:
        """Delegate to GeminiCliChecker"""
        return self.gemini_checker.get_version()

    # Package manager delegation methods
    def is_chocolatey_installed(self) -> bool:
        """Delegate to PackageManagerChecker"""
        return self.pm_checker.is_chocolatey_installed()

    def get_chocolatey_version(self) -> Optional[str]:
        """Delegate to PackageManagerChecker"""
        return self.pm_checker.get_chocolatey_version()

    def is_winget_installed(self) -> bool:
        """Delegate to PackageManagerChecker"""
        return self.pm_checker.is_winget_installed()

    def get_winget_version(self) -> Optional[str]:
        """Delegate to PackageManagerChecker"""
        return self.pm_checker.get_winget_version()

    # System exploration delegation methods
    def _find_git_installations(self):
        """Delegate to SystemExplorer"""
        return self.system_explorer.find_git_installations()

    def _find_nodejs_installations(self):
        """Delegate to SystemExplorer"""
        return self.system_explorer.find_nodejs_installations()

    def _get_system_path(self):
        """Delegate to SystemExplorer"""
        return self.system_explorer.get_system_path()

    def _get_user_path(self):
        """Delegate to SystemExplorer"""
        return self.system_explorer.get_user_path()

    def _get_git_config(self):
        """Delegate to GitChecker"""
        return self.git_checker.get_config()

    def _get_npm_config(self):
        """Delegate to PackageManagerChecker"""
        return self.pm_checker.get_npm_config()

    def _get_npm_global_packages(self):
        """Delegate to PackageManagerChecker"""
        return self.pm_checker.get_npm_global_packages()

    def get_detailed_git_status(self) -> Dict[str, Any]:
        """Get detailed Git installation status"""
        return {
            'installed': self.is_git_installed(),
            'version': self.get_git_version(),
            'installations': self._find_git_installations(),
            'config': self._get_git_config() if self.is_git_installed() else {},
            'system_path': self._get_system_path(),
            'user_path': self._get_user_path()
        }

    def get_detailed_nodejs_status(self) -> Dict[str, Any]:
        """Get detailed Node.js installation status"""
        return {
            'node_installed': self.is_nodejs_installed(),
            'node_version': self.get_nodejs_version(),
            'npm_installed': self.is_npm_installed(),
            'npm_version': self.get_npm_version(),
            'installations': self._find_nodejs_installations(),
            'npm_config': self._get_npm_config() if self.is_npm_installed() else {},
            'global_packages': self._get_npm_global_packages() if self.is_npm_installed() else [],
            'system_path': self._get_system_path(),
            'user_path': self._get_user_path()
        }

    def check_all(self) -> Dict[str, Any]:
        """
        Return complete status dictionary for all software with standardized format

        Returns:
            Dictionary containing installation status for all components
        """
        # Check installation status for all tools
        git_installed = self.is_git_installed()
        nodejs_installed = self.is_nodejs_installed()
        npm_installed = self.is_npm_installed()
        claude_installed = self.is_claude_cli_installed()
        gemini_installed = self.is_gemini_cli_installed()
        choco_installed = self.is_chocolatey_installed()
        winget_installed = self.is_winget_installed()

        return {
            'choco': {
                'installed': choco_installed,
                'version': self.get_chocolatey_version() if choco_installed else None
            },
            'git': {
                'installed': git_installed,
                'version': self.get_git_version() if git_installed else None,
                'available': git_installed
            },
            'nodejs': {
                'installed': nodejs_installed,
                'version': self.get_nodejs_version() if nodejs_installed else None,
                'available': nodejs_installed
            },
            'npm': {
                'installed': npm_installed,
                'version': self.get_npm_version() if npm_installed else None,
                'available': npm_installed
            },
            'claude': {
                'installed': claude_installed,
                'version': self.get_claude_cli_version() if claude_installed else None,
                'available': claude_installed
            },
            'gemini': {
                'installed': gemini_installed,
                'version': self.get_gemini_cli_version() if gemini_installed else None,
                'available': gemini_installed
            },
            'winget': {
                'installed': winget_installed,
                'version': self.get_winget_version() if winget_installed else None,
                'available': winget_installed
            },
            'summary': {
                'total_checked': 7,
                'installed_count': sum([
                    git_installed,
                    nodejs_installed,
                    npm_installed,
                    claude_installed,
                    gemini_installed,
                    choco_installed,
                    winget_installed
                ]),
                'all_installed': all([
                    git_installed,
                    nodejs_installed,
                    npm_installed,
                    claude_installed,
                    gemini_installed
                ])  # Core tools only
            }
        }

    def clear_cache(self):
        """Clear internal cache"""
        self._cache.clear()

    def disable_cache(self):
        """Disable caching for fresh checks"""
        self._cache_enabled = False
        self.clear_cache()

    def enable_cache(self):
        """Enable caching for performance"""
        self._cache_enabled = True


# Export for backward compatibility
__all__ = ['StatusChecker', 'check_command_exists']


def main():
    """Demo function showing usage of StatusChecker"""
    try:
        checker = StatusChecker()

        print("=" * 60)
        print("통합 상태 확인")
        print("=" * 60)

        # Get complete status
        status = checker.check_all()

        print(f"\n설치 요약: {status['summary']['installed_count']}/{status['summary']['total_checked']} 도구")
        print("-" * 40)

        # Show individual tool status
        tools = ['choco', 'git', 'nodejs', 'npm', 'claude', 'winget']
        for tool in tools:
            tool_status = status[tool]
            status_symbol = "OK" if tool_status['installed'] else "X"
            version_info = f" ({tool_status['version']})" if tool_status['version'] else ""
            print(f"{status_symbol} {tool.replace('_', ' ').title()}: {'설치됨' if tool_status['installed'] else '설치되지 않음'}{version_info}")

        print("\n" + "=" * 60)
        if status['summary']['all_installed']:
            print("모든 핵심 개발 도구가 설치되었습니다!")
        else:
            missing_tools = [tool for tool in ['git', 'nodejs', 'npm', 'claude']
                            if not status[tool]['installed']]
            print(f"누락된 핵심 도구: {', '.join(missing_tools)}")
        print("=" * 60)

        return status

    except Exception as e:
        raise ToolCheckError(f"상태 확인 실패: {str(e)}")


if __name__ == "__main__":
    import sys
    try:
        result = main()
        sys.exit(0 if result['summary']['all_installed'] else 1)
    except Exception as e:
        print(f"오류: {e}")
        sys.exit(1)