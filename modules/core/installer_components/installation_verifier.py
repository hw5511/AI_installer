"""
Installation Verifier Module
Verifies installation and manages PATH
Brain Module System v4.0
"""

import os
import subprocess
from typing import Optional, Callable, List
from modules.utils.path_manager import add_to_path_immediate, add_to_system_path
from modules.utils.path_verifier import PathVerifier


class InstallationVerifier:
    """Verifies installation and manages PATH"""

    def __init__(self, config=None, log_callback: Optional[Callable] = None):
        self.config = config
        self.log_callback = log_callback or print
        self.common_paths = {
            'git': [r"C:\Program Files\Git\cmd", r"C:\Program Files\Git\bin",
                   r"C:\Program Files (x86)\Git\cmd", r"C:\Program Files (x86)\Git\bin"],
            'nodejs': [r"C:\Program Files\nodejs", r"C:\Program Files (x86)\nodejs"]
        }

    def _log(self, message: str) -> None:
        self.log_callback(message)

    def verify_installation(self, software: str) -> tuple[bool, str]:
        """Enhanced verification with PATH update and new-process validation"""
        tool_mapping = {'git': 'Git', 'nodejs': 'Node.js', 'npm': 'NPM',
                       'claude': 'Claude CLI', 'gemini': 'Gemini CLI'}

        if self._check_software_installed(software):
            self._log(f"{software} 설치가 현재 프로세스에서 확인되었습니다")
            verifier = PathVerifier(log_callback=self._log)
            tool_name = tool_mapping.get(software, software)
            self._log(f"새 프로세스에서 {tool_name}를 확인하는 중...")

            result = verifier.verify_single_tool(tool_name, {
                'command': software if software != 'nodejs' else 'node',
                'args': ['--version']
            })

            if result['status'] == 'success':
                self._log(f"[확인] {software}가 새 프로세스에서 확인되었습니다: {result['version']}")
                return True, f"{software} 설치가 확인되었으며 새 프로세스에서 작동합니다"
            else:
                self._log(f"[!] {software}가 새 프로세스에서 접근할 수 없습니다. PATH 수정을 시도하는 중...")

        install_path = self.find_installation_path(software)
        if install_path:
            self._log(f"{software}를 다음 위치에서 찾았습니다: {install_path}")
            self._log(f"시스템 PATH에 추가하는 중...")

            if self.add_to_path([install_path]):
                self._log(f"{software}에 대한 PATH가 업데이트되었습니다")
                verifier = PathVerifier(log_callback=self._log)
                tool_name = tool_mapping.get(software, software)
                self._log(f"PATH 업데이트 후 {tool_name}를 다시 확인하는 중...")

                result = verifier.verify_single_tool(tool_name, {
                    'command': software if software != 'nodejs' else 'node',
                    'args': ['--version']
                })

                if result['status'] == 'success':
                    self._log(f"[확인] {software}가 이제 새 프로세스에서 접근 가능합니다: {result['version']}")
                    return True, f"{software} 설치가 PATH 업데이트 후 확인되었습니다"
                else:
                    warning_msg = f"{software}가 설치되었지만 터미널 재시작이 필요할 수 있습니다"
                    self._log(f"[!] {warning_msg}")
                    return True, warning_msg
            else:
                self._log(f"[!] {software}에 대한 PATH 업데이트에 실패했습니다")

        warning_msg = f"{software}가 설치되었지만 PATH에서 찾을 수 없습니다. 터미널을 재시작하세요."
        self._log(warning_msg)
        return True, warning_msg

    def find_installation_path(self, software: str) -> Optional[str]:
        """Find installation path for software"""
        if software not in self.common_paths:
            return None

        for path in self.common_paths[software]:
            exe_name = 'git.exe' if software == 'git' else 'node.exe'
            if os.path.exists(os.path.join(path, exe_name)):
                return path
        return None

    def add_to_path(self, paths: List[str]) -> bool:
        """Add directories to system PATH with immediate effect"""
        if isinstance(paths, str):
            paths = [paths]

        valid_paths = [p for p in paths if os.path.exists(p)]
        if not valid_paths:
            self._log("PATH에 추가할 유효한 경로가 없습니다")
            return False

        try:
            self._log(f"향상된 PATH 관리자를 사용하여 {len(valid_paths)}개의 경로를 추가하는 중")
            success = add_to_path_immediate(valid_paths)

            if success:
                self._log("[확인] PATH가 모든 새 프로세스에 즉시 적용되어 업데이트되었습니다")
                self._log("  새로운 터미널/VSCode에서 즉시 접근할 수 있습니다")
            else:
                self._log("[!] 향상된 PATH 업데이트가 실패했습니다. 대체 방법을 사용합니다")
                added_any = False
                for path in valid_paths:
                    try:
                        if add_to_system_path(path):
                            self._log(f"{path}를 시스템 PATH에 추가했습니다")
                            added_any = True
                        current_path = os.environ.get('PATH', '')
                        if path not in current_path:
                            os.environ['PATH'] = f"{path};{current_path}"
                    except Exception as e:
                        self._log(f"{path}를 PATH에 추가하는데 실패했습니다: {str(e)}")

                if added_any:
                    self._log("[!] PATH가 업데이트되었지만 새 터미널은 재시작이 필요할 수 있습니다")
                    self._log("  실행: $env:PATH = [System.Environment]::GetEnvironmentVariable('PATH','Machine')")
                    success = added_any
            return success

        except Exception as e:
            self._log(f"PATH 업데이트 중 오류 발생: {str(e)}")
            for path in valid_paths:
                current_path = os.environ.get('PATH', '')
                if path not in current_path:
                    os.environ['PATH'] = f"{path};{current_path}"
                    self._log(f"{path}를 현재 세션에만 추가했습니다")
            return False

    def _check_software_installed(self, software: str) -> bool:
        """Check if software is already installed"""
        commands = {
            'git': ['git', '--version'],
            'nodejs': ['node', '--version'],
            'npm': ['npm', '--version'],
            'claude': ['claude', '--version'],
            'gemini': ['gemini', '--version']
        }

        if software not in commands:
            return False

        try:
            creationflags = self.config.get_subprocess_flags() if self.config else 0
            result = subprocess.run(commands[software], capture_output=True,
                                   text=True, timeout=10, shell=True,
                                   creationflags=creationflags)
            return result.returncode == 0
        except:
            return False


__all__ = ['InstallationVerifier']
