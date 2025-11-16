"""
자동 설치 GUI를 담당하는 AutoGUI 클래스 - Facade Pattern
깔끔하고 직관적인 한국어 인터페이스 제공
Brain Module System v4.0
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional

from .auto_installer import AutoInstaller
from .gui_modules.gui_widgets import GUIWidgetBuilder
from .gui_modules.gui_logger import GUILogger
from .gui_modules.gui_installer_bridge import GUIInstallerBridge


class AutoGUI:
    """자동 설치를 위한 GUI 인터페이스 - Facade"""

    def __init__(self, root: Optional[tk.Tk] = None):
        """
        GUI 초기화

        Args:
            root: 기존 Tkinter 루트 윈도우 (None이면 새로 생성)
        """
        self.root = root or tk.Tk()

        # GUI 컴포넌트 빌더 초기화
        self.widget_builder = GUIWidgetBuilder(self.root)

        # 위젯 생성
        self.widget_builder.setup_window()
        self.widget_builder.create_widgets()
        self.widget_builder.setup_layout()

        # 위젯 참조 가져오기
        widgets = self.widget_builder.get_widgets()
        self._assign_widgets(widgets)

        # 로거 초기화
        self.logger = GUILogger(self.log_text, self.root)

        # 설치 브리지 초기화
        self.installer_bridge = GUIInstallerBridge(
            root=self.root,
            start_button=self.start_button,
            stop_button=self.stop_button,
            progress_var=self.progress_var,
            status_label=self.status_label,
            progress_callback=self.logger.add_log,
            log_callback=self.logger.add_log
        )

        # 버튼 이벤트 연결
        self.start_button.config(command=self.installer_bridge.start_installation)
        self.stop_button.config(command=self.installer_bridge.stop_installation)
        self.clear_log_button.config(command=self.logger.clear_log)
        self.save_log_button.config(command=self.logger.save_log)

        # AutoInstaller 설정
        self.installer_bridge.setup_auto_installer()

        # 닫기 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _assign_widgets(self, widgets: dict):
        """위젯 참조 할당"""
        self.main_frame = widgets['main_frame']
        self.title_label = widgets['title_label']
        self.desc_label = widgets['desc_label']
        self.control_frame = widgets['control_frame']
        self.start_button = widgets['start_button']
        self.stop_button = widgets['stop_button']
        self.progress_frame = widgets['progress_frame']
        self.progress_var = widgets['progress_var']
        self.progress_bar = widgets['progress_bar']
        self.status_label = widgets['status_label']
        self.log_frame = widgets['log_frame']
        self.log_text = widgets['log_text']
        self.log_control_frame = widgets['log_control_frame']
        self.clear_log_button = widgets['clear_log_button']
        self.save_log_button = widgets['save_log_button']

    def _on_closing(self):
        """프로그램 종료 처리"""
        if self.installer_bridge.is_installing:
            response = messagebox.askyesno(
                "프로그램 종료",
                "설치가 진행 중입니다.\n\n"
                "정말로 프로그램을 종료하시겠습니까?\n"
                "진행 중인 설치가 중단됩니다.",
                icon="warning"
            )

            if not response:
                return

            # 설치 중단
            if self.installer_bridge.auto_installer:
                self.installer_bridge.auto_installer.stop_installation()

        self.root.quit()
        self.root.destroy()

    def run(self):
        """GUI 실행"""
        self.root.mainloop()

    def get_root(self):
        """루트 윈도우 반환"""
        return self.root


__all__ = ['AutoGUI']