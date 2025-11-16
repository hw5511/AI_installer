"""
GUI Widgets Module
Widget creation and styling for auto installation GUI
Brain Module System v4.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext


class GUIWidgetBuilder:
    """Handles GUI widget creation and styling"""

    def __init__(self, root: tk.Tk):
        """
        Initialize widget builder

        Args:
            root: Tkinter root window
        """
        self.root = root

        # 위젯 참조
        self.main_frame = None
        self.title_label = None
        self.desc_label = None
        self.control_frame = None
        self.start_button = None
        self.stop_button = None
        self.progress_frame = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        self.log_frame = None
        self.log_text = None
        self.log_control_frame = None
        self.clear_log_button = None
        self.save_log_button = None

        # 폰트 설정
        self.default_font = ("맑은 고딕", 9)
        self.button_font = ("맑은 고딕", 10, "bold")
        self.title_font = ("맑은 고딕", 12, "bold")
        self.log_font = ("Consolas", 9)

    def setup_window(self):
        """메인 윈도우 설정"""
        self.root.title("AI 개발 환경 자동 설치 도구 v2.8")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # 아이콘 설정 (있다면)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # 닫기 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # 폰트 설정
        self.default_font = ("맑은 고딕", 9)
        self.button_font = ("맑은 고딕", 10, "bold")
        self.title_font = ("맑은 고딕", 12, "bold")
        self.log_font = ("Consolas", 9)

    def create_widgets(self):
        """GUI 위젯들 생성"""
        # 메인 프레임
        self.main_frame = ttk.Frame(self.root, padding="10")

        # 제목 라벨
        self.title_label = tk.Label(
            self.main_frame,
            text="🚀 AI 개발 환경 자동 설치 도구",
            font=self.title_font,
            fg="#2E7D32"
        )

        # 설명 라벨
        self.desc_label = tk.Label(
            self.main_frame,
            text="Git, Node.js, Claude CLI를 자동으로 설치하고 PATH를 설정합니다",
            font=self.default_font,
            fg="#424242"
        )

        # 컨트롤 프레임
        self.control_frame = ttk.Frame(self.main_frame)

        # 시작 버튼
        self.start_button = tk.Button(
            self.control_frame,
            text="🚀 자동 설치 시작",
            command=None,  # 외부에서 설정
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=8
        )

        # 중지 버튼
        self.stop_button = tk.Button(
            self.control_frame,
            text="⏹️ 설치 중지",
            command=None,  # 외부에서 설정
            font=self.button_font,
            bg="#f44336",
            fg="white",
            relief="raised",
            bd=2,
            padx=20,
            pady=8,
            state="disabled"
        )

        # 프로그레스 프레임
        self.progress_frame = ttk.Frame(self.main_frame)

        # 프로그레스 바
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=600,
            mode='determinate'
        )

        # 상태 라벨
        self.status_label = tk.Label(
            self.progress_frame,
            text="설치 준비 완료 - 시작 버튼을 클릭해주세요",
            font=self.default_font,
            fg="#424242"
        )

        # 로그 프레임
        self.log_frame = ttk.LabelFrame(self.main_frame, text="📋 설치 로그", padding="5")

        # 로그 텍스트 (스크롤 포함)
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            height=20,
            width=80,
            font=self.log_font,
            bg="#1E1E1E",
            fg="#00FF00",
            insertbackground="white",
            wrap=tk.WORD,
            state="disabled"
        )

        # 로그 컨트롤 프레임
        self.log_control_frame = ttk.Frame(self.log_frame)

        # 로그 지우기 버튼
        self.clear_log_button = tk.Button(
            self.log_control_frame,
            text="🗑️ 로그 지우기",
            command=None,  # 외부에서 설정
            font=self.default_font,
            bg="#FF9800",
            fg="white",
            relief="raised",
            bd=1,
            padx=10,
            pady=4
        )

        # 로그 저장 버튼
        self.save_log_button = tk.Button(
            self.log_control_frame,
            text="💾 로그 저장",
            command=None,  # 외부에서 설정
            font=self.default_font,
            bg="#2196F3",
            fg="white",
            relief="raised",
            bd=1,
            padx=10,
            pady=4
        )

    def setup_layout(self):
        """레이아웃 배치"""
        # 메인 프레임
        self.main_frame.pack(fill="both", expand=True)

        # 제목
        self.title_label.pack(pady=(0, 5))
        self.desc_label.pack(pady=(0, 15))

        # 컨트롤 버튼들
        self.control_frame.pack(pady=(0, 15))
        self.start_button.pack(side="left", padx=(0, 10))
        self.stop_button.pack(side="left")

        # 프로그레스
        self.progress_frame.pack(fill="x", pady=(0, 15))
        self.progress_bar.pack(fill="x", pady=(0, 8))
        self.status_label.pack()

        # 로그
        self.log_frame.pack(fill="both", expand=True)
        self.log_text.pack(fill="both", expand=True, pady=(0, 8))
        self.log_control_frame.pack(fill="x")
        self.clear_log_button.pack(side="left", padx=(0, 10))
        self.save_log_button.pack(side="left")

    def _on_closing(self):
        """닫기 이벤트 핸들러 (외부에서 재설정 필요)"""
        self.root.quit()
        self.root.destroy()

    def get_widgets(self):
        """생성된 위젯들을 딕셔너리로 반환"""
        return {
            'main_frame': self.main_frame,
            'title_label': self.title_label,
            'desc_label': self.desc_label,
            'control_frame': self.control_frame,
            'start_button': self.start_button,
            'stop_button': self.stop_button,
            'progress_frame': self.progress_frame,
            'progress_var': self.progress_var,
            'progress_bar': self.progress_bar,
            'status_label': self.status_label,
            'log_frame': self.log_frame,
            'log_text': self.log_text,
            'log_control_frame': self.log_control_frame,
            'clear_log_button': self.clear_log_button,
            'save_log_button': self.save_log_button
        }


__all__ = ['GUIWidgetBuilder']
