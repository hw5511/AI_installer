"""
Configuration UI Module
User interface configuration settings
Brain Module System v4.0
"""

# =============================================================================
# WINDOW CONFIGURATION
# =============================================================================

WINDOW_CONFIG = {
    'title': 'AI 설정 도구 - Chocolatey 버전',
    'geometry': '700x750',
    'min_width': 650,
    'min_height': 600,
    'resizable': (True, True),
    'resizable_width': True,
    'resizable_height': True
}

# =============================================================================
# UI LAYOUT CONFIGURATION
# =============================================================================

UI_LAYOUT = {
    'title_frame_height': 60,
    'padding_x': 20,
    'padding_y': 10,
    'button_width': 25,
    'log_height': 10,
    'font_title': ('Arial', 16, 'bold'),
    'font_section': ('Arial', 11, 'bold'),
    'font_button': ('Arial', 9, 'bold'),
    'font_status': ('Arial', 10),
    'font_log': ('Consolas', 9)
}

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'WINDOW_CONFIG',
    'UI_LAYOUT'
]
