"""
Registry Operations Module
Windows registry direct access for PATH management
Brain Module System v4.0
"""

import winreg
from typing import List, Optional


class RegistryOperations:
    """Low-level registry operations for PATH"""

    def __init__(self):
        """Initialize registry paths"""
        self.SYSTEM_ENV_KEY = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        self.USER_ENV_KEY = r'Environment'

    def read_system_path(self) -> List[str]:
        """
        Read system PATH from registry

        Returns:
            List of paths in system PATH, empty list if error
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.SYSTEM_ENV_KEY,
                0,
                winreg.KEY_READ
            )

            try:
                system_path, _ = winreg.QueryValueEx(key, 'Path')
                path_list = [p.strip() for p in system_path.split(';') if p.strip()]
                return path_list
            except:
                return []
            finally:
                winreg.CloseKey(key)
        except:
            return []

    def read_user_path(self) -> List[str]:
        """
        Read user PATH from registry

        Returns:
            List of paths in user PATH, empty list if error
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.USER_ENV_KEY,
                0,
                winreg.KEY_READ
            )

            try:
                user_path, _ = winreg.QueryValueEx(key, 'Path')
                path_list = [p.strip() for p in user_path.split(';') if p.strip()]
                return path_list
            except:
                return []
            finally:
                winreg.CloseKey(key)
        except:
            return []

    def write_system_path(self, paths: List[str]) -> bool:
        """
        Write system PATH to registry

        Args:
            paths: List of paths to write to system PATH

        Returns:
            True if successful, False otherwise
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                self.SYSTEM_ENV_KEY,
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )

            # Join paths with semicolon
            new_path_value = ';'.join(paths)

            # Write to registry using REG_EXPAND_SZ type
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path_value)
            winreg.CloseKey(key)

            return True

        except PermissionError:
            print("[ERROR] Permission denied. System PATH requires administrator privileges.")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to write system PATH: {e}")
            return False

    def write_user_path(self, paths: List[str]) -> bool:
        """
        Write user PATH to registry

        Args:
            paths: List of paths to write to user PATH

        Returns:
            True if successful, False otherwise
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.USER_ENV_KEY,
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )

            # Join paths with semicolon
            new_path_value = ';'.join(paths)

            # Write to registry using REG_EXPAND_SZ type
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path_value)
            winreg.CloseKey(key)

            return True

        except PermissionError:
            print("[ERROR] Permission denied. Cannot write to user PATH.")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to write user PATH: {e}")
            return False

    def write_environment_variable(
        self,
        name: str,
        value: str,
        user: bool = False
    ) -> bool:
        """
        Write environment variable to registry

        Args:
            name: Environment variable name
            value: Environment variable value
            user: If True, write to user environment; if False, write to system

        Returns:
            True if successful, False otherwise
        """
        try:
            if user:
                key_path = self.USER_ENV_KEY
                root_key = winreg.HKEY_CURRENT_USER
            else:
                key_path = self.SYSTEM_ENV_KEY
                root_key = winreg.HKEY_LOCAL_MACHINE

            key = winreg.OpenKey(
                root_key,
                key_path,
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )

            # Write to registry using REG_SZ type
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
            winreg.CloseKey(key)

            scope = "user" if user else "system"
            print(f"[OK] Environment variable set ({scope}): {name} = {value}")
            return True

        except PermissionError:
            scope = "user" if user else "system"
            print(f"[ERROR] Permission denied. Cannot write to {scope} environment.")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to set environment variable {name}: {e}")
            return False

    def read_environment_variable(
        self,
        name: str,
        user: bool = False
    ) -> Optional[str]:
        """
        Read environment variable from registry

        Args:
            name: Environment variable name
            user: If True, read from user environment; if False, read from system

        Returns:
            Variable value if found, None otherwise
        """
        try:
            if user:
                key_path = self.USER_ENV_KEY
                root_key = winreg.HKEY_CURRENT_USER
            else:
                key_path = self.SYSTEM_ENV_KEY
                root_key = winreg.HKEY_LOCAL_MACHINE

            key = winreg.OpenKey(
                root_key,
                key_path,
                0,
                winreg.KEY_READ
            )

            try:
                value, _ = winreg.QueryValueEx(key, name)
                return value
            except:
                return None
            finally:
                winreg.CloseKey(key)

        except:
            return None

    def delete_environment_variable(
        self,
        name: str,
        user: bool = False
    ) -> bool:
        """
        Delete environment variable from registry

        Args:
            name: Environment variable name to delete
            user: If True, delete from user environment; if False, delete from system

        Returns:
            True if successful, False otherwise
        """
        try:
            if user:
                key_path = self.USER_ENV_KEY
                root_key = winreg.HKEY_CURRENT_USER
            else:
                key_path = self.SYSTEM_ENV_KEY
                root_key = winreg.HKEY_LOCAL_MACHINE

            key = winreg.OpenKey(
                root_key,
                key_path,
                0,
                winreg.KEY_READ | winreg.KEY_WRITE
            )

            # Delete the value
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)

            scope = "user" if user else "system"
            print(f"[OK] Environment variable deleted ({scope}): {name}")
            return True

        except FileNotFoundError:
            print(f"[INFO] Environment variable not found: {name}")
            return False
        except PermissionError:
            scope = "user" if user else "system"
            print(f"[ERROR] Permission denied. Cannot delete from {scope} environment.")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to delete environment variable {name}: {e}")
            return False


__all__ = ['RegistryOperations']
