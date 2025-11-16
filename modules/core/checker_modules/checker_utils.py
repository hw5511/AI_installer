"""
Checker Utilities Module
Common utility functions for status checkers
Brain Module System v4.0
"""

import subprocess
from typing import Optional, Tuple

# Config import
try:
    from modules.core.config import Config
    _config = Config()
except ImportError:
    _config = None


def check_command_exists(command: str, timeout: int = 5) -> Tuple[bool, Optional[str]]:
    """
    Check if a command exists and is executable

    Args:
        command: Command to check (e.g., 'git --version')
        timeout: Timeout in seconds (default: 5)

    Returns:
        Tuple[bool, Optional[str]]: (exists, version_or_error)
            - exists: True if command exists and ran successfully
            - version_or_error: Command output or error message
    """
    try:
        cmd_parts = command.split()
        creationflags = _config.get_subprocess_flags() if _config else 0
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            shell=True,
            timeout=timeout,
            creationflags=creationflags
        )

        if result.returncode == 0:
            version = result.stdout.strip() or result.stderr.strip()
            return True, version
        else:
            return False, None

    except subprocess.TimeoutExpired:
        return False, "명령어 시간 초과"
    except FileNotFoundError:
        return False, "명령어를 찾을 수 없음"
    except Exception as e:
        error_msg = str(e)
        return False, error_msg


__all__ = ['check_command_exists', '_config']
