"""
Status Components Module
Tool installation status display components
Brain Module System v4.0
"""

import tkinter as tk


class StatusComponentBuilder:
    """Builder class for status display components"""

    def __init__(self, config=None):
        """Initialize with configuration instance"""
        from modules.core.config import Config
        self.config = config if config is not None else Config()

    def create_status_frame(self, parent):
        """Create status display frame for tool installation status"""
        status_frame = tk.LabelFrame(
            parent,
            text=" 설치 상태 ",
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=15
        )
        status_frame.pack(fill='x', padx=20, pady=(20, 10))

        # Create status labels container
        status_labels = {}
        tools = [
            ('choco', 'Chocolatey 패키지 관리자'),
            ('git', 'Git 버전 관리'),
            ('nodejs', 'Node.js 런타임'),
            ('npm', 'NPM 패키지 관리자'),
            ('claude', 'Claude Code CLI')
        ]

        for i, (key, name) in enumerate(tools):
            frame = tk.Frame(status_frame)
            frame.pack(fill='x', pady=3)

            # Status indicator
            indicator = tk.Label(frame, text="●", font=('Arial', 12))
            indicator.pack(side='left', padx=(0, 10))

            # Tool name and version
            label = tk.Label(frame, text=name, font=('Arial', 10), anchor='w')
            label.pack(side='left', fill='x', expand=True)

            status_labels[key] = {
                'indicator': indicator,
                'label': label
            }

        return status_frame, status_labels


__all__ = ['StatusComponentBuilder']
