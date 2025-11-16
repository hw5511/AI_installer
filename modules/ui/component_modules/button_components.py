"""
Button Components Module
Installation button components
Brain Module System v4.0
"""

import tkinter as tk


class ButtonComponentBuilder:
    """Builder class for button components"""

    def __init__(self, config=None):
        """Initialize with configuration instance"""
        from modules.core.config import Config
        self.config = config if config is not None else Config()

    def create_install_buttons(self, parent, callback_dict):
        """Create installation buttons frame with callbacks and config-based colors"""
        install_frame = tk.LabelFrame(
            parent,
            text=" 설치 옵션 ",
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=10
        )
        install_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        buttons = {}

        # Git installation button - hardcoding removed
        buttons['git'] = tk.Button(
            install_frame,
            text="Git 설치",
            width=25,
            command=callback_dict.get('git', lambda: None),
            bg=self.config.get_install_color('git'),
            fg='white',
            font=('Arial', 9, 'bold')
        )
        buttons['git'].pack(pady=5, padx=5)

        # Node.js installation button - hardcoding removed
        buttons['nodejs'] = tk.Button(
            install_frame,
            text="Node.js 설치",
            width=25,
            command=callback_dict.get('nodejs', lambda: None),
            bg=self.config.get_install_color('nodejs'),
            fg='white',
            font=('Arial', 9, 'bold')
        )
        buttons['nodejs'].pack(pady=5, padx=5)

        # Claude CLI installation button - hardcoding removed
        buttons['claude_cli'] = tk.Button(
            install_frame,
            text="Claude CLI 설치",
            width=25,
            command=callback_dict.get('claude_cli', lambda: None),
            bg=self.config.get_install_color('claude_cli'),
            fg='white',
            font=('Arial', 9, 'bold')
        )
        buttons['claude_cli'].pack(pady=5, padx=5)

        return install_frame, buttons


__all__ = ['ButtonComponentBuilder']
