"""
자동 설치를 담당하는 AutoInstaller 클래스 - Facade Pattern
6단계 자동 설치 프로세스 오케스트레이션
Brain Module System v4.0
"""

import threading
from typing import Callable, Optional

from modules.core.installer import Installer
from modules.core.status_checker import StatusChecker
from modules.utils.path_verifier import PathVerifier
from modules.utils.error_logger import ErrorLogManager

from .installer_modules.installation_step_executor import InstallationStepExecutor


class AutoInstaller:
    """
    6단계 자동 설치 시스템 - Orchestrator

    완전 자동화된 설치 프로세스:
    1. Chocolatey 설치 및 즉시 적용 (0-20%)
    2. Chocolatey 감지 확인 (20-40%)
    3. Git 자동 설치 및 PATH 설정 (40-60%)
    4. Node.js 자동 설치 및 PATH 설정 (60-80%)
    5. Claude CLI 설치 및 검증 (80-90%)
    6. Gemini CLI 설치 및 최종 검증 (90-100%)
    """

    def __init__(self, progress_callback: Optional[Callable] = None,
                 log_callback: Optional[Callable] = None):
        """
        AutoInstaller 초기화

        Args:
            progress_callback: 진행률 업데이트 콜백 (progress, message)
            log_callback: 로그 메시지 콜백
        """
        self.progress_callback = progress_callback
        self.log_callback = log_callback

        # 핵심 모듈 초기화
        self.installer = Installer()
        self.status_checker = StatusChecker()
        self.path_verifier = PathVerifier()
        self.error_logger = ErrorLogManager()

        # 단계 실행기 초기화
        self.step_executor = InstallationStepExecutor(
            installer=self.installer,
            status_checker=self.status_checker,
            path_verifier=self.path_verifier,
            error_logger=self.error_logger,
            progress_callback=self._update_progress,
            log_callback=self._log
        )

        # 상태 관리
        self.installation_thread = None
        self.stop_requested = False

    def _log(self, message: str):
        """로그 메시지 출력"""
        if self.log_callback:
            self.log_callback(message)

    def _update_progress(self, progress: float, message: str):
        """진행률 업데이트"""
        if self.progress_callback:
            self.progress_callback(progress, message)

    def start_auto_installation(self) -> bool:
        """
        자동 설치 시작 (백그라운드 스레드)

        Returns:
            bool: 스레드 시작 성공 여부
        """
        if self.installation_thread and self.installation_thread.is_alive():
            self._log("이미 설치가 진행 중입니다!")
            return False

        # 스레드로 설치 실행
        self.stop_requested = False
        self.installation_thread = threading.Thread(
            target=self._run_installation,
            daemon=True
        )
        self.installation_thread.start()
        return True

    def _run_installation(self):
        """설치 프로세스 실행 (스레드 내부)"""
        try:
            self._log("=" * 50)
            self._log("AI 개발 환경 자동 설치를 시작합니다")
            self._log("=" * 50)

            # 6단계 순차 실행
            steps = [
                (self.step_executor.execute_step_1, "Step 1: Chocolatey 설치"),
                (self.step_executor.execute_step_2, "Step 2: Chocolatey 감지"),
                (self.step_executor.execute_step_3, "Step 3: Git 설치"),
                (self.step_executor.execute_step_4, "Step 4: Node.js 설치"),
                (self.step_executor.execute_step_5, "Step 5: Claude CLI 설치"),
                (self.step_executor.execute_step_6, "Step 6: Gemini CLI 설치 및 검증")
            ]

            for step_func, step_name in steps:
                if self.stop_requested:
                    self._log(f"{step_name}에서 설치가 중단되었습니다.")
                    self._update_progress(0, "설치가 중단되었습니다")
                    return

                success = step_func()

                if not success:
                    self._log(f"{step_name} 실행 실패!")
                    self._update_progress(0, f"{step_name} 실패")
                    return

            # 완료
            self._log("=" * 50)
            self._log("모든 설치가 완료되었습니다!")
            self._log("새 터미널에서 git, node, claude, gemini 명령어를 사용할 수 있습니다.")
            self._log("=" * 50)
            self._update_progress(100, "모든 설치가 완료되었습니다!")

        except Exception as e:
            self._log(f"설치 중 예상치 못한 오류: {str(e)}")
            self.error_logger.log_error(e, "설치 프로세스")
            self._update_progress(0, "설치 실패")

    def stop_installation(self):
        """설치 중지 요청"""
        self.stop_requested = True
        self.step_executor.set_stop_flag(True)
        self._log("설치 중지가 요청되었습니다...")

    def get_installation_status(self) -> dict:
        """현재 설치 상태 반환"""
        return {
            'is_running': self.installation_thread and self.installation_thread.is_alive(),
            'stop_requested': self.stop_requested
        }


__all__ = ['AutoInstaller']