"""
Configuration Commands Module
Package manager and shell command definitions
Brain Module System v4.0
"""

# =============================================================================
# PACKAGE MANAGER COMMANDS
# =============================================================================

CHOCOLATEY_COMMANDS = {
    'install_git': ['choco', 'install', 'git', '-y', '--no-progress'],
    'install_nodejs': ['choco', 'install', 'nodejs', '-y', '--no-progress'],
    'install_python': ['choco', 'install', 'python312', '-y', '--no-progress'],
    'version_check': ['choco', '--version'],
    'refresh_env': 'refreshenv'
}

WINGET_COMMANDS = {
    'install_git': [
        'winget', 'install', '--id', 'Git.Git',
        '-e', '--silent', '--accept-package-agreements', '--accept-source-agreements'
    ],
    'install_nodejs': [
        'winget', 'install', '--id', 'OpenJS.NodeJS',
        '-e', '--silent', '--accept-package-agreements', '--accept-source-agreements'
    ],
    'install_python': ['winget', 'install', 'Python.Python.3.12', '-e', '--silent']
}

# =============================================================================
# NPM COMMANDS
# =============================================================================

NPM_COMMANDS = {
    'install_claude_cli': ['npm', 'install', '-g', '@claude-ai/claude-cli'],
    'install_claude_cli_alt': ['npm', 'install', '-g', 'claude-code-cli'],
    'version_check': ['npm', '--version'],
    'config_get_prefix': ['npm', 'config', 'get', 'prefix']
}

# =============================================================================
# POWERSHELL COMMANDS
# =============================================================================

POWERSHELL_COMMANDS = {
    'chocolatey_install': [
        'powershell', '-NoProfile', '-InputFormat', 'None',
        '-ExecutionPolicy', 'Bypass', '-Command',
        "Set-ExecutionPolicy Bypass -Scope Process -Force; "
        "[System.Net.ServicePointManager]::SecurityProtocol = "
        "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
        "iex ((New-Object System.Net.WebClient).DownloadString("
        "'https://community.chocolatey.org/install.ps1'))"
    ],
    'where_choco': ['powershell', '-Command', 'where.exe choco']
}

# =============================================================================
# VERSION CHECK COMMANDS
# =============================================================================

VERSION_CHECK_COMMANDS = {
    'git': ['git', '--version'],
    'node': ['node', '--version'],
    'npm': ['npm', '--version'],
    'claude': ['claude', '--version'],
    'choco': ['choco', '--version'],
    'python': ['python', '--version']
}

# =============================================================================
# INSTALLATION COMMANDS MAPPING
# =============================================================================

INSTALL_COMMANDS = {
    'git': ['choco', 'install', 'git', '-y'],
    'nodejs': ['choco', 'install', 'nodejs', '-y'],
    'claude_cli': ['npm', 'install', '-g', '@anthropic-ai/claude-cli']
}

# =============================================================================
# SHELL SETTINGS
# =============================================================================

SHELL_REQUIRED_COMMANDS = {
    'npm_version_check': True,
    'npm_install': True,
    'claude_version_check': True,
    'chocolatey_refresh': True,
    'chocolatey_version_check': True
}

NO_SHELL_COMMANDS = {
    'git_version_check': False,
    'node_version_check': False,
    'winget_install': False,
    'powershell_commands': False
}

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'CHOCOLATEY_COMMANDS',
    'WINGET_COMMANDS',
    'NPM_COMMANDS',
    'POWERSHELL_COMMANDS',
    'VERSION_CHECK_COMMANDS',
    'INSTALL_COMMANDS',
    'SHELL_REQUIRED_COMMANDS',
    'NO_SHELL_COMMANDS'
]
