"""
Installation Step Executor Module
Executes each installation step with progress tracking
Brain Module System v4.0
"""

import time
import subprocess
from typing import Callable, Optional, List
import traceback

from modules.core.installer import Installer
from modules.core.status_checker import StatusChecker
from modules.utils.path_verifier import PathVerifier
from modules.utils.path_manager import add_to_path_immediate, add_to_user_path_immediate, refresh_environment_variables


class InstallationStepExecutor:
    """Handles execution of individual installation steps"""

    def __init__(self,
                 installer: Installer,
                 status_checker: StatusChecker,
                 path_verifier: PathVerifier,
                 progress_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None,
                 error_logger: Optional[object] = None):
        """
        Initialize step executor

        Args:
            installer: Installer instance
            status_checker: StatusChecker instance
            path_verifier: PathVerifier instance
            progress_callback: Callback for progress updates
            log_callback: Callback for log messages
            error_logger: Error logger instance for detailed error tracking
        """
        self.installer = installer
        self.status_checker = status_checker
        self.path_verifier = path_verifier
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.error_logger = error_logger

        self.stop_flag = False

    def _log(self, message: str):
        """Log a message"""
        if self.log_callback:
            self.log_callback(message)

    def _update_progress(self, progress: float, message: str):
        """Update progress"""
        if self.progress_callback:
            self.progress_callback(progress, message)

    def set_stop_flag(self, value: bool):
        """Set stop flag"""
        self.stop_flag = value

    def _check_stop(self) -> bool:
        """Check if stop was requested"""
        if self.stop_flag:
            self._log("설치 중단 요청됨")
            self._update_progress(0, "설치 중단됨")
            return True
        return False

    def _refresh_environment(self):
        """Refresh environment variables"""
        try:
            # PowerShell 환경변수 갱신
            refresh_environment_variables()

            # Chocolatey refreshenv 명령어 (무음 실행)
            subprocess.run(
                ['powershell', '-Command', 'refreshenv'],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            self._log("환경변수가 갱신되었습니다")

        except Exception as e:
            self._log(f"환경변수 갱신 중 오류: {str(e)}")

    def _ensure_tool_in_path(self, tool_name: str, executable_paths: List[str], check_command: str = None) -> bool:
        """
        도구가 설치되었을 때 PATH 확인 및 조건부 추가

        Args:
            tool_name: 도구 이름 (로그 출력용, 예: "Git")
            executable_paths: System PATH에 추가할 경로 리스트
            check_command: PATH 확인용 명령어 (기본값: tool_name.lower())

        Returns:
            bool: PATH에서 실행 가능하면 True, 추가 실패 시 False

        동작:
            1. PATH에서 명령어 실행 시도 (--version)
            2. 성공하면 True 반환 (이미 PATH에 있음)
            3. 실패하면 executable_paths를 System PATH에 추가
            4. 2초 대기 후 재확인
            5. 성공하면 True, 실패해도 경고만 하고 True 반환 (설치는 완료된 상태)
        """
        # 기본 명령어 설정
        if check_command is None:
            check_command = tool_name.lower()

        # 1단계: 현재 PATH에서 명령어 실행 시도
        self._log(f"{tool_name} PATH 확인 중...")
        try:
            result = subprocess.run(
                [check_command, '--version'],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            if result.returncode == 0:
                self._log(f"{tool_name}이(가) 이미 PATH에 있습니다")
                return True

        except FileNotFoundError:
            self._log(f"{tool_name}이(가) PATH에서 발견되지 않음 - PATH 추가 시도...")

        except subprocess.TimeoutExpired:
            self._log(f"{tool_name} 명령어 실행 시간 초과 - PATH 추가 시도...")

        except Exception as e:
            self._log(f"{tool_name} 확인 중 오류 발생: {str(e)} - PATH 추가 시도...")

        # 2단계: PATH에 추가
        self._log(f"{tool_name} PATH 추가 중...")
        try:
            if add_to_path_immediate(executable_paths):
                self._log(f"{tool_name} PATH 추가 완료")
            else:
                self._log(f"[경고] {tool_name} PATH 추가 실패 - 레지스트리 오류 가능성")
                return False

        except Exception as e:
            self._log(f"[오류] {tool_name} PATH 추가 중 예외 발생: {str(e)}")
            return False

        # 3단계: 2초 대기 후 재확인
        self._log(f"{tool_name} PATH 반영 대기 중...")
        time.sleep(2)

        try:
            result = subprocess.run(
                [check_command, '--version'],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            if result.returncode == 0:
                self._log(f"{tool_name} PATH 설정 및 확인 완료")
                return True
            else:
                self._log(f"[경고] {tool_name} PATH 추가했으나 명령어 실행 실패 - 재로그인 필요 가능성")
                return True  # 설치는 완료된 상태

        except FileNotFoundError:
            self._log(f"[경고] {tool_name} PATH 추가했으나 아직 인식 안 됨 - 재로그인 또는 시스템 재시작 필요")
            return True  # 설치는 완료된 상태

        except subprocess.TimeoutExpired:
            self._log(f"[경고] {tool_name} 명령어 실행 시간 초과 - 재로그인 필요 가능성")
            return True  # 설치는 완료된 상태

        except Exception as e:
            self._log(f"[경고] {tool_name} 재확인 중 오류: {str(e)} - 재로그인 또는 시스템 재시작 권장")
            return True  # 설치는 완료된 상태

    def execute_step_1(self) -> bool:
        """Execute Step 1: Chocolatey installation and immediate application"""
        try:
            self._update_progress(5, "1단계: Chocolatey 설치 및 설정 - 상태 확인 중...")

            # Chocolatey 설치 여부 확인
            if self.status_checker.is_chocolatey_installed():
                self._log("Chocolatey가 이미 설치되어 있습니다")
                self._update_progress(20, "1단계 완료: Chocolatey 사용 준비됨")
                return True

            # Chocolatey 설치 시작
            self._update_progress(8, "Chocolatey 설치를 시작합니다...")
            success, message = self.installer.install_chocolatey()

            if not success:
                self._log(f"Chocolatey 설치 실패: {message}")
                self._update_progress(0, "1단계 실패: Chocolatey 설치 오류")
                return False

            self._log("Chocolatey 설치 완료")

            # 환경변수 즉시 적용
            self._update_progress(15, "환경변수 갱신 중...")
            self._refresh_environment()

            self._update_progress(20, "1단계 완료: Chocolatey 설치 및 설정 완료")
            return True

        except Exception as e:
            self._log(f"1단계 오류: {str(e)}")
            self._update_progress(0, f"1단계 실패: {str(e)}")
            return False

    def execute_step_2(self) -> bool:
        """Execute Step 2: Chocolatey detection confirmation"""
        try:
            self._update_progress(25, "2단계: Chocolatey 감지 확인 - 접근성 테스트...")

            # Chocolatey 명령어 테스트 (최대 3회 재시도)
            retry_count = 0
            max_retries = 3

            while retry_count < max_retries:
                if self._check_stop():
                    return False

                self._update_progress(25 + (retry_count * 5),
                                    f"Chocolatey 감지 시도 {retry_count + 1}/{max_retries}...")

                # 새 프로세스에서 확인
                if self.status_checker.is_chocolatey_installed():
                    self._log("Chocolatey 명령어가 정상적으로 감지되었습니다")
                    self._update_progress(40, "2단계 완료: Chocolatey 정상 동작 확인")
                    return True

                retry_count += 1
                if retry_count < max_retries:
                    self._log(f"Chocolatey 감지 실패 - {2}초 후 재시도...")
                    time.sleep(2)
                    self._refresh_environment()

            # 3회 재시도 후에도 실패
            self._log("Chocolatey 감지에 실패했습니다")
            self._log("PowerShell을 관리자 권한으로 재시작한 후 다시 시도해주세요")
            self._update_progress(0, "2단계 실패: Chocolatey 감지 불가")
            return False

        except Exception as e:
            self._log(f"2단계 오류: {str(e)}")
            self._update_progress(0, f"2단계 실패: {str(e)}")
            return False

    def execute_step_3(self) -> bool:
        """Execute Step 3: Git automatic installation"""
        try:
            self._update_progress(45, "3단계: Git 설치 및 PATH 설정 - Git 상태 확인...")

            # Git 설치 여부 확인
            if self.status_checker.is_git_installed():
                self._log("Git이 이미 설치되어 있습니다")
                git_version = self.status_checker.get_git_version()
                if git_version:
                    self._log(f"현재 Git 버전: {git_version}")

                # PATH 확인 및 조건부 추가
                self._update_progress(55, "Git PATH 확인 중...")
                git_paths = [
                    r"C:\Program Files\Git\cmd",
                    r"C:\Program Files\Git\bin",
                    r"C:\Program Files\Git\usr\bin"
                ]

                if self._ensure_tool_in_path("Git", git_paths, "git"):
                    self._log("Git PATH 설정 확인 완료")
                else:
                    self._log("[WARNING] Git PATH 설정에 문제가 있을 수 있습니다")

                self._update_progress(60, "3단계 완료: Git 사용 준비됨")
                return True

            # Git 설치 시작
            self._update_progress(48, "Git 설치를 시작합니다...")
            success, message = self.installer.install_git(method='chocolatey')

            if not success:
                self._log(f"Git 설치 실패: {message}")
                self._update_progress(0, "3단계 실패: Git 설치 오류")
                return False

            self._log("Git 설치 완료")

            # Git PATH 설정
            self._update_progress(55, "Git PATH 설정 중...")
            git_paths = [
                r"C:\Program Files\Git\cmd",
                r"C:\Program Files\Git\bin",
                r"C:\Program Files\Git\usr\bin"
            ]

            if add_to_path_immediate(git_paths):
                self._log("Git PATH 설정 완료")
            else:
                self._log("Git PATH 설정에 문제가 있을 수 있습니다")

            # 설치 검증
            self._update_progress(58, "Git 설치 검증 중...")
            if self.status_checker.is_git_installed():
                git_version = self.status_checker.get_git_version()
                self._log(f"Git 설치 검증 완료 - 버전: {git_version}")

            self._update_progress(60, "3단계 완료: Git 설치 및 PATH 설정 완료")
            return True

        except Exception as e:
            self._log(f"3단계 오류: {str(e)}")
            self._update_progress(0, f"3단계 실패: {str(e)}")
            return False

    def execute_step_4(self) -> bool:
        """Execute Step 4: Node.js automatic installation"""
        try:
            self._update_progress(65, "4단계: Node.js 설치 및 PATH 설정 - Node.js 상태 확인...")

            # Node.js 설치 여부 확인
            if self.status_checker.is_nodejs_installed():
                self._log("Node.js가 이미 설치되어 있습니다")
                node_version = self.status_checker.get_nodejs_version()
                npm_version = self.status_checker.get_npm_version()
                if node_version:
                    self._log(f"현재 Node.js 버전: {node_version}")
                if npm_version:
                    self._log(f"현재 npm 버전: {npm_version}")

                # npm PATH 확인 및 조건부 추가
                self._update_progress(75, "npm 글로벌 경로 확인 중...")
                import os
                npm_path = os.path.join(os.environ.get('APPDATA', ''), 'npm')

                if self._ensure_tool_in_path("npm", [npm_path], "npm"):
                    self._log("npm 글로벌 경로 설정 확인 완료")
                else:
                    self._log("[WARNING] npm PATH 설정에 문제가 있을 수 있습니다")

                self._update_progress(80, "4단계 완료: Node.js 사용 준비됨")
                return True

            # Node.js 설치 시작
            self._update_progress(68, "Node.js 설치를 시작합니다...")
            success, message = self.installer.install_nodejs(method='chocolatey')

            if not success:
                self._log(f"Node.js 설치 실패: {message}")
                self._update_progress(0, "4단계 실패: Node.js 설치 오류")
                return False

            self._log("Node.js 설치 완료")

            # Node.js PATH 설정 (System PATH로 통합)
            self._update_progress(75, "Node.js PATH 설정 중...")

            # npm 글로벌 경로를 실제 경로로 확장
            import os
            npm_path = os.path.join(os.environ.get('APPDATA', ''), 'npm')

            # System PATH에 Node.js와 npm 경로 모두 추가
            system_paths = [r"C:\Program Files\nodejs", npm_path]

            if add_to_path_immediate(system_paths):
                self._log("Node.js 및 npm 경로를 System PATH에 성공적으로 추가했습니다")
            else:
                error_msg = "npm System PATH 추가 실패 - 중요!"
                self._log(f"[ERROR] {error_msg}")

                # error_logger가 있으면 상세 정보 기록
                if hasattr(self, 'error_logger') and self.error_logger:
                    self.error_logger.add_error_detail(
                        step="Step 4: Node.js npm PATH setup",
                        error_message="System PATH addition failed",
                        traceback_info="add_to_path_immediate returned False"
                    )

                self._update_progress(0, "4단계 실패: npm PATH 설정 실패")
                return False  # 설치 중단!

            # 설치 검증
            self._update_progress(78, "Node.js 설치 검증 중...")
            time.sleep(2)  # PATH 반영 대기

            if self.status_checker.is_nodejs_installed():
                node_version = self.status_checker.get_nodejs_version()
                npm_version = self.status_checker.get_npm_version()
                self._log(f"Node.js 설치 검증 완료 - 버전: {node_version}")
                if npm_version:
                    self._log(f"npm 버전: {npm_version}")

            self._update_progress(80, "4단계 완료: Node.js 설치 및 PATH 설정 완료")
            return True

        except Exception as e:
            self._log(f"4단계 오류: {str(e)}")
            self._update_progress(0, f"4단계 실패: {str(e)}")
            return False

    def execute_step_5(self) -> bool:
        """Execute Step 5: Claude CLI installation"""
        try:
            self._update_progress(80, "5단계: Claude CLI 설치 및 PATH 설정 - Claude CLI 상태 확인...")

            # Claude CLI 설치 여부 확인
            if self.status_checker.is_claude_cli_installed():
                self._log("Claude Code CLI가 이미 설치되어 있습니다")
                claude_version = self.status_checker.get_claude_cli_version()
                if claude_version:
                    self._log(f"현재 Claude CLI 버전: {claude_version}")

                # Claude CLI 실행 가능 여부 확인
                self._log("Claude CLI 실행 가능 여부 확인 중...")
                import os
                npm_path = os.path.join(os.environ.get('APPDATA', ''), 'npm')

                if not self._ensure_tool_in_path("Claude", [npm_path], "claude"):
                    self._log("[WARNING] Claude CLI PATH 확인 필요 - npm 경로 설정을 확인하세요")
            else:
                # Claude CLI 설치 시작
                self._update_progress(81, "Claude Code CLI 설치를 시작합니다...")
                success, message = self.installer.install_claude_cli()

                if not success:
                    self._log(f"Claude CLI 설치 실패: {message}")
                    self._update_progress(0, "5단계 실패: Claude CLI 설치 오류")
                    return False

                self._log("Claude Code CLI 설치 완료")

            self._update_progress(83, "5단계 완료: Claude CLI 설치 완료")
            return True

        except Exception as e:
            self._log(f"5단계 오류: {str(e)}")
            self._update_progress(0, f"5단계 실패: {str(e)}")
            return False

    def execute_step_6(self) -> bool:
        """Execute Step 6: Gemini CLI installation and final verification"""
        try:
            self._update_progress(85, "6단계: Gemini CLI 설치 및 최종 검증 - Gemini CLI 상태 확인...")

            # Gemini CLI 설치 여부 확인
            if self.status_checker.is_gemini_cli_installed():
                self._log("Gemini CLI가 이미 설치되어 있습니다")
                gemini_version = self.status_checker.get_gemini_cli_version()
                if gemini_version:
                    self._log(f"현재 Gemini CLI 버전: {gemini_version}")

                # Gemini CLI 실행 가능 여부 확인
                self._log("Gemini CLI 실행 가능 여부 확인 중...")
                import os
                npm_path = os.path.join(os.environ.get('APPDATA', ''), 'npm')

                if not self._ensure_tool_in_path("Gemini", [npm_path], "gemini"):
                    self._log("[WARNING] Gemini CLI PATH 확인 필요 - npm 경로 설정을 확인하세요")
            else:
                # Gemini CLI 설치 시작
                self._update_progress(88, "Gemini CLI 설치를 시작합니다...")
                success, message = self.installer.install_gemini_cli()

                if not success:
                    self._log(f"Gemini CLI 설치 실패: {message}")
                    self._update_progress(0, "6단계 실패: Gemini CLI 설치 오류")
                    return False

                self._log("Gemini CLI 설치 완료")

            # 전체 PATH 검증
            self._update_progress(92, "전체 도구 PATH 검증 시작...")
            results = self.path_verifier.verify_all_silent()

            # 검증 결과 출력 (실행 성공 시 메시지 없음, 실패 시만 경고)
            for result in results:
                tool_name = result.get('tool', 'Unknown')
                execution_success = result.get('status') == 'success'

                # 실행 가능하면 메시지 없음
                if execution_success:
                    continue  # 성공 시 아무 메시지도 출력하지 않음

                # 실패한 경우만 경고 메시지
                self._log(f"[경고] {tool_name}: 실행 실패 - 확인 필요")

            # 최종 환경변수 리프레시
            self._update_progress(95, "최종 환경변수 리프레시...")
            self._refresh_environment()

            # 최종 상태 요약
            self._update_progress(98, "최종 설치 상태 확인...")
            final_status = self.status_checker.check_all()

            installed_tools = []
            if final_status.get('git', {}).get('installed', False):
                installed_tools.append("Git")
            if final_status.get('nodejs', {}).get('installed', False):
                installed_tools.append("Node.js")
            if final_status.get('claude', {}).get('installed', False):
                installed_tools.append("Claude CLI")
            if final_status.get('gemini', {}).get('installed', False):
                installed_tools.append("Gemini CLI")

            self._log(f"설치된 도구: {', '.join(installed_tools)}")
            self._update_progress(100, "설치 완료!")

            # VSCode 터미널 자동 최적화
            self._optimize_vscode_terminal()

            return True

        except Exception as e:
            self._log(f"6단계 오류: {str(e)}")
            self._update_progress(0, f"6단계 실패: {str(e)}")
            return False

    def _optimize_vscode_terminal(self):
        """VSCode 터미널 PATH 자동 최적화"""
        try:
            from modules.utils.vscode_settings_manager import VSCodeSettingsManager

            self._log("VSCode 터미널 설정 최적화 중...")
            manager = VSCodeSettingsManager()
            manager.auto_fix_vscode_terminal_path()
            self._log("VSCode 터미널 설정 최적화 완료")

        except Exception as e:
            # 실패해도 무시 (치명적 아님)
            self._log(f"VSCode 설정 최적화 건너뜀 (선택사항)")


__all__ = ['InstallationStepExecutor']
