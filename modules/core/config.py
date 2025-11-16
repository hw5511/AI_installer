"""
Unified Configuration Module for AI Setup Tool - Facade Pattern
Consolidated configuration from modules/config.py and main_modules/config.py
Brain Module System v4.0 - Central configuration management
"""

import os
import subprocess

from .config_modules.config_constants import (
    TIMEOUT_SECONDS, COMMAND_TIMEOUTS, PACKAGE_CONFIGS, TOOL_NAMES,
    GIT_PATHS, NODEJS_PATHS, CHOCOLATEY_PATHS,
    ENVIRONMENT_VARIABLES, REGISTRY_SETTINGS, CONFIG_PATHS
)
from .config_modules.config_commands import (
    CHOCOLATEY_COMMANDS, WINGET_COMMANDS, NPM_COMMANDS,
    POWERSHELL_COMMANDS, VERSION_CHECK_COMMANDS, INSTALL_COMMANDS,
    SHELL_REQUIRED_COMMANDS, NO_SHELL_COMMANDS
)
from .config_modules.config_ui import WINDOW_CONFIG, UI_LAYOUT
from .config_modules.config_messages import SUCCESS_MESSAGES, ERROR_MESSAGES, INFO_MESSAGES


class Config:
    """Central configuration class for AI Setup Tool - Facade Pattern"""
    TIMEOUT_SECONDS, COMMAND_TIMEOUTS, PACKAGE_CONFIGS, TOOL_NAMES = (
        TIMEOUT_SECONDS, COMMAND_TIMEOUTS, PACKAGE_CONFIGS, TOOL_NAMES
    )
    WINDOW_CONFIG, UI_LAYOUT = WINDOW_CONFIG, UI_LAYOUT
    GIT_PATHS, NODEJS_PATHS, CHOCOLATEY_PATHS = GIT_PATHS, NODEJS_PATHS, CHOCOLATEY_PATHS
    ENVIRONMENT_VARIABLES, REGISTRY_SETTINGS, CONFIG_PATHS = (
        ENVIRONMENT_VARIABLES, REGISTRY_SETTINGS, CONFIG_PATHS
    )
    CHOCOLATEY_COMMANDS, WINGET_COMMANDS, NPM_COMMANDS, POWERSHELL_COMMANDS = (
        CHOCOLATEY_COMMANDS, WINGET_COMMANDS, NPM_COMMANDS, POWERSHELL_COMMANDS
    )
    VERSION_CHECK_COMMANDS, INSTALL_COMMANDS = VERSION_CHECK_COMMANDS, INSTALL_COMMANDS
    SHELL_REQUIRED_COMMANDS, NO_SHELL_COMMANDS = SHELL_REQUIRED_COMMANDS, NO_SHELL_COMMANDS
    SUCCESS_MESSAGES, ERROR_MESSAGES, INFO_MESSAGES = SUCCESS_MESSAGES, ERROR_MESSAGES, INFO_MESSAGES

    def __init__(self):
        """Initialize configuration with production mode detection and validation"""
        from ..ui.themes import COLORS
        self.COLORS = COLORS
        self._production_mode = True
        try:
            self._production_mode = self._detect_production_mode()
        except Exception:
            pass
        self._validate_configuration()

    def _detect_production_mode(self):
        """Detect if running in production mode"""
        if os.path.exists('production_mode.flag'):
            return True
        import sys
        if hasattr(sys, 'frozen') or sys.argv[0].endswith('.exe'):
            return True
        return False

    def is_production_mode(self):
        """Return whether the application is running in production mode"""
        if not hasattr(self, '_production_mode'):
            self._production_mode = True
        return self._production_mode

    def get_subprocess_flags(self):
        """Get subprocess creation flags based on production mode"""
        if not hasattr(self, '_production_mode'):
            self._production_mode = True
        return subprocess.CREATE_NO_WINDOW if self._production_mode else 0

    def _validate_configuration(self):
        """Validate configuration completeness"""
        required_sections = ['PACKAGE_CONFIGS', 'COLORS', 'WINDOW_CONFIG', 'TOOL_NAMES', 'INSTALL_COMMANDS']
        for section in required_sections:
            if not hasattr(self, section):
                raise ValueError(f"Missing required configuration section: {section}")

    @classmethod
    def get_window_config(cls):
        return cls.WINDOW_CONFIG.copy()
    @classmethod
    def get_ui_colors(cls):
        from ..ui.themes import COLORS
        return COLORS.copy()
    @classmethod
    def get_install_color(cls, tool_name):
        from ..ui.themes import get_install_color
        return get_install_color(tool_name)
    @classmethod
    def get_uninstall_color(cls, tool_name):
        from ..ui.themes import get_uninstall_color
        return get_uninstall_color(tool_name)
    @classmethod
    def get_tool_display_name(cls, tool_name):
        if tool_name in cls.PACKAGE_CONFIGS:
            return cls.PACKAGE_CONFIGS[tool_name]['display_name']
        return cls.TOOL_NAMES.get(tool_name, tool_name.title())
    @classmethod
    def validate_chocolatey_installation(cls):
        chocolatey_paths = [cls.CHOCOLATEY_PATHS['default']] + cls.CHOCOLATEY_PATHS['alternatives']
        for path in chocolatey_paths:
            if os.path.exists(path):
                return True, path
        return False, None
    @classmethod
    def get_install_command(cls, tool_key):
        return cls.INSTALL_COMMANDS.get(tool_key, [])
    @classmethod
    def is_shell_command(cls, tool_key):
        return cls.SHELL_REQUIRED_COMMANDS.get(f"{tool_key}_install", tool_key == 'claude_cli')
    @classmethod
    def get_layout_config(cls):
        return cls.UI_LAYOUT.copy()
    @classmethod
    def get_package_config(cls, tool_name):
        return cls.PACKAGE_CONFIGS.get(tool_name, {})
    @classmethod
    def get_timeout(cls, operation):
        return cls.COMMAND_TIMEOUTS.get(operation, cls.TIMEOUT_SECONDS)
    @classmethod
    def should_use_shell(cls, command_type):
        return cls.SHELL_REQUIRED_COMMANDS.get(command_type, False)
    @classmethod
    def get_chocolatey_default_path(cls):
        return os.environ.get(cls.ENVIRONMENT_VARIABLES['chocolatey_install'], cls.CHOCOLATEY_PATHS['install_dir'])
    @classmethod
    def get_npm_bin_path(cls, npm_prefix):
        return os.path.join(npm_prefix, 'bin') if os.name != 'nt' else npm_prefix
    @classmethod
    def format_success_message(cls, message_key, **kwargs):
        return cls.SUCCESS_MESSAGES.get(message_key, message_key).format(**kwargs)
    @classmethod
    def format_error_message(cls, message_key, **kwargs):
        return cls.ERROR_MESSAGES.get(message_key, message_key).format(**kwargs)
    @classmethod
    def format_info_message(cls, message_key, **kwargs):
        return cls.INFO_MESSAGES.get(message_key, message_key).format(**kwargs)


try:
    config = Config()
except Exception as e:
    print(f"Warning: Config initialization failed: {e}")
    class MinimalConfig:
        _production_mode = True
        is_production_mode = lambda self: True
        get_subprocess_flags = lambda self: __import__('subprocess').CREATE_NO_WINDOW
    config = MinimalConfig()

__all__ = ['Config', 'config']