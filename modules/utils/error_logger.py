"""
에러 로그 파일 자동 생성 및 관리 모듈
설치 실패 시 exe 실행 위치에 로그 파일을 자동으로 저장
"""

import os
import sys
import platform
import traceback
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class ErrorLogManager:
    """설치 실패 시 에러 로그를 파일로 저장하는 관리자 클래스"""

    def __init__(self, exe_path: Optional[str] = None):
        """
        초기화

        Args:
            exe_path: 실행 파일 경로 (None이면 자동 감지)
        """
        # exe 실행 경로 감지
        if exe_path:
            self.exe_dir = os.path.dirname(exe_path)
        elif getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 exe인 경우
            self.exe_dir = os.path.dirname(sys.executable)
        else:
            # 개발 환경에서 실행되는 경우
            self.exe_dir = os.getcwd()

        # 로그 항목 저장
        self.log_entries: List[Tuple[str, str, str]] = []  # (timestamp, level, message)

        # 에러 발생 여부
        self.error_occurred = False

        # 시스템 정보 수집
        self.system_info = self._collect_system_info()

        # 에러 상세 정보
        self.error_details: List[Dict] = []

    def _collect_system_info(self) -> Dict[str, str]:
        """시스템 정보 수집"""
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False

        return {
            'os': f"{platform.system()} {platform.release()} ({platform.version()})",
            'python_version': sys.version.split()[0],
            'is_admin': str(is_admin),
            'exe_path': sys.executable if getattr(sys, 'frozen', False) else 'Development Mode',
            'working_dir': os.getcwd(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def add_entry(self, message: str, level: str = "INFO"):
        """
        로그 항목 추가

        Args:
            message: 로그 메시지
            level: 로그 레벨 (INFO, WARNING, ERROR)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_entries.append((timestamp, level, message))

        # 에러 레벨인 경우 플래그 설정
        if level == "ERROR":
            self.error_occurred = True

    def add_error_detail(self, step: str, error_message: str, traceback_info: Optional[str] = None):
        """
        에러 상세 정보 추가

        Args:
            step: 실패한 단계
            error_message: 에러 메시지
            traceback_info: 스택 트레이스 정보
        """
        self.error_details.append({
            'step': step,
            'error_message': error_message,
            'traceback': traceback_info,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.error_occurred = True

    def save_error_log(self) -> Optional[str]:
        """
        에러 로그 파일 저장 (실패 시에만)

        Returns:
            str: 저장된 로그 파일 경로 (성공 시), None (실패 시 또는 에러 없음)
        """
        # 에러가 없으면 저장하지 않음
        if not self.error_occurred:
            return None

        try:
            # 로그 파일명 생성 (타임스탬프 포함)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_filename = f"ai_setup_error_{timestamp}.log"
            log_filepath = os.path.join(self.exe_dir, log_filename)

            # 로그 내용 작성
            with open(log_filepath, 'w', encoding='utf-8') as f:
                # 헤더
                f.write("=" * 70 + "\n")
                f.write("AI 개발 환경 자동 설치 - 에러 로그\n")
                f.write("=" * 70 + "\n")
                f.write(f"생성 시간: {self.system_info['timestamp']}\n")
                f.write(f"설치 실행 파일: {self.system_info['exe_path']}\n\n")

                # 시스템 정보
                f.write("[시스템 정보]\n")
                f.write(f"- OS: {self.system_info['os']}\n")
                f.write(f"- Python 버전: {self.system_info['python_version']}\n")
                f.write(f"- 관리자 권한: {self.system_info['is_admin']}\n")
                f.write(f"- 실행 경로: {self.system_info['working_dir']}\n\n")

                # 설치 진행 로그
                f.write("[설치 진행 로그]\n")
                for timestamp, level, message in self.log_entries:
                    prefix = ""
                    if level == "ERROR":
                        prefix = "❌ "
                    elif level == "WARNING":
                        prefix = "⚠️ "
                    f.write(f"[{timestamp}] {prefix}{message}\n")
                f.write("\n")

                # 에러 상세 정보
                if self.error_details:
                    f.write("[에러 상세]\n")
                    for idx, error in enumerate(self.error_details, 1):
                        f.write(f"\n--- 에러 #{idx} ---\n")
                        f.write(f"발생 시각: {error['timestamp']}\n")
                        f.write(f"실패 단계: {error['step']}\n")
                        f.write(f"에러 메시지: {error['error_message']}\n")
                        if error.get('traceback'):
                            f.write(f"스택 트레이스:\n{error['traceback']}\n")
                    f.write("\n")

                # 푸터
                f.write("=" * 70 + "\n")
                f.write("문제가 지속될 경우, 이 로그 파일을 아래 이메일로 보내주세요:\n")
                f.write("📧 yangheewoo5511@gmail.com\n")
                f.write("   (문제 상황 설명과 함께 첨부 부탁드립니다)\n")
                f.write("=" * 70 + "\n")

            return log_filepath

        except Exception as e:
            # 로그 저장 실패 시 (하지만 이 예외는 무시)
            print(f"로그 파일 저장 실패: {e}")
            return None

    def get_log_summary(self) -> str:
        """로그 요약 반환"""
        error_count = sum(1 for _, level, _ in self.log_entries if level == "ERROR")
        warning_count = sum(1 for _, level, _ in self.log_entries if level == "WARNING")

        return (
            f"총 로그 항목: {len(self.log_entries)}\n"
            f"에러: {error_count}개\n"
            f"경고: {warning_count}개"
        )
