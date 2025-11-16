"""
Layout Components Module
Scrollable container and actions frame components
Brain Module System v4.0
"""

import tkinter as tk
from tkinter import ttk


class LayoutComponentBuilder:
    """Builder class for layout components"""

    def __init__(self, config=None):
        """Initialize with configuration instance"""
        from modules.core.config import Config
        self.config = config if config is not None else Config()

    def create_scrollable_container(self, parent):
        """Create scrollable container with canvas and scrollbar"""
        # Create main container
        main_container = tk.Frame(parent)
        main_container.pack(fill='both', expand=True)

        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind mousewheel for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return main_container, scrollable_frame, canvas

    def create_actions_frame(self, parent, refresh_callback=None):
        """Create actions frame container for install/uninstall sections with config-based colors"""
        actions_frame = tk.LabelFrame(
            parent,
            text=" 도구 관리 ",
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=15
        )
        actions_frame.pack(fill='x', padx=20, pady=10)

        # Create horizontal container for install/uninstall frames
        horizontal_container = tk.Frame(actions_frame)
        horizontal_container.pack(fill='x')

        # Add refresh button at the bottom with config-based color
        refresh_container = tk.Frame(actions_frame)
        refresh_container.pack(fill='x', pady=(10, 0))

        ui_colors = self.config.get_ui_colors()
        refresh_button = tk.Button(
            refresh_container,
            text="상태 새로고침",
            width=54,
            command=refresh_callback if refresh_callback else lambda: None,
            bg=ui_colors.get('refresh_button', '#34495E'),
            fg='white',
            font=('Arial', 10, 'bold')
        )
        refresh_button.pack()

        return actions_frame, horizontal_container, refresh_button


__all__ = ['LayoutComponentBuilder']
