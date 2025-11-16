"""
VSCode Settings Manager
VSCode의 settings.json을 관리하고 터미널 PATH 설정을 자동 수정하는 유틸리티
"""

import os
import json
from pathlib import Path
from typing import Optional


class VSCodeSettingsManager:
    """VSCode settings.json 관리 클래스"""

    def __init__(self):
        """settings.json 경로 초기화"""
        appdata = os.getenv('APPDATA')
        if appdata:
            self.settings_path = Path(appdata) / 'Code' / 'User' / 'settings.json'
        else:
            self.settings_path = None

    def is_vscode_installed(self) -> bool:
        """
        VSCode 설치 여부 확인

        Returns:
            bool: VSCode가 설치되어 있으면 True, 아니면 False
        """
        if not self.settings_path:
            return False

        # settings.json 파일이 없어도 User 폴더가 있으면 설치된 것으로 간주
        user_dir = self.settings_path.parent
        return user_dir.exists()

    def _read_settings(self) -> dict:
        """
        settings.json 파일 읽기

        Returns:
            dict: settings 내용, 파일이 없으면 빈 딕셔너리
        """
        if not self.settings_path or not self.settings_path.exists():
            return {}

        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"settings.json 읽기 실패: {e}")
            return {}

    def _save_settings(self, settings: dict):
        """
        settings.json 파일 저장

        Args:
            settings: 저장할 settings 딕셔너리
        """
        if not self.settings_path:
            return

        # User 디렉토리가 없으면 생성
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            print(f"settings.json 저장 완료: {self.settings_path}")
        except Exception as e:
            print(f"settings.json 저장 실패: {e}")

    def auto_fix_vscode_terminal_path(self):
        """
        VSCode 터미널의 PATH 환경변수 자동 수정

        terminal.integrated.env.windows 설정이 있는 경우:
        - Git, Node.js 관련 필수 경로를 PATH에 추가
        - 이미 존재하는 경로는 중복 추가하지 않음
        - 실제 존재하는 경로만 추가
        """
        try:
            # VSCode 미설치 시 조용히 종료
            if not self.is_vscode_installed():
                return

            # settings.json 읽기
            settings = self._read_settings()

            # terminal.integrated.env.windows 설정이 없으면 정상 종료
            if 'terminal.integrated.env.windows' not in settings:
                return

            env_settings = settings['terminal.integrated.env.windows']

            # PATH 설정이 없으면 정상 종료
            if 'PATH' not in env_settings:
                return

            current_path = env_settings['PATH']

            # 필수 경로 정의
            required_paths = [
                r'C:\Program Files\Git\cmd',
                r'C:\Program Files\Git\bin',
                r'C:\Program Files\nodejs',
                os.path.expandvars(r'%APPDATA%\npm')
            ]

            # 현재 PATH를 세미콜론으로 분리
            path_list = [p.strip() for p in current_path.split(';') if p.strip()]

            # 대소문자 무시하고 비교하기 위해 소문자 버전 생성
            path_list_lower = [p.lower() for p in path_list]

            # 추가된 경로 추적
            added_paths = []

            # 각 필수 경로 확인
            for req_path in required_paths:
                # 경로가 실제로 존재하는지 확인
                if not os.path.exists(req_path):
                    continue

                # 이미 PATH에 있는지 확인 (대소문자 무시)
                if req_path.lower() in path_list_lower:
                    continue

                # PATH에 추가
                path_list.append(req_path)
                path_list_lower.append(req_path.lower())
                added_paths.append(req_path)

            # 새로운 경로가 추가되었으면 저장
            if added_paths:
                new_path = ';'.join(path_list)
                env_settings['PATH'] = new_path
                settings['terminal.integrated.env.windows'] = env_settings

                self._save_settings(settings)

                print("VSCode 터미널 PATH 수정 완료:")
                for path in added_paths:
                    print(f"  - 추가됨: {path}")

        except Exception as e:
            # 모든 예외는 조용히 무시
            pass


# 테스트용 코드
if __name__ == '__main__':
    manager = VSCodeSettingsManager()

    if manager.is_vscode_installed():
        print("VSCode가 설치되어 있습니다.")
        print(f"설정 파일 경로: {manager.settings_path}")

        print("\nPATH 자동 수정 실행...")
        manager.auto_fix_vscode_terminal_path()
    else:
        print("VSCode가 설치되어 있지 않습니다.")
