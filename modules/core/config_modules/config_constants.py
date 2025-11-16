"""
Configuration Constants Module
Centralized constant definitions for AI Setup Tool
Brain Module System v4.0
"""

import os

# =============================================================================
# PYTHON PATHS
# =============================================================================

# Python paths
PYTHON_PATHS = [
    r"C:\Python312",
    r"C:\Python312\Scripts"
]

# =============================================================================
# TIMEOUT CONFIGURATIONS
# =============================================================================

TIMEOUT_SECONDS = 30  # Standardized timeout value

COMMAND_TIMEOUTS = {
    'version_check': 5,
    'npm_version_check': 10,
    'npm_config_check': 5,
    'chocolatey_install': 120,
    'package_install': 300,
    'environment_refresh': 30,
    'command_check': 2,
    'installation': 300
}

# =============================================================================
# PACKAGE CONFIGURATIONS
# =============================================================================

PACKAGE_CONFIGS = {
    'git': {
        'choco_name': 'git',
        'winget_id': 'Git.Git',
        'display_name': 'Git 버전 관리',
        'install_color': '#9B59B6',
        'uninstall_color': '#8E44AD'
    },
    'nodejs': {
        'choco_name': 'nodejs',
        'winget_id': 'OpenJS.NodeJS',
        'display_name': 'Node.js Runtime',
        'install_color': '#E67E22',
        'uninstall_color': '#D35400'
    },
    'claude_cli': {
        'npm_primary': '@claude-ai/claude-cli',
        'npm_alternative': 'claude-code-cli',
        'display_name': 'Claude Code CLI',
        'install_color': '#E74C3C',
        'uninstall_color': '#C0392B'
    },
    'choco': {
        'display_name': 'Chocolatey 패키지 관리자',
        'install_color': '#8B4513',
        'uninstall_color': '#654321'
    },
    'npm': {
        'display_name': 'NPM 패키지 관리자',
        'install_color': '#CB3837',
        'uninstall_color': '#A52A2A'
    },
    'python': {
        'choco_name': 'python312',
        'winget_id': 'Python.Python.3.12',
        'display_name': 'Python 3.12',
        'install_color': '#3776AB',
        'uninstall_color': '#2C5F8D'
    }
}

# =============================================================================
# TOOL NAMES MAPPING
# =============================================================================

TOOL_NAMES = {
    'choco': 'Chocolatey 패키지 관리자',
    'git': 'Git 버전 관리',
    'nodejs': 'Node.js Runtime',
    'npm': 'NPM 패키지 관리자',
    'claude': 'Claude Code CLI'
}

# =============================================================================
# INSTALLATION PATHS
# =============================================================================

GIT_PATHS = {
    'default': r"C:\Program Files\Git\cmd",
    'alternatives': [
        r"C:\Program Files\Git\bin",
        r"C:\Program Files (x86)\Git\cmd",
        r"C:\Program Files (x86)\Git\bin"
    ]
}

NODEJS_PATHS = {
    'default': r"C:\Program Files\nodejs",
    'alternatives': [
        r"C:\Program Files (x86)\nodejs"
    ]
}

CHOCOLATEY_PATHS = {
    'default': r"C:\ProgramData\chocolatey\bin\choco.exe",
    'alternatives': [
        r"C:\ProgramData\chocolatey\choco.exe"
    ],
    'install_dir': r"C:\ProgramData\chocolatey",
    'bin_dir': r"C:\ProgramData\chocolatey\bin"
}

# =============================================================================
# ENVIRONMENT VARIABLES
# =============================================================================

ENVIRONMENT_VARIABLES = {
    'chocolatey_install': 'ChocolateyInstall',
    'path': 'PATH'
}

# =============================================================================
# REGISTRY SETTINGS
# =============================================================================

REGISTRY_SETTINGS = {
    'environment_key': r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'hkey': 'HKEY_LOCAL_MACHINE',
    'path_value_name': 'Path',
    'chocolatey_value_name': 'ChocolateyInstall'
}

# =============================================================================
# CONFIGURATION FILE PATHS
# =============================================================================

CONFIG_PATHS = {
    'user_config': os.path.expanduser('~/.ai_setup_config.json'),
    'system_config': 'config.json'
}

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'PYTHON_PATHS',
    'TIMEOUT_SECONDS',
    'COMMAND_TIMEOUTS',
    'PACKAGE_CONFIGS',
    'TOOL_NAMES',
    'GIT_PATHS',
    'NODEJS_PATHS',
    'CHOCOLATEY_PATHS',
    'ENVIRONMENT_VARIABLES',
    'REGISTRY_SETTINGS',
    'CONFIG_PATHS'
]
