"""
Configuration Messages Module
User-facing message templates
Brain Module System v4.0
"""

# =============================================================================
# SUCCESS MESSAGES
# =============================================================================
SUCCESS_MESSAGES = {
    'already_installed': "{tool}이 이미 설치되어 있습니다",
    'install_success': "{tool}이 성공적으로 설치되었습니다!",
    'install_verified': "{tool} 설치가 확인되었습니다",
    'chocolatey_found': "Chocolatey를 찾았습니다: {path}",
    'chocolatey_command_works': "Chocolatey 명령이 작동합니다: {version}",
    'chocolatey_where_found': "Chocolatey를 where 명령으로 찾았습니다: {path}",
    'npm_included': "npm 설치가 확인되었습니다",
    'path_added': "시스템 PATH에 {path}를 추가했습니다",
    'env_var_set': "{var} 환경 변수를 {value}로 설정했습니다",
    'env_broadcast': "시스템에 환경 변수 변경 사항을 알렸습니다"
}

# =============================================================================
# ERROR MESSAGES
# =============================================================================
ERROR_MESSAGES = {
    'install_failed': "{tool} 설치에 실패했습니다: {error}",
    'not_found_in_path': "{tool}이 설치되었지만 PATH에서 찾을 수 없습니다. 터미널을 재시작해 주세요.",
    'npm_not_found': "npm을 찾을 수 없습니다. Node.js와 함께 포함되어야 합니다.",
    'npm_not_installed': "오류: npm이 설치되지 않았습니다. 먼저 Node.js를 설치해 주세요.",
    'admin_required': "Chocolatey 설치를 위해서는 관리자 권한이 필요합니다.",
    'install_timeout': "{tool} 설치가 {timeout}초 후 시간 초과되었습니다.",
    'installation_error': "{tool} 설치 오류: {error}",
    'both_attempts_failed': "두 설치 시도 모두 실패했습니다: {error}",
    'chocolatey_install_failed': "Chocolatey 설치가 반환 코드 {code}로 실패했습니다",
    'chocolatey_timeout': "Chocolatey 설치가 2분 후 시간 초과되었습니다.",
    'chocolatey_verification_failed': "Chocolatey 설치가 완료되었지만 확인에 실패했습니다. 애플리케이션을 재시작해 주세요.",
    'path_update_failed': "시스템 PATH 업데이트에 실패했습니다: {error}",
    'env_var_failed': "{var} 변수 설정에 실패했습니다: {error}",
    'env_refresh_failed': "환경 새로고침에 실패했습니다: {error}",
    'env_broadcast_failed': "환경 변수 변경 사항 알림에 실패했습니다: {error}"
}

# =============================================================================
# INFO MESSAGES
# =============================================================================
INFO_MESSAGES = {
    'installing_with_choco': "Chocolatey로 {tool}을 설치하는 중입니다...",
    'installing_with_winget': "Winget으로 {tool}을 설치하는 중입니다...",
    'installing_with_npm': "npm으로 {tool}을 설치하는 중입니다...",
    'installing_chocolatey': "Chocolatey 패키지 관리자를 설치하는 중입니다...",
    'trying_alternative': "대안 패키지 이름을 시도하는 중입니다...",
    'restart_terminal': "터미널을 재시작하거나 npm global bin을 PATH에 추가해야 할 수 있습니다.",
    'chocolatey_already_installed': "Chocolatey가 이미 설치되어 있습니다."
}

# =============================================================================
# EXPORTS
# =============================================================================
__all__ = [
    'SUCCESS_MESSAGES',
    'ERROR_MESSAGES',
    'INFO_MESSAGES'
]
