"""
UI Components Module for AI Setup Tool - Facade Pattern
Provides reusable UI building blocks for the GUI
Brain Module System v4.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from modules.core.config import Config

# Import from separated modules
from .component_modules.status_components import StatusComponentBuilder
from .component_modules.button_components import ButtonComponentBuilder
from .component_modules.display_components import DisplayComponentBuilder
from .component_modules.layout_components import LayoutComponentBuilder
from .component_modules.ui_builder import CompleteUIBuilder


class UIBuilder:
    """Facade class for creating reusable UI components with config-based colors"""

    def __init__(self, config=None):
        """Initialize UIBuilder with configuration instance"""
        self.config = config if config is not None else Config()

        # Initialize component builders
        self.status_builder = StatusComponentBuilder(self.config)
        self.button_builder = ButtonComponentBuilder(self.config)
        self.display_builder = DisplayComponentBuilder(self.config)
        self.layout_builder = LayoutComponentBuilder(self.config)
        self.complete_builder = CompleteUIBuilder(self.config)

    def create_status_frame(self, parent):
        """Delegate to StatusComponentBuilder"""
        return self.status_builder.create_status_frame(parent)

    def create_install_buttons(self, parent, callback_dict):
        """Delegate to ButtonComponentBuilder"""
        return self.button_builder.create_install_buttons(parent, callback_dict)

    def create_log_window(self, parent):
        """Delegate to DisplayComponentBuilder"""
        return self.display_builder.create_log_window(parent)

    def create_scrollable_container(self, parent):
        """Delegate to LayoutComponentBuilder"""
        return self.layout_builder.create_scrollable_container(parent)

    def create_title_frame(self, parent, title_text="AI 개발 도구 설치 프로그램"):
        """Delegate to DisplayComponentBuilder"""
        return self.display_builder.create_title_frame(parent, title_text)

    def create_actions_frame(self, parent, refresh_callback=None):
        """Delegate to LayoutComponentBuilder"""
        return self.layout_builder.create_actions_frame(parent, refresh_callback)

    def create_complete_ui(self, root, callbacks):
        """Delegate to CompleteUIBuilder"""
        return self.complete_builder.create_complete_ui(root, callbacks)


__all__ = ['UIBuilder']