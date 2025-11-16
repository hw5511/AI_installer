"""
Broadcast Manager Module
Windows message broadcasting for environment changes
Brain Module System v4.0
"""

import ctypes
from ctypes import wintypes
from typing import Optional


# Windows API 상수
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A
SMTO_ABORTIFHUNG = 0x0002
SMTO_BLOCK = 0x0001


class BroadcastManager:
    """Manages Windows environment change notifications"""

    def __init__(self):
        """Initialize BroadcastManager with Windows API constants"""
        self._hwnd_broadcast = HWND_BROADCAST
        self._wm_settingchange = WM_SETTINGCHANGE
        self._smto_abortifhung = SMTO_ABORTIFHUNG
        self._smto_block = SMTO_BLOCK
        self._setup_windows_api()

    def _setup_windows_api(self):
        """Setup Windows API function signatures"""
        try:
            # SendMessageTimeoutW 함수 설정
            self.send_message_timeout = ctypes.windll.user32.SendMessageTimeoutW
            self.send_message_timeout.argtypes = [
                wintypes.HWND,      # hWnd
                wintypes.UINT,      # Msg
                wintypes.WPARAM,    # wParam
                wintypes.LPVOID,    # lParam
                wintypes.UINT,      # fuFlags
                wintypes.UINT,      # uTimeout
                ctypes.POINTER(wintypes.DWORD)  # lpdwResult
            ]
            self.send_message_timeout.restype = wintypes.LPARAM

            # PostMessageW 함수 설정
            self.post_message = ctypes.windll.user32.PostMessageW
            self.post_message.argtypes = [
                wintypes.HWND,      # hWnd
                wintypes.UINT,      # Msg
                wintypes.WPARAM,    # wParam
                wintypes.LPARAM     # lParam
            ]
            self.post_message.restype = wintypes.BOOL

        except Exception as e:
            print(f"Windows API 설정 실패: {e}")
            raise

    def broadcast_environment_change(self, timeout: int = 5000) -> bool:
        """
        Broadcast environment variable change to system

        Args:
            timeout: Timeout in milliseconds (default: 5000)

        Returns:
            bool: Success status
        """
        try:
            result = wintypes.DWORD()

            # WM_SETTINGCHANGE 메시지를 모든 최상위 윈도우에 전송
            return_value = self.send_message_timeout(
                self._hwnd_broadcast,
                self._wm_settingchange,
                0,
                'Environment',
                self._smto_abortifhung,
                timeout,
                ctypes.byref(result)
            )

            if return_value:
                print("시스템에 환경 변수 변경사항을 브로드캐스트했습니다")
                return True
            else:
                print("브로드캐스트 메시지 전송 실패")
                return False

        except Exception as e:
            print(f"환경 변수 변경사항 브로드캐스트 실패: {e}")
            return False

    def broadcast_environment_change_enhanced(self, timeout: int = 10000) -> bool:
        """
        Enhanced broadcast with multiple attempts and methods
        Uses both blocking and non-blocking notification methods

        Args:
            timeout: Timeout in milliseconds (default: 10000)

        Returns:
            bool: Success status
        """
        try:
            result = wintypes.DWORD()

            # Method 1: Send with BLOCK flag to ensure processing
            # 블로킹 플래그를 사용하여 메시지가 처리될 때까지 대기
            return_value = self.send_message_timeout(
                self._hwnd_broadcast,
                self._wm_settingchange,
                0,
                'Environment',
                self._smto_block | self._smto_abortifhung,
                timeout,
                ctypes.byref(result)
            )

            if not return_value:
                print("[경고] 블로킹 브로드캐스트 실패, 대체 방법 시도 중...")

            # Method 2: Also notify using PostMessage for non-blocking notification
            # 논블로킹 방식으로 추가 알림 전송 (백그라운드 처리)
            post_result = self.post_message(
                self._hwnd_broadcast,
                self._wm_settingchange,
                0,
                0
            )

            # 둘 중 하나라도 성공하면 OK
            success = bool(return_value or post_result)

            if success:
                print("향상된 브로드캐스트 완료 (블로킹 + 논블로킹 방식)")
                return True
            else:
                print("모든 브로드캐스트 방법 실패")
                return False

        except Exception as e:
            print(f"향상된 브로드캐스트 실패: {e}")
            return False

    def notify_system_change(self, change_type: str = "Environment", timeout: int = 5000) -> bool:
        """
        Notify system of specific change

        Args:
            change_type: Type of change to notify (default: "Environment")
            timeout: Timeout in milliseconds (default: 5000)

        Returns:
            bool: Success status
        """
        try:
            result = wintypes.DWORD()

            # WM_SETTINGCHANGE 메시지 전송
            return_value = self.send_message_timeout(
                self._hwnd_broadcast,
                self._wm_settingchange,
                0,
                change_type,
                self._smto_abortifhung,
                timeout,
                ctypes.byref(result)
            )

            if return_value:
                print(f"시스템 변경 알림 전송 완료: {change_type}")
                return True
            else:
                print(f"시스템 변경 알림 실패: {change_type}")
                return False

        except Exception as e:
            print(f"시스템 변경 알림 오류: {e}")
            return False

    def broadcast_with_retry(self, max_retries: int = 3, timeout: int = 5000) -> bool:
        """
        Broadcast with retry logic

        Args:
            max_retries: Maximum number of retry attempts (default: 3)
            timeout: Timeout in milliseconds for each attempt (default: 5000)

        Returns:
            bool: Success status
        """
        for attempt in range(max_retries):
            try:
                if self.broadcast_environment_change_enhanced(timeout):
                    if attempt > 0:
                        print(f"브로드캐스트 성공 (재시도 {attempt}회 후)")
                    return True

                if attempt < max_retries - 1:
                    print(f"브로드캐스트 실패, 재시도 중... ({attempt + 1}/{max_retries})")

            except Exception as e:
                print(f"브로드캐스트 시도 {attempt + 1} 실패: {e}")

        print(f"모든 재시도 실패 (총 {max_retries}회 시도)")
        return False


__all__ = ['BroadcastManager', 'HWND_BROADCAST', 'WM_SETTINGCHANGE', 'SMTO_ABORTIFHUNG', 'SMTO_BLOCK']
