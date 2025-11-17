"""
Tool Executor Module
Executes tools in new process for verification
Brain Module System v4.0
"""

import subprocess
import os
from typing import Optional, Tuple, Dict, List, Any

try:
    from modules.core.config import Config
    _config = Config()
except Exception:
    _config = None


class ToolExecutor:
    """Executes tools in new process to verify PATH access"""

    def __init__(self, log_callback=None):
        """Initialize tool executor"""
        self.log_callback = log_callback

    def log(self, message: str) -> None:
        """Log a message"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def execute_tool(self, tool_name: str, command_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute tool in new process to verify PATH access

        Args:
            tool_name: Tool name
            command_info: Dict with 'command' and 'args'

        Returns:
            dict: Result with tool, status, version, command
        """
        try:
            command = command_info['command']

            # Generate PowerShell command
            ps_command = self.generate_powershell_command(command, command_info['args'])

            # Execute in new process
            creationflags = self._get_subprocess_flags()

            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=creationflags
            )

            # Parse result
            if result.returncode == 0 and result.stdout and 'NOTFOUND' not in result.stdout:
                version = result.stdout.strip() if result.stdout else ''
                return {
                    'tool': tool_name,
                    'status': 'success',
                    'version': version,
                    'command': command
                }
            else:
                return {
                    'tool': tool_name,
                    'status': 'not_found',
                    'version': None,
                    'command': command
                }

        except subprocess.TimeoutExpired:
            return {
                'tool': tool_name,
                'status': 'timeout',
                'version': None,
                'command': command_info['command']
            }

        except Exception as e:
            return {
                'tool': tool_name,
                'status': 'error',
                'version': None,
                'command': command_info['command'],
                'error': str(e)
            }

    def generate_powershell_command(self, command: str, args: List[str]) -> str:
        """Generate PowerShell command for tool execution"""
        args_str = ' '.join(args)
        base_script = """
$ErrorActionPreference = 'SilentlyContinue'
$MachinePath = [Environment]::GetEnvironmentVariable('PATH', 'Machine')
$UserPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
$env:PATH = "$MachinePath;$UserPath"
"""

        if os.name == 'nt' and command in ['npm', 'claude']:
            return base_script + f"""
$result = & {command}.cmd {args_str} 2>&1
if ($LASTEXITCODE -eq 0) {{ Write-Output $result; exit 0 }}
$result = & {command} {args_str} 2>&1
if ($LASTEXITCODE -eq 0) {{ Write-Output $result; exit 0 }} else {{ Write-Output "NOTFOUND"; exit 1 }}
"""
        else:
            return base_script + f"""
$result = & {command} {args_str} 2>&1
if ($LASTEXITCODE -eq 0) {{ Write-Output $result; exit 0 }} else {{ Write-Output "NOTFOUND"; exit 1 }}
"""

    def _get_subprocess_flags(self) -> int:
        """Get subprocess creation flags from config"""
        if _config:
            return _config.get_subprocess_flags()
        return subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW


__all__ = ['ToolExecutor']
