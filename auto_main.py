#!/usr/bin/env python3
"""
AI 개발 환경 자동 설치 도구 - 메인 실행 파일

이 파일은 auto_main 패키지의 자동 설치 시스템을 실행합니다.
Git, Node.js, Claude CLI를 순차적으로 자동 설치하며,
사용자 친화적인 GUI 인터페이스를 제공합니다.

사용법:
    python auto_main.py

요구사항:
    - Windows 10/11
    - Python 3.8+
    - 관리자 권한 (패키지 설치용)
    - 인터넷 연결

Author: Woohee Dev Team
Version: 1.0.0
License: MIT
"""

import sys
import os
import traceback
import tkinter as tk
from tkinter import messagebox

# 현재 디렉토리를 sys.path에 추가하여 모듈 import 가능하게 함
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from auto_main import AutoGUI
except ImportError as e:
    print(f"❌ 모듈 import 오류: {e}")
    print("auto_main 패키지를 찾을 수 없습니다.")
    print("파일 경로를 확인해주세요.")
    sys.exit(1)


def check_python_version():
    """Python 버전 확인"""
    if sys.version_info < (3, 8):
        messagebox.showerror(
            "Python 버전 오류",
            f"Python 3.8 이상이 필요합니다.\n"
            f"현재 버전: {sys.version}\n\n"
            f"Python을 업그레이드해주세요."
        )
        return False
    return True


def check_admin_privileges():
    """관리자 권한 확인 (Windows)"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# 관리자 권한 경고 함수 제거 (manifest.xml에서 requireAdministrator 설정으로 대체)


def setup_error_handling():
    """전역 오류 처리 설정"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        """예외 처리 함수"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(f"❌ 예상치 못한 오류 발생:\n{error_msg}")

        # GUI가 있으면 메시지박스로 표시
        try:
            messagebox.showerror(
                "예상치 못한 오류",
                f"프로그램 실행 중 오류가 발생했습니다:\n\n"
                f"{exc_type.__name__}: {exc_value}\n\n"
                f"자세한 오류 정보는 콘솔을 확인해주세요."
            )
        except:
            pass

    sys.excepthook = handle_exception


def print_startup_info():
    """시작 정보 출력"""
    try:
        print("=" * 70)
        print("AI 개발 환경 자동 설치 도구 v1.0.0")
        print("=" * 70)
        print(f"실행 경로: {current_dir}")
        print(f"Python 버전: {sys.version}")
        print(f"운영체제: {os.name}")

        if os.name == 'nt':  # Windows
            admin_status = "관리자" if check_admin_privileges() else "일반 사용자"
            print(f"권한 상태: {admin_status}")

        print("=" * 70)
    except UnicodeEncodeError:
        # 인코딩 오류 시 기본 ASCII로 출력
        print("=" * 70)
        print("AI Development Environment Auto Installer v1.0.0")
        print("=" * 70)


def main():
    """메인 함수"""
    try:
        # 시작 정보 출력
        print_startup_info()

        # Python 버전 확인
        if not check_python_version():
            return 1

        # 전역 오류 처리 설정
        setup_error_handling()

        # 관리자 권한 확인 (manifest.xml의 requireAdministrator로 보장됨)
        if os.name == 'nt':
            if check_admin_privileges():
                print("[OK] 관리자 권한으로 실행 중입니다.")
            else:
                print("[WARNING] 경고: 관리자 권한이 필요합니다.")
                print("프로그램을 우클릭하여 '관리자 권한으로 실행'해주세요.")

        print("GUI 인터페이스를 시작합니다...")

        # GUI 애플리케이션 시작
        root = tk.Tk()
        app = AutoGUI(root)

        print("GUI 초기화 완료")
        print("사용자 인터랙션 대기 중...")
        print("=" * 70)

        # GUI 실행
        app.run()

        print("프로그램이 정상적으로 종료되었습니다.")
        return 0

    except KeyboardInterrupt:
        print("\n사용자가 프로그램을 중단했습니다.")
        return 0

    except ImportError as e:
        print(f"모듈 import 오류: {e}")
        print("필요한 패키지가 설치되어 있는지 확인해주세요.")
        try:
            messagebox.showerror(
                "모듈 오류",
                f"필요한 모듈을 찾을 수 없습니다:\n{e}\n\n"
                f"패키지 설치 상태를 확인해주세요."
            )
        except:
            pass
        return 1

    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        traceback.print_exc()
        try:
            messagebox.showerror(
                "치명적 오류",
                f"프로그램 시작 중 치명적 오류가 발생했습니다:\n\n"
                f"{type(e).__name__}: {e}\n\n"
                f"프로그램을 다시 시작해주세요."
            )
        except:
            pass
        return 1


if __name__ == "__main__":
    """프로그램 진입점"""
    exit_code = main()
    sys.exit(exit_code)