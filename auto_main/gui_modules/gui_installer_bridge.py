"""
GUI Installer Bridge Module
Bridge between AutoInstaller and GUI components
Brain Module System v4.0
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import Callable

from ..auto_installer import AutoInstaller


class GUIInstallerBridge:
    """Manages installation process and GUI interaction"""

    def __init__(self, root: tk.Tk, start_button: tk.Button, stop_button: tk.Button,
                 progress_var: tk.DoubleVar, status_label: tk.Label,
                 progress_callback: Callable, log_callback: Callable):
        """
        Initialize installer bridge

        Args:
            root: Tkinter root window
            start_button: Start installation button
            stop_button: Stop installation button
            progress_var: Progress bar variable
            status_label: Status label
            progress_callback: Callback for progress updates
            log_callback: Callback for log messages
        """
        self.root = root
        self.start_button = start_button
        self.stop_button = stop_button
        self.progress_var = progress_var
        self.status_label = status_label
        self.progress_callback = progress_callback
        self.log_callback = log_callback

        self.auto_installer = None
        self.is_installing = False
        self.installation_completed = False  # 중복 팝업 방지 플래그

    def setup_auto_installer(self):
        """AutoInstaller 설정"""
        self.auto_installer = AutoInstaller(
            progress_callback=self.update_progress,
            log_callback=self.log_callback
        )

        # 초기 로그 메시지
        self.log_callback("시스템이 준비되었습니다. 자동 설치를 시작하려면 시작 버튼을 클릭해주세요.")
        self.log_callback("=" * 70)

    def start_installation(self):
        """설치 시작"""
        if self.is_installing:
            messagebox.showwarning("경고", "이미 설치가 진행 중입니다!")
            return

        # 관리자 권한 확인 메시지 제거 (manifest.xml에서 requireAdministrator로 보장됨)
        # 이미 UAC를 통과해서 관리자 권한으로 실행 중이므로 중복 확인 불필요

        # UI 상태 변경
        self.is_installing = True
        self.installation_completed = False  # 플래그 초기화
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # 로그 초기화
        self.log_callback("\n" + "=" * 70)
        self.log_callback(f"🕐 설치 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_callback("=" * 70)

        # 설치 시작
        success = self.auto_installer.start_auto_installation()
        if not success:
            self.installation_finished(False)

    def stop_installation(self):
        """설치 중지"""
        if not self.is_installing:
            return

        response = messagebox.askyesno(
            "설치 중지",
            "정말로 설치를 중지하시겠습니까?\n\n"
            "현재 단계가 완료된 후 중지됩니다.",
            icon="warning"
        )

        if response:
            self.auto_installer.stop_installation()
            self.log_callback("⏸️ 사용자가 설치 중지를 요청했습니다...")

    def update_progress(self, progress: float, message: str):
        """프로그레스 업데이트 (스레드 안전)"""
        def update():
            self.progress_var.set(progress)
            self.status_label.config(text=message)

            # 설치 완료 확인
            if progress >= 100:
                self.root.after(2000, lambda: self.installation_finished(True))
            elif progress == 0 and "실패" in message:
                self.root.after(1000, lambda: self.installation_finished(False))

        self.root.after(0, update)

    def installation_finished(self, success: bool):
        """설치 완료 처리"""
        # 중복 호출 방지
        if self.installation_completed:
            return
        self.installation_completed = True

        self.is_installing = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

        if success:
            # GUI 팝업만 표시 (간단한 메시지)
            messagebox.showinfo(
                "설치 완료",
                "AI 개발 환경 설치가 완료되었습니다!\n\n"
                "설치된 도구: Git, Node.js, Claude CLI, Gemini CLI\n\n"
                "⚠️ VSCode 사용자는 VSCode를 재시작해주세요!\n"
                "(새 터미널에서 바로 사용 가능합니다)"
            )
        else:
            # 에러 로그 파일 저장
            log_file_path = None
            if self.auto_installer and hasattr(self.auto_installer, 'error_logger'):
                log_file_path = self.auto_installer.error_logger.save_error_log()

            self.log_callback("=" * 70)
            self.log_callback("❌ 설치 중 오류가 발생했습니다.")
            if log_file_path:
                self.log_callback(f"📁 에러 로그가 저장되었습니다: {log_file_path}")
            self.log_callback("💡 로그를 확인하시고 문제를 해결한 후 다시 시도해주세요.")
            self.log_callback("=" * 70)

            # 안내 메시지 생성
            error_message = (
                "설치 중 오류가 발생했습니다.\n\n"
                "로그를 확인하시고 다음 사항을 점검해주세요:\n"
                "• 관리자 권한으로 실행했는지 확인\n"
                "• 인터넷 연결 상태 확인\n"
                "• 바이러스 백신 소프트웨어 일시 해제\n\n"
            )

            if log_file_path:
                error_message += (
                    f"문제가 지속될 경우:\n"
                    f"로그 파일이 다음 위치에 저장되었습니다:\n"
                    f"{log_file_path}\n\n"
                    f"로그 파일을 yangheewoo5511@gmail.com 으로\n"
                    f"문제 상황 설명과 함께 보내주세요."
                )
            else:
                error_message += (
                    "문제가 지속되면 GUI 하단의 '로그 저장' 버튼을 눌러\n"
                    "로그를 저장한 후 yangheewoo5511@gmail.com 으로\n"
                    "문제 상황 설명과 함께 보내주세요."
                )

            messagebox.showerror("설치 실패", error_message)


__all__ = ['GUIInstallerBridge']
