"""
Display Components Module
Log window and title frame components
Brain Module System v4.0
"""

import tkinter as tk
from tkinter import scrolledtext


class DisplayComponentBuilder:
    """Builder class for display components"""

    def __init__(self, config=None):
        """Initialize with configuration instance"""
        from modules.core.config import Config
        self.config = config if config is not None else Config()

    def create_log_window(self, parent):
        """Create log text area with scrollbar and config-based colors"""
        log_frame = tk.LabelFrame(
            parent,
            text=" 설치 로그 ",
            font=('Arial', 11, 'bold'),
            padx=10,
            pady=10
        )
        log_frame.pack(fill='both', expand=False, padx=20, pady=(10, 20))

        # Log text area with scrolled text widget - hardcoding removed
        ui_colors = self.config.get_ui_colors()
        log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=('Consolas', 9),
            bg=ui_colors.get('log_bg', '#1E1E1E'),
            fg=ui_colors.get('log_fg', '#00FF00')
        )
        log_text.pack(fill='both', expand=True)

        return log_frame, log_text

    def create_title_frame(self, parent, title_text="AI 개발 도구 설치 프로그램"):
        """Create title frame with header text and config-based colors"""
        ui_colors = self.config.get_ui_colors()

        title_frame = tk.Frame(
            parent,
            bg=ui_colors.get('title_bg', '#2C3E50'),
            height=60
        )
        title_frame.pack(fill='x', padx=0, pady=0)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text=title_text,
            font=('Arial', 16, 'bold'),
            fg=ui_colors.get('title_fg', 'white'),
            bg=ui_colors.get('title_bg', '#2C3E50')
        )
        title_label.pack(pady=15)

        return title_frame, title_label


__all__ = ['DisplayComponentBuilder']
