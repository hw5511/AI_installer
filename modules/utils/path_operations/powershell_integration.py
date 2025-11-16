"""
PowerShell Integration Module
PowerShell script execution for PATH management
Brain Module System v4.0
"""

import subprocess
from typing import Optional, Tuple, List

# Import Config for production mode detection with safe initialization
try:
    from modules.core.config import Config
    _config = Config()
except Exception:
    # Fallback if Config is not available or initialization fails
    _config = None


class PowerShellIntegration:
    """Manages PowerShell script execution"""

    def __init__(self):
        """Initialize PowerShell integration"""
        self._config = _config

    def execute_script(self, script: str, timeout: int = 30) -> Tuple[bool, str]:
        """
        Execute PowerShell script

        Args:
            script: PowerShell script content
            timeout: Timeout in seconds

        Returns:
            (success, output)
        """
        try:
            creationflags = self._config.get_subprocess_flags() if self._config else 0
            result = subprocess.run(
                ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', script],
                capture_output=True,
                text=True,
                shell=False,
                timeout=timeout,
                creationflags=creationflags
            )

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr

        except subprocess.TimeoutExpired:
            return False, f"PowerShell script execution timeout after {timeout} seconds"
        except Exception as e:
            return False, f"PowerShell execution error: {str(e)}"

    def check_execution_policy(self) -> str:
        """
        Check current PowerShell execution policy

        Returns:
            str: Execution policy name (LocalMachine, Effective, etc.)
        """
        try:
            # Check LocalMachine scope first
            creationflags = self._config.get_subprocess_flags() if self._config else 0
            result = subprocess.run(
                ['powershell', '-Command', 'Get-ExecutionPolicy -Scope LocalMachine'],
                capture_output=True,
                text=True,
                shell=False,
                creationflags=creationflags
            )

            localmachine_policy = result.stdout.strip()

            # Also check effective policy
            effective_result = subprocess.run(
                ['powershell', '-Command', 'Get-ExecutionPolicy'],
                capture_output=True,
                text=True,
                shell=False,
                creationflags=creationflags
            )

            effective_policy = effective_result.stdout.strip()

            return f"LocalMachine: {localmachine_policy}, Effective: {effective_policy}"

        except Exception as e:
            return f"Error checking execution policy: {str(e)}"

    def set_execution_policy(self, policy: str = 'RemoteSigned',
                           scope: str = 'LocalMachine') -> bool:
        """
        Set PowerShell execution policy

        Args:
            policy: Policy to set (RemoteSigned, Unrestricted, etc.)
            scope: Scope to apply (LocalMachine, CurrentUser)

        Returns:
            bool: True if successful
        """
        try:
            print(f"{scope} 범위에서 PowerShell 실행 정책을 {policy}로 설정하는 중...")

            creationflags = self._config.get_subprocess_flags() if self._config else 0
            result = subprocess.run(
                ['powershell', '-Command',
                 f'Set-ExecutionPolicy -ExecutionPolicy {policy} -Scope {scope} -Force'],
                capture_output=True,
                text=True,
                shell=False,
                creationflags=creationflags
            )

            if result.returncode == 0:
                print(f"[OK] PowerShell 실행 정책이 {policy}({scope})로 업데이트되었습니다")
                return True
            else:
                error_msg = result.stderr.strip()
                print(f"[경고] {scope} 실행 정책 설정 실패: {error_msg}")
                return False

        except Exception as e:
            print(f"PowerShell 실행 정책 설정 실패: {e}")
            return False

    def ensure_execution_policy(self) -> bool:
        """
        Ensure PowerShell execution policy is set correctly
        This is crucial for npm and other script-based tools to work properly

        Returns:
            bool: True if policy is set correctly or was successfully changed
        """
        try:
            # Check current execution policy
            creationflags = self._config.get_subprocess_flags() if self._config else 0
            result = subprocess.run(
                ['powershell', '-Command', 'Get-ExecutionPolicy -Scope LocalMachine'],
                capture_output=True,
                text=True,
                shell=False,
                creationflags=creationflags
            )

            localmachine_policy = result.stdout.strip()
            print(f"LocalMachine PowerShell 실행 정책: {localmachine_policy}")

            # Also check effective policy
            effective_result = subprocess.run(
                ['powershell', '-Command', 'Get-ExecutionPolicy'],
                capture_output=True,
                text=True,
                shell=False,
                creationflags=creationflags
            )

            effective_policy = effective_result.stdout.strip()
            print(f"유효한 PowerShell 실행 정책: {effective_policy}")

            # If policies are restrictive, fix it
            if (localmachine_policy in ['Restricted', 'AllSigned', 'Undefined'] or
                effective_policy in ['Restricted', 'AllSigned']):

                print("LocalMachine 범위에서 PowerShell 실행 정책을 RemoteSigned로 설정하는 중...")
                print("이는 모든 향후 PowerShell 세션과 IDE에 적용됩니다")

                # Try LocalMachine first
                if self.set_execution_policy('RemoteSigned', 'LocalMachine'):
                    print("[OK] 모든 새로운 PowerShell 세션에서 적용됩니다")
                    return True
                else:
                    # Fallback to CurrentUser
                    print("CurrentUser 범위로 대체하는 중...")
                    if self.set_execution_policy('RemoteSigned', 'CurrentUser'):
                        print("[정보] 참고: 현재 사용자에게만 적용됩니다. LocalMachine 범위는 관리자 권한이 필요합니다")
                        return True
                    else:
                        print("[오류] 모든 범위에서 실행 정책 설정 실패")
                        return False
            else:
                print(f"[OK] PowerShell 실행 정책이 이미 {effective_policy}입니다")
                return True

        except Exception as e:
            print(f"PowerShell 실행 정책 확인/설정 실패: {e}")
            return False

    def verify_path_changes(self, added_paths: List[str]) -> bool:
        """
        Verify PATH changes via PowerShell

        Args:
            added_paths: List of paths that should be in PATH

        Returns:
            bool: True if all paths are verified in PATH
        """
        try:
            if not added_paths:
                return True

            # Build verification script
            paths_check = ','.join([f"'{p}'" for p in added_paths])

            script = f"""
            $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'Machine')
            $pathArray = $currentPath -split ';' | Where-Object {{ $_ -ne '' }}

            $pathsToCheck = @({paths_check})
            $allFound = $true

            foreach ($pathToCheck in $pathsToCheck) {{
                if ($pathArray -notcontains $pathToCheck) {{
                    Write-Host "누락: $pathToCheck"
                    $allFound = $false
                }} else {{
                    Write-Host "확인: $pathToCheck"
                }}
            }}

            if ($allFound) {{
                Write-Host "모든 경로가 PATH에 있습니다"
                exit 0
            }} else {{
                Write-Host "일부 경로가 PATH에 없습니다"
                exit 1
            }}
            """

            success, output = self.execute_script(script)
            print(output)

            return success

        except Exception as e:
            print(f"PATH 검증 실패: {e}")
            return False

    def update_path_environment(self, paths_to_add: List[str]) -> bool:
        """
        Use PowerShell to update PATH with immediate effect
        PowerShell's [Environment]::SetEnvironmentVariable has special behavior

        Args:
            paths_to_add: List of paths to add to PATH

        Returns:
            bool: True if successful
        """
        try:
            ps_script = """
        $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'Machine')
        $pathArray = $currentPath -split ';' | Where-Object { $_ -ne '' }

        $newPaths = @({paths})

        foreach ($newPath in $newPaths) {{
            if ($pathArray -notcontains $newPath) {{
                $pathArray += $newPath
                Write-Host "추가하는 중: $newPath"
            }}
        }}

        $finalPath = $pathArray -join ';'

        # This method triggers immediate propagation
        [Environment]::SetEnvironmentVariable('PATH', $finalPath, 'Machine')

        # Force refresh for current session
        $env:PATH = $finalPath + ';' + [Environment]::GetEnvironmentVariable('PATH', 'User')

        Write-Host "PATH가 성공적으로 업데이트되었습니다"
        """.format(paths="'" + "','".join(paths_to_add) + "'")

            success, output = self.execute_script(ps_script)

            if success:
                print("PowerShell PATH 업데이트 성공")
                print(output)
                return True
            else:
                print(f"PowerShell PATH 업데이트 실패: {output}")
                return False

        except Exception as e:
            print(f"PowerShell 방법 실패: {e}")
            return False


__all__ = ['PowerShellIntegration']
