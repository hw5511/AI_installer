"""
System Utility Functions for AI Setup Application
Administrator privileges and system software checks
"""
import subprocess
import ctypes
import sys
import os
import platform

# Import Config for production mode detection
try:
    from modules.core.config import Config
    _config = Config()
except Exception:
    # Fallback if Config is not available or initialization fails
    _config = None


def is_admin():
    """
    Check if the current process has administrator privileges

    Returns:
        bool: True if running as administrator, False otherwise
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin(command):
    """
    Execute a command with administrator privileges

    Args:
        command (str): Command to execute as administrator

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if isinstance(command, list):
            command = ' '.join(command)

        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "cmd.exe", f"/c {command}", None, 1
        )
        return True
    except Exception as e:
        print(f"관리자 권한으로 명령 실행 실패: {e}")
        return False


def restart_as_admin(script_path=None):
    """
    Restart the current script with administrator privileges

    Args:
        script_path (str): Path to the script to restart (defaults to current script)

    Returns:
        None: This function will exit the current process
    """
    if script_path is None:
        script_path = os.path.abspath(__file__)

    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script_path}"', None, 1
        )
        sys.exit(0)
    except Exception as e:
        print(f"관리자 권한으로 재시작 실패: {e}")
        sys.exit(1)


def check_software_installed(software_name, command_args, timeout=5):
    """
    Generic function to check if software is installed by running a command

    Args:
        software_name (str): Name of the software for display purposes
        command_args (list): Command and arguments to check software (e.g., ['git', '--version'])
        timeout (int): Timeout in seconds for the command

    Returns:
        tuple: (bool, str) - (is_installed, version_or_error)
    """
    try:
        # Get subprocess flags based on production mode
        creationflags = _config.get_subprocess_flags() if _config else 0

        result = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            shell=True,
            timeout=timeout,
            creationflags=creationflags
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, None
    except subprocess.TimeoutExpired:
        return False, f"명령이 {timeout}초 후 시간 초과되었습니다"
    except Exception as e:
        return False, str(e)


def check_package_manager(manager_type):
    """
    Check if a package manager is available

    Args:
        manager_type (str): Type of package manager ('winget', 'choco', 'npm')

    Returns:
        bool: True if package manager is available, False otherwise
    """
    commands = {
        'winget': ['winget', '--version'],
        'choco': ['choco', '--version'],
        'npm': ['npm', '--version']
    }

    if manager_type not in commands:
        return False

    try:
        # Get subprocess flags based on production mode
        creationflags = _config.get_subprocess_flags() if _config else 0

        result = subprocess.run(
            commands[manager_type],
            capture_output=True,
            text=True,
            shell=True,
            timeout=5,
            creationflags=creationflags
        )
        return result.returncode == 0
    except:
        return False


def run_command_with_timeout(command, timeout=5, shell=True):
    """
    Run a command with a specified timeout

    Args:
        command (list or str): Command to run
        timeout (int): Timeout in seconds
        shell (bool): Whether to use shell

    Returns:
        tuple: (success, stdout, stderr, returncode)
    """
    try:
        # Get subprocess flags based on production mode
        creationflags = _config.get_subprocess_flags() if _config else 0

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=shell,
            timeout=timeout,
            creationflags=creationflags
        )
        return True, result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return False, "", f"명령이 {timeout}초 후 시간 초과되었습니다", -1
    except Exception as e:
        return False, "", str(e), -1


def check_multiple_software_installations(software_configs):
    """
    Check multiple software installations at once

    Args:
        software_configs (list): List of dictionaries with 'name' and 'command' keys

    Returns:
        dict: Dictionary mapping software names to (installed, version) tuples
    """
    results = {}

    for config in software_configs:
        name = config.get('name')
        command = config.get('command')
        timeout = config.get('timeout', 5)

        if name and command:
            installed, version = check_software_installed(name, command, timeout)
            results[name] = (installed, version)

    return results


def find_executable_in_common_paths(executable_name, common_paths):
    """
    Find an executable in common installation paths

    Args:
        executable_name (str): Name of the executable file
        common_paths (list): List of common paths to search

    Returns:
        str or None: Path to the executable if found, None otherwise
    """
    for path in common_paths:
        exe_path = os.path.join(path, executable_name)
        if os.path.exists(exe_path):
            return path
    return None


def search_drives_for_executable(executable_name, search_subdirs):
    """
    Search multiple drives for an executable in specified subdirectories

    Args:
        executable_name (str): Name of the executable file
        search_subdirs (list): List of subdirectories to search in each drive

    Returns:
        str or None: Path to the directory containing the executable if found, None otherwise
    """
    for drive in ['C:', 'D:', 'E:']:
        for subdir in search_subdirs:
            search_path = os.path.join(drive, subdir)
            exe_path = os.path.join(search_path, executable_name)
            if os.path.exists(exe_path):
                return search_path
    return None


def ensure_directory_exists(directory_path):
    """
    Ensure a directory exists, creating it if necessary

    Args:
        directory_path (str): Path to the directory

    Returns:
        bool: True if directory exists or was created successfully, False otherwise
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
            print(f"디렉토리 생성됨: {directory_path}")
        return True
    except Exception as e:
        print(f"디렉토리 생성 실패 {directory_path}: {e}")
        return False


def get_windows_version():
    """
    Get Windows version information

    Returns:
        dict: Dictionary with version information
    """
    try:
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    except Exception as e:
        print(f"Windows 버전 정보 가져오기 실패: {e}")
        return {}