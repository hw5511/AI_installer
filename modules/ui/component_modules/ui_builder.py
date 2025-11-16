"""
UI Builder Module
Complete UI assembly and orchestration
Brain Module System v4.0
"""

import tkinter as tk
from .status_components import StatusComponentBuilder
from .button_components import ButtonComponentBuilder
from .display_components import DisplayComponentBuilder
from .layout_components import LayoutComponentBuilder


class CompleteUIBuilder:
    """Orchestrator for building complete UI using component builders"""

    def __init__(self, config=None):
        """Initialize with configuration and component builders"""
        from modules.core.config import Config
        self.config = config if config is not None else Config()

        # Initialize all component builders
        self.status_builder = StatusComponentBuilder(self.config)
        self.button_builder = ButtonComponentBuilder(self.config)
        self.display_builder = DisplayComponentBuilder(self.config)
        self.layout_builder = LayoutComponentBuilder(self.config)

    def create_complete_ui(self, root, callbacks):
        """
        Create the complete UI interface with all components
        Returns a dictionary with all UI elements for external control

        Args:
            root: The root tkinter window
            callbacks: Dictionary of callback functions:
                - install_callback(tool_name)
                - uninstall_callback(tool_name)
                - refresh_callback()
                - log_callback(message)
        """
        ui_elements = {}

        # Create main container with scrollbar
        main_container, scrollable_frame, canvas = self.layout_builder.create_scrollable_container(root)
        ui_elements['main_container'] = main_container
        ui_elements['scrollable_frame'] = scrollable_frame
        ui_elements['canvas'] = canvas

        # Title Frame
        title_frame, title_label = self.display_builder.create_title_frame(scrollable_frame)
        ui_elements['title_frame'] = title_frame
        ui_elements['title_label'] = title_label

        # Status Frame
        status_frame, status_labels = self.status_builder.create_status_frame(scrollable_frame)
        ui_elements['status_frame'] = status_frame
        ui_elements['status_labels'] = status_labels

        # Actions Frame with Install and Uninstall sections
        actions_frame, horizontal_container, refresh_button = self.layout_builder.create_actions_frame(
            scrollable_frame,
            callbacks.get('refresh_callback')
        )
        ui_elements['actions_frame'] = actions_frame
        ui_elements['refresh_button'] = refresh_button

        # Install buttons - create callback dict for each tool
        install_callbacks = {
            'git': lambda: callbacks.get('install_callback', lambda x: None)('git'),
            'nodejs': lambda: callbacks.get('install_callback', lambda x: None)('nodejs'),
            'claude_cli': lambda: callbacks.get('install_callback', lambda x: None)('claude_cli')
        }
        install_frame, install_buttons = self.button_builder.create_install_buttons(
            horizontal_container,
            install_callbacks
        )
        ui_elements['install_frame'] = install_frame
        ui_elements['install_buttons'] = install_buttons

        # Uninstall feature disabled - commenting out the uninstall button creation
        # # Uninstall buttons - create callback dict for each tool
        # uninstall_callbacks = {
        #     'git': lambda: callbacks.get('uninstall_callback', lambda x: None)('git'),
        #     'nodejs': lambda: callbacks.get('uninstall_callback', lambda x: None)('nodejs'),
        #     'claude_cli': lambda: callbacks.get('uninstall_callback', lambda x: None)('claude_cli')
        # }
        # uninstall_frame, uninstall_buttons = self.create_uninstall_buttons(
        #     horizontal_container,
        #     uninstall_callbacks
        # )
        # ui_elements['uninstall_frame'] = uninstall_frame
        # ui_elements['uninstall_buttons'] = uninstall_buttons

        # Set empty dict for uninstall buttons to prevent errors
        ui_elements['uninstall_frame'] = None
        ui_elements['uninstall_buttons'] = {}

        # Log Frame
        log_frame, log_text = self.display_builder.create_log_window(scrollable_frame)
        ui_elements['log_frame'] = log_frame
        ui_elements['log_text'] = log_text

        # Initialize log with welcome message if callback provided
        if callbacks.get('log_callback'):
            callbacks['log_callback']("AI 설정 도구가 초기화되었습니다. 개발 도구 설치 준비 완료.")

        return ui_elements


__all__ = ['CompleteUIBuilder']
