"""
Path Repair Core Module
PATH diagnosis and repair orchestration
Brain Module System v4.0
"""

from typing import Dict, List, Tuple, Callable, Optional

from .path_discovery import PathDiscovery
from .path_registry import PathRegistry


class PathRepairManager:
    """
    Manages PATH verification and automatic repair for installed tools
    """

    def __init__(self, log_callback: Optional[Callable] = None):
        """
        Initialize PATH Repair Manager

        Args:
            log_callback: Optional callback function for logging
        """
        self.log_callback = log_callback

        # Initialize component modules
        self.discovery = PathDiscovery(log_callback)
        self.registry = PathRegistry(log_callback)

        self.repair_results = {}

    def _log(self, message: str, level: str = "INFO"):
        """Log a message"""
        if self.log_callback:
            self.log_callback(f"[{level}] {message}")
        else:
            print(f"[{level}] {message}")

    def check_tool_in_path(self, tool_name: str) -> bool:
        """Delegate to PathDiscovery"""
        return self.discovery.check_tool_in_path(tool_name)

    def find_tool_installation(self, tool_name: str) -> List[str]:
        """Delegate to PathDiscovery"""
        return self.discovery.find_tool_installation(tool_name)

    def get_current_system_path(self) -> List[str]:
        """Delegate to PathRegistry"""
        return self.registry.get_current_system_path()

    def get_current_user_path(self) -> List[str]:
        """Delegate to PathRegistry"""
        return self.registry.get_current_user_path()

    def diagnose_path_issues(self) -> Dict[str, Dict]:
        """
        Diagnose PATH issues for all tools

        Returns:
            Dictionary with diagnosis results for each tool
        """
        self._log("=" * 60)
        self._log("PATH 진단 및 복구를 시작합니다")
        self._log("=" * 60)

        diagnosis = {}
        system_path = self.registry.get_current_system_path()
        user_path = self.registry.get_current_user_path()
        all_paths = system_path + user_path

        tools_to_check = [
            ('git', 'Git'),
            ('node', 'Node.js'),
            ('npm', 'npm')
        ]

        for cmd_name, display_name in tools_to_check:
            self._log(f"\n{display_name} 확인 중...")

            # Map command names to tool names for path lookup
            tool_key = 'nodejs' if cmd_name == 'node' else cmd_name

            result = {
                'display_name': display_name,
                'in_path': False,
                'found_installations': [],
                'missing_from_path': [],
                'needs_repair': False
            }

            # Check if tool works
            result['in_path'] = self.discovery.check_tool_in_path(cmd_name)

            if result['in_path']:
                self._log(f"  [OK] {display_name}이(가) 정상적으로 작동합니다", "SUCCESS")
            else:
                self._log(f"  [X] {display_name}에 접근할 수 없습니다", "WARNING")

                # Find installations
                installations = self.discovery.find_tool_installation(tool_key)
                result['found_installations'] = installations

                if installations:
                    self._log(f"  {len(installations)}개의 설치 경로를 찾았습니다")

                    # Check which are missing from PATH
                    for install_path in installations:
                        if install_path not in all_paths:
                            result['missing_from_path'].append(install_path)
                            self._log(f"    - PATH에서 누락됨: {install_path}", "WARNING")

                    if result['missing_from_path']:
                        result['needs_repair'] = True
                        self._log(f"  [!] {display_name}의 PATH 복구가 필요합니다", "WARNING")
                else:
                    self._log(f"  [X] {display_name} 설치를 찾을 수 없습니다", "ERROR")

            diagnosis[cmd_name] = result

        return diagnosis

    def repair_path_for_tool(self, tool_name: str, missing_paths: List[str]) -> bool:
        """
        Repair PATH for a specific tool

        Args:
            tool_name: Name of the tool
            missing_paths: Paths to add to system PATH

        Returns:
            bool: True if repair was successful
        """
        if not missing_paths:
            return True

        self._log(f"\n{tool_name}의 PATH를 복구하는 중...")

        try:
            # Import the unified PATH manager with immediate effect
            from ..path_manager import add_to_path_immediate, add_to_system_path

            # Add missing paths
            self._log(f"  시스템 PATH에 {len(missing_paths)}개의 경로를 추가하는 중")
            for path in missing_paths:
                self._log(f"    + {path}")

            # Try enhanced method first
            success = add_to_path_immediate(missing_paths)

            if success:
                self._log(f"  [OK] {tool_name}의 PATH 복구가 성공했습니다", "SUCCESS")
                self._log("  새 터미널에서 즉시 사용할 수 있습니다", "SUCCESS")
                return True
            else:
                # Fallback to basic method
                self._log("  [!] 향상된 방법이 실패했습니다. 기본 PATH 업데이트를 사용합니다", "WARNING")

                for path in missing_paths:
                    if add_to_system_path(path):
                        self._log(f"    + 추가됨: {path}")
                    else:
                        self._log(f"    [X] 추가 실패: {path}", "ERROR")

                self._log("  [!] PATH가 업데이트되었지만 터미널을 다시 시작해야 합니다", "WARNING")
                return True

        except Exception as e:
            self._log(f"  [X] PATH 복구 실패: {e}", "ERROR")
            return False

    def auto_repair_all(self) -> Tuple[bool, Dict]:
        """
        Automatically diagnose and repair all PATH issues

        Returns:
            Tuple of (success, results_dict)
        """
        self._log("\n" + "=" * 60)
        self._log("자동 PATH 복구를 시작합니다")
        self._log("=" * 60)

        # Diagnose issues
        diagnosis = self.diagnose_path_issues()

        # Count issues
        tools_needing_repair = [
            (name, info) for name, info in diagnosis.items()
            if info['needs_repair']
        ]

        if not tools_needing_repair:
            self._log("\n[OK] 모든 도구가 PATH에 올바르게 구성되어 있습니다!", "SUCCESS")
            return True, diagnosis

        # Perform repairs
        self._log(f"\n{len(tools_needing_repair)}개의 도구가 PATH 복구를 필요로 합니다")
        self._log("-" * 40)

        repair_success = True
        for tool_name, info in tools_needing_repair:
            display_name = info['display_name']
            missing_paths = info['missing_from_path']

            if missing_paths:
                success = self.repair_path_for_tool(display_name, missing_paths)
                info['repair_attempted'] = True
                info['repair_success'] = success

                if not success:
                    repair_success = False
            else:
                self._log(f"\n[!] {display_name}이(가) 설치되지 않았습니다", "WARNING")
                info['repair_attempted'] = False
                info['repair_success'] = False

        # Final summary
        self._log("\n" + "=" * 60)
        self._log("PATH 복구 요약")
        self._log("=" * 60)

        for tool_name, info in diagnosis.items():
            display_name = info['display_name']

            if info.get('repair_attempted'):
                if info.get('repair_success'):
                    self._log(f"  [OK] {display_name}: PATH가 성공적으로 복구되었습니다", "SUCCESS")
                else:
                    self._log(f"  [!] {display_name}: PATH 복구가 부분적으로 완료되었습니다", "WARNING")
            elif info['in_path']:
                self._log(f"  [OK] {display_name}: 이미 정상 작동 중", "SUCCESS")
            else:
                self._log(f"  [X] {display_name}: 설치되지 않음", "INFO")

        if repair_success:
            self._log("\n[OK] PATH 복구가 성공적으로 완료되었습니다!", "SUCCESS")
            self._log("  새 터미널에서 복구된 도구에 즉시 접근할 수 있습니다.", "INFO")
        else:
            self._log("\n[!] PATH 복구가 경고와 함께 완료되었습니다", "WARNING")
            self._log("  일부 도구는 터미널 재시작이 필요할 수 있습니다.", "INFO")

        return repair_success, diagnosis

    def verify_repair(self) -> Dict[str, bool]:
        """
        Verify if repairs were successful

        Returns:
            Dictionary of tool_name: is_working
        """
        self._log("\nPATH 복구를 검증하는 중...")

        results = {}
        tools = [('git', 'Git'), ('node', 'Node.js'), ('npm', 'npm')]

        for cmd_name, display_name in tools:
            working = self.discovery.check_tool_in_path(cmd_name)
            results[cmd_name] = working

            if working:
                self._log(f"  [OK] {display_name}에 이제 접근할 수 있습니다", "SUCCESS")
            else:
                self._log(f"  [X] {display_name}에 여전히 접근할 수 없습니다", "WARNING")

        return results


__all__ = ['PathRepairManager']
