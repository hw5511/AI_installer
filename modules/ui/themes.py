"""
Simple color definitions for AI Setup Tool
Lightweight theme system - Brain Module System v4.0
"""

# Basic colors for UI components
COLORS = {
    # Install button colors
    'git_install': '#9B59B6',
    'nodejs_install': '#E67E22',
    'claude_cli_install': '#E74C3C',
    'gemini_cli_install': '#4285F4',
    'choco_install': '#8B4513',
    'npm_install': '#CB3837',

    # Uninstall button colors
    'git_uninstall': '#8E44AD',
    'nodejs_uninstall': '#D35400',
    'claude_cli_uninstall': '#C0392B',
    'gemini_cli_uninstall': '#3367D6',
    'choco_uninstall': '#654321',
    'npm_uninstall': '#A52A2A',

    # Status colors
    'status_installed': '#27AE60',
    'status_not_installed': '#E74C3C',
    'button_disabled': '#95A5A6',

    # UI frame colors
    'title_bg': '#2C3E50',
    'title_fg': 'white',
    'refresh_button': '#34495E',

    # Log colors
    'log_bg': '#1E1E1E',
    'log_fg': '#00FF00'
}

# Legacy compatibility functions
def get_install_color(tool_name: str) -> str:
    return COLORS.get(f'{tool_name}_install', '#95A5A6')

def get_uninstall_color(tool_name: str) -> str:
    return COLORS.get(f'{tool_name}_uninstall', '#95A5A6')