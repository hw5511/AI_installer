"""
Path Registry Module
Windows registry PATH reading operations
Brain Module System v4.0
"""

import winreg
from typing import List, Callable, Optional


class PathRegistry:
    """Handles Windows registry PATH operations"""

    def __init__(self, log_callback: Optional[Callable] = None):
        """Initialize with optional logging callback"""
        self.log_callback = log_callback

    def _log(self, message: str, level: str = "INFO"):
        """Log a message"""
        if self.log_callback:
            self.log_callback(f"[{level}] {message}")
        else:
            print(f"[{level}] {message}")

    def get_current_system_path(self) -> List[str]:
        """Get current system PATH from registry"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
                0,
                winreg.KEY_READ
            )

            try:
                system_path, _ = winreg.QueryValueEx(key, 'Path')
                return [p.strip() for p in system_path.split(';') if p.strip()]
            finally:
                winreg.CloseKey(key)
        except Exception as e:
            self._log(f"시스템 PATH 읽기 실패: {e}", "ERROR")
            return []

    def get_current_user_path(self) -> List[str]:
        """Get current user PATH from registry"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Environment',
                0,
                winreg.KEY_READ
            )

            try:
                user_path, _ = winreg.QueryValueEx(key, 'Path')
                return [p.strip() for p in user_path.split(';') if p.strip()]
            except:
                return []
            finally:
                winreg.CloseKey(key)
        except Exception:
            return []


__all__ = ['PathRegistry']
