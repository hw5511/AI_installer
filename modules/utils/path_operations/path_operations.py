"""
Path Operations Module - Main
High-level PATH management API
Brain Module System v4.0
"""

import os
import time
import subprocess
import winreg
import ctypes
from typing import List, Optional, Dict
from .registry_operations import RegistryOperations
from .broadcast_manager import BroadcastManager
from .powershell_integration import PowerShellIntegration

# Import Config for production mode detection with safe initialization
try:
    from modules.core.config import Config
    _config = Config()
except Exception:
    # Fallback if Config is not available or initialization fails
    _config = None


class PathOperations:
    """High-level PATH management combining all components"""

    def __init__(self):
        """Initialize with all PATH operation components"""
        self.registry_ops = RegistryOperations()
        self.broadcast_mgr = BroadcastManager()
        self.powershell = PowerShellIntegration()

    def add_to_system_path(self, path: str) -> bool:
        """
        Add path to system PATH (basic mode)

        Args:
            path: Path to add to system PATH

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read current system PATH
            path_list = self.registry_ops.read_system_path()

            # Check if path already exists
            if path in path_list:
                print(f"{path}는 이미 시스템 PATH에 있습니다")
                return True

            # Add the new path
            path_list.append(path)

            # Write back to registry
            if not self.registry_ops.write_system_path(path_list):
                return False

            # Broadcast environment change
            self.broadcast_mgr.broadcast_environment_change()

            print(f"시스템 PATH에 {path}를 성공적으로 추가했습니다")
            return True

        except Exception as e:
            print(f"시스템 PATH 추가 실패: {e}")
            return False

    def add_multiple_paths_to_system_path(self, new_paths: List[str]) -> bool:
        """
        Add multiple directories to the system PATH environment variable

        Args:
            new_paths: List of paths to add to system PATH

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read current system PATH
            path_list = self.registry_ops.read_system_path()

            added_paths = []
            for new_path in new_paths:
                if new_path not in path_list:
                    path_list.append(new_path)
                    added_paths.append(new_path)
                    print(f"시스템 PATH에 {new_path} 추가하는 중")
                else:
                    print(f"{new_path}는 이미 시스템 PATH에 있습니다")

            if added_paths:
                # Write back to registry
                if not self.registry_ops.write_system_path(path_list):
                    return False

                # Broadcast environment change
                self.broadcast_mgr.broadcast_environment_change()

                print(f"시스템 PATH에 {len(added_paths)}개의 경로를 성공적으로 추가했습니다")
                return True
            else:
                print("모든 경로가 이미 시스템 PATH에 있습니다")
                return True

        except Exception as e:
            print(f"시스템 PATH 추가 실패: {e}")
            return False

    def add_to_path_immediate(self, paths) -> bool:
        """
        Add paths with immediate effect across all new processes (enhanced mode)

        Args:
            paths: Single path or list of paths to add

        Returns:
            bool: Success status
        """
        if not paths:
            return False

        if isinstance(paths, str):
            paths = [paths]

        print(f"{len(paths)}개의 경로를 즉시 적용하여 추가하는 중...")

        # First, ensure PowerShell execution policy is set correctly
        self.powershell.ensure_execution_policy()

        # Try PowerShell method first (most reliable)
        success = self.powershell.update_path_environment(paths)

        if not success:
            # Fallback to enhanced registry method
            success = self._update_path_with_immediate_effect(paths)

        # Always refresh current process
        self._refresh_current_process_path()

        # Verify propagation
        if success:
            time.sleep(2)  # Give system time to propagate

            # Test with a simple command
            test_result = self._verify_path_propagation('where')
            if test_result:
                print("[OK] PATH 변경사항이 성공적으로 전파되었습니다!")
            else:
                print("[!] PATH가 업데이트되었지만 완전한 적용을 위해 탐색기 재시작이 필요할 수 있습니다")

        return success

    def remove_from_path(self, path: str) -> bool:
        """
        Remove path from system PATH

        Args:
            path: Path to remove from system PATH

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read current system PATH
            path_list = self.registry_ops.read_system_path()

            # Check if path exists
            if path not in path_list:
                print(f"{path}는 시스템 PATH에 없습니다")
                return True

            # Remove the path
            path_list.remove(path)

            # Write back to registry
            if not self.registry_ops.write_system_path(path_list):
                return False

            # Broadcast environment change
            self.broadcast_mgr.broadcast_environment_change()

            print(f"시스템 PATH에서 {path}를 성공적으로 제거했습니다")
            return True

        except Exception as e:
            print(f"시스템 PATH 제거 실패: {e}")
            return False

    def get_current_path(self) -> List[str]:
        """
        Get current system PATH

        Returns:
            List[str]: List of paths in system PATH
        """
        return self.registry_ops.read_system_path()

    def check_path_in_environment(self, target_path: str, case_sensitive: bool = False) -> Dict:
        """
        Check if a path exists in the current environment PATH

        Args:
            target_path: Path to check
            case_sensitive: Whether to perform case-sensitive comparison

        Returns:
            Dictionary with 'in_system_path', 'in_user_path', 'in_current_path'
        """
        system_paths = self.registry_ops.read_system_path()
        user_paths = self.registry_ops.read_user_path()
        current_path = os.environ.get('PATH', '').split(';')

        if not case_sensitive:
            target_path = target_path.lower()
            system_paths = [p.lower() for p in system_paths]
            user_paths = [p.lower() for p in user_paths]
            current_path = [p.lower() for p in current_path]

        return {
            'in_system_path': target_path in system_paths,
            'in_user_path': target_path in user_paths,
            'in_current_path': target_path in current_path
        }

    def refresh_environment_variables(self) -> bool:
        """
        Refresh environment variables for the current process

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Refresh PATH from registry
            system_path = self.registry_ops.read_system_path()
            user_path = self.registry_ops.read_user_path()

            # Combine paths
            combined_path = []
            if system_path:
                combined_path.extend(system_path)
            if user_path:
                combined_path.extend(user_path)

            # Update current process PATH
            if combined_path:
                os.environ['PATH'] = ';'.join(combined_path)

            return True
        except Exception as e:
            print(f"환경 변수 새로고침 실패: {e}")
            return False

    # Private helper methods

    def _update_path_with_immediate_effect(self, new_paths: List[str]) -> bool:
        """
        Update PATH and ensure immediate availability in new processes

        Args:
            new_paths: List of paths to add

        Returns:
            bool: Success status
        """
        try:
            # Read current system PATH
            path_list = self.registry_ops.read_system_path()

            added = False
            for new_path in new_paths:
                if new_path not in path_list:
                    path_list.append(new_path)
                    added = True
                    print(f"PATH에 추가하는 중: {new_path}")

            if added:
                # Write back to registry
                if not self.registry_ops.write_system_path(path_list):
                    return False

                # Force Explorer to reload
                self._force_refresh_explorer_environment()

                # Enhanced broadcast
                self.broadcast_mgr.broadcast_environment_change_enhanced()

                print("PATH가 즉시 적용되도록 업데이트되었습니다")
                return True
            else:
                print("모든 경로가 이미 PATH에 있습니다")
                return True

        except Exception as e:
            print(f"PATH 업데이트 실패: {e}")
            return False

    def _force_refresh_explorer_environment(self) -> bool:
        """
        Force Explorer.exe to reload environment variables
        This affects all new processes spawned from Explorer
        """
        try:
            # Method 1: Use setx to trigger system-wide refresh
            # setx creates a permanent change AND notifies the system
            dummy_var = f"TEMP_REFRESH_{int(time.time())}"
            creationflags = _config.get_subprocess_flags() if _config else 0
            subprocess.run(
                ['setx', dummy_var, 'refresh'],
                capture_output=True,
                shell=True,
                timeout=5,
                creationflags=creationflags
            )

            # Clean up the dummy variable
            subprocess.run(
                ['reg', 'delete',
                 'HKCU\\Environment',
                 '/v', dummy_var, '/f'],
                capture_output=True,
                shell=True,
                timeout=5,
                creationflags=creationflags
            )

            # Method 2: Broadcast WM_SETTINGCHANGE more aggressively
            self.broadcast_mgr.broadcast_environment_change_enhanced()

            print("탐색기 환경 새로고침이 트리거되었습니다")
            return True
        except Exception as e:
            print(f"탐색기 환경 새로고침 실패: {e}")
            return False

    def _refresh_current_process_path(self) -> bool:
        """
        Refresh PATH for the current Python process
        """
        try:
            # Get system PATH from registry
            system_path = self.registry_ops.read_system_path()
            user_path = self.registry_ops.read_user_path()

            # Combine and update current process
            combined = ';'.join(system_path)
            if user_path:
                combined = f"{combined};{';'.join(user_path)}"

            os.environ['PATH'] = combined

            print("현재 프로세스의 PATH를 새로고침했습니다")
            return True

        except Exception as e:
            print(f"현재 프로세스 PATH 새로고침 실패: {e}")
            return False

    def _verify_path_propagation(self, test_command: str = 'git') -> bool:
        """
        Test if PATH changes have propagated by spawning a test process

        Args:
            test_command: Command to test

        Returns:
            bool: True if command is accessible in new process
        """
        try:
            # Test in a completely new process
            creationflags = _config.get_subprocess_flags() if _config else 0
            result = subprocess.run(
                ['powershell', '-Command', f'(Get-Command {test_command} -ErrorAction SilentlyContinue) -ne $null'],
                capture_output=True,
                text=True,
                shell=False,
                creationflags=creationflags
            )

            return result.returncode == 0 and 'True' in result.stdout

        except Exception as e:
            print(f"검증 실패: {e}")
            return False

    def add_to_user_path_immediate(self, paths) -> bool:
        """
        Add paths to User PATH with immediate effect

        This method modifies HKEY_CURRENT_USER\\Environment registry
        and broadcasts WM_SETTINGCHANGE to apply changes immediately.

        Args:
            paths: Single path string or list of paths to add

        Returns:
            bool: True if successful, False otherwise

        Features:
            - Supports environment variable expansion (%APPDATA%, etc.)
            - Converts AppData\\Roaming paths to %APPDATA% format
            - Checks for duplicates (case-insensitive)
            - Broadcasts WM_SETTINGCHANGE for immediate effect
        """
        # Broadcast constants
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002

        try:
            # Handle input: convert single path to list
            if isinstance(paths, str):
                paths = [paths]

            if not paths:
                print("추가할 경로가 제공되지 않았습니다")
                return False

            # Open User Environment registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Environment',
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )

            try:
                # Read current PATH
                current_path, reg_type = winreg.QueryValueEx(key, 'Path')

                # Parse current PATH into list
                current_paths = [p.strip() for p in current_path.split(';') if p.strip()]

                # Convert paths for case-insensitive comparison
                current_paths_lower = [p.lower() for p in current_paths]

                added_count = 0
                skipped_count = 0

                for new_path in paths:
                    # Convert AppData\Roaming to %APPDATA% format
                    new_path = new_path.strip()
                    appdata_roaming = os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Roaming')

                    if new_path.lower().startswith(appdata_roaming.lower()):
                        # Replace AppData\Roaming with %APPDATA%
                        relative_part = new_path[len(appdata_roaming):].lstrip('\\/')
                        new_path = os.path.join('%APPDATA%', relative_part)
                        print(f"환경변수 형식으로 변환: {new_path}")

                    # Check for duplicates (case-insensitive)
                    if new_path.lower() in current_paths_lower:
                        print(f"이미 User PATH에 존재: {new_path}")
                        skipped_count += 1
                        continue

                    # Add new path
                    current_paths.append(new_path)
                    current_paths_lower.append(new_path.lower())
                    print(f"User PATH에 추가: {new_path}")
                    added_count += 1

                # Write back to registry if any paths were added
                if added_count > 0:
                    # Join paths with semicolon
                    new_path_value = ';'.join(current_paths)

                    # Use REG_EXPAND_SZ to support environment variable expansion
                    winreg.SetValueEx(
                        key,
                        'Path',
                        0,
                        winreg.REG_EXPAND_SZ,
                        new_path_value
                    )

                    print(f"\nUser PATH 레지스트리 업데이트 완료 ({added_count}개 추가)")

                    # Broadcast WM_SETTINGCHANGE for immediate effect
                    result = ctypes.c_long()
                    ctypes.windll.user32.SendMessageTimeoutW(
                        HWND_BROADCAST,
                        WM_SETTINGCHANGE,
                        0,
                        'Environment',
                        SMTO_ABORTIFHUNG,
                        5000,
                        ctypes.byref(result)
                    )

                    print("WM_SETTINGCHANGE 브로드캐스트 완료")
                    print("\n[안내] 변경사항은 새로운 프로세스에 즉시 적용됩니다.")
                    print("[안내] VSCode에서 변경사항을 확인하려면 VSCode를 재시작하세요.")

                else:
                    print(f"\n모든 경로가 이미 User PATH에 존재합니다 (건너뜀: {skipped_count}개)")

            finally:
                winreg.CloseKey(key)

            return True

        except PermissionError:
            print("\n[오류] User PATH 수정 권한이 없습니다")
            print("       일반적으로 User PATH는 관리자 권한 없이 수정 가능합니다")
            return False

        except Exception as e:
            print(f"\n[오류] User PATH 추가 실패: {e}")
            import traceback
            traceback.print_exc()
            return False


def add_to_user_path_immediate(paths) -> bool:
    """
    Add paths to User PATH with immediate effect

    This function modifies HKEY_CURRENT_USER\\Environment registry
    and broadcasts WM_SETTINGCHANGE to apply changes immediately.

    Args:
        paths: Single path string or list of paths to add

    Returns:
        bool: True if successful, False otherwise

    Features:
        - Supports environment variable expansion (%APPDATA%, etc.)
        - Converts AppData\\Roaming paths to %APPDATA% format
        - Checks for duplicates (case-insensitive)
        - Broadcasts WM_SETTINGCHANGE for immediate effect
    """
    # Broadcast constants
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002

    try:
        # Handle input: convert single path to list
        if isinstance(paths, str):
            paths = [paths]

        if not paths:
            print("추가할 경로가 제공되지 않았습니다")
            return False

        # Open User Environment registry key
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Environment',
            0,
            winreg.KEY_READ | winreg.KEY_WRITE
        )

        try:
            # Read current PATH
            current_path, reg_type = winreg.QueryValueEx(key, 'Path')

            # Parse current PATH into list
            current_paths = [p.strip() for p in current_path.split(';') if p.strip()]

            # Convert paths for case-insensitive comparison
            current_paths_lower = [p.lower() for p in current_paths]

            added_count = 0
            skipped_count = 0

            for new_path in paths:
                # Convert AppData\Roaming to %APPDATA% format
                new_path = new_path.strip()
                appdata_roaming = os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Roaming')

                if new_path.lower().startswith(appdata_roaming.lower()):
                    # Replace AppData\Roaming with %APPDATA%
                    relative_part = new_path[len(appdata_roaming):].lstrip('\\/')
                    new_path = os.path.join('%APPDATA%', relative_part)
                    print(f"환경변수 형식으로 변환: {new_path}")

                # Check for duplicates (case-insensitive)
                if new_path.lower() in current_paths_lower:
                    print(f"이미 User PATH에 존재: {new_path}")
                    skipped_count += 1
                    continue

                # Add new path
                current_paths.append(new_path)
                current_paths_lower.append(new_path.lower())
                print(f"User PATH에 추가: {new_path}")
                added_count += 1

            # Write back to registry if any paths were added
            if added_count > 0:
                # Join paths with semicolon
                new_path_value = ';'.join(current_paths)

                # Use REG_EXPAND_SZ to support environment variable expansion
                winreg.SetValueEx(
                    key,
                    'Path',
                    0,
                    winreg.REG_EXPAND_SZ,
                    new_path_value
                )

                print(f"\nUser PATH 레지스트리 업데이트 완료 ({added_count}개 추가)")

                # Broadcast WM_SETTINGCHANGE for immediate effect
                result = ctypes.c_long()
                ctypes.windll.user32.SendMessageTimeoutW(
                    HWND_BROADCAST,
                    WM_SETTINGCHANGE,
                    0,
                    'Environment',
                    SMTO_ABORTIFHUNG,
                    5000,
                    ctypes.byref(result)
                )

                print("WM_SETTINGCHANGE 브로드캐스트 완료")
                print("\n[안내] 변경사항은 새로운 프로세스에 즉시 적용됩니다.")
                print("[안내] VSCode에서 변경사항을 확인하려면 VSCode를 재시작하세요.")

            else:
                print(f"\n모든 경로가 이미 User PATH에 존재합니다 (건너뜀: {skipped_count}개)")

        finally:
            winreg.CloseKey(key)

        return True

    except PermissionError:
        print("\n[오류] User PATH 수정 권한이 없습니다")
        print("       일반적으로 User PATH는 관리자 권한 없이 수정 가능합니다")
        return False

    except Exception as e:
        print(f"\n[오류] User PATH 추가 실패: {e}")
        import traceback
        traceback.print_exc()
        return False


__all__ = ['PathOperations']
