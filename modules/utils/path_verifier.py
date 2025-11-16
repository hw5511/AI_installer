"""
PATH Verifier Module - Facade Pattern
Dual verification system: Registry + Execution
Brain Module System v4.0
"""
from typing import Dict, List, Optional, Any

# Handle both relative and absolute imports
try:
    from .verifier_components.registry_checker import RegistryChecker
    from .verifier_components.tool_executor import ToolExecutor
    from .verifier_components.verification_ui import VerificationUI, TerminalVerificationUI
except ImportError:
    from verifier_components.registry_checker import RegistryChecker
    from verifier_components.tool_executor import ToolExecutor
    from verifier_components.verification_ui import VerificationUI, TerminalVerificationUI

try:
    from modules.core.config import Config
    _config = Config()
except Exception:
    _config = None


class PathVerifier:
    """
    PATH verification system - Facade
    Registry 직접 확인 + 실행 테스트
    """

    def __init__(self, log_callback=None):
        """Initialize with all verifier components"""
        self.log_callback = log_callback
        self.registry_checker = RegistryChecker(log_callback)
        self.tool_executor = ToolExecutor(log_callback)
        self.verification_ui = None
        self.terminal_ui = TerminalVerificationUI(log_callback, _config)

        # Tool definitions
        self.tools = {
            'Git': {
                'command': 'git',
                'args': ['--version'],
                'expected_paths': ['Git\\cmd', 'Git\\bin']
            },
            'Node.js': {
                'command': 'node',
                'args': ['--version'],
                'expected_paths': ['nodejs']
            },
            'NPM': {
                'command': 'npm',
                'args': ['--version'],
                'expected_paths': ['nodejs', 'npm']
            },
            'Claude CLI': {
                'command': 'claude',
                'args': ['--version'],
                'expected_paths': ['npm']
            },
            'Gemini CLI': {
                'command': 'gemini',
                'args': ['--version'],
                'expected_paths': ['npm']
            }
        }

    def log(self, message: str):
        """Log a message"""
        if self.log_callback:
            self.log_callback(message)
        print(message)

    def get_registry_paths(self) -> Dict[str, List[str]]:
        """
        Get PATH entries directly from Windows Registry
        Delegates to RegistryChecker

        Returns:
            dict: {'Machine': [...], 'User': [...]}
        """
        return self.registry_checker.get_registry_paths()

    def check_tool_in_registry_path(self, tool_name: str, command_info: Dict) -> Dict:
        """
        Check if tool's expected paths are in the registry PATH
        Delegates to RegistryChecker

        Args:
            tool_name: Name of the tool
            command_info: Tool configuration with expected_paths

        Returns:
            dict: Registry check result
        """
        return self.registry_checker.check_tool_in_registry(tool_name, command_info)

    def verify_single_tool(self, tool_name: str, command_info: Dict) -> Dict:
        """
        Verify a single tool in a new process
        Delegates to ToolExecutor

        Args:
            tool_name: Name of the tool
            command_info: Dictionary with 'command' and 'args'

        Returns:
            dict: Verification result with status, version, etc.
        """
        return self.tool_executor.execute_tool(tool_name, command_info)

    def verify_with_comparison(self) -> Dict:
        """
        Verify all tools using both methods and compare results
        Primary verification API

        Returns:
            dict: Comprehensive verification results with comparison
        """
        results = {'summary': {}, 'details': [], 'discrepancies': []}

        self.log("=" * 60)
        self.log("레지스트리 비교와 함께하는 PATH 검증")
        self.log("=" * 60)
        self.log("")

        for tool_name, command_info in self.tools.items():
            self.log(f"{tool_name} 확인 중...")
            self.log("-" * 40)

            # Dual verification: Registry + Execution
            registry_result = self.check_tool_in_registry_path(tool_name, command_info)
            execution_result = self.verify_single_tool(tool_name, command_info)

            # Build comparison
            comparison = {
                'tool': tool_name,
                'registry_check': {
                    'in_path': registry_result['in_registry'],
                    'executable_found': registry_result['executable_found'],
                    'executable_path': registry_result['executable_path'],
                    'found_in': registry_result['found_paths'][:3] if registry_result['found_paths'] else []
                },
                'execution_check': {
                    'success': execution_result['status'] == 'success',
                    'version': execution_result.get('version'),
                    'status': execution_result['status']
                },
                'match': registry_result['in_registry'] == (execution_result['status'] == 'success')
            }

            # Log detailed results
            self._log_comparison_results(registry_result, execution_result, comparison)

            # Track discrepancies
            if not comparison['match']:
                discrepancy_msg = f"{tool_name}: 레지스트리={'발견됨' if registry_result['in_registry'] else '누락'}, 실행={'정상' if execution_result['status'] == 'success' else '실패'}"
                results['discrepancies'].append(discrepancy_msg)
                self.log(f"  [경고] 불일치가 감지되었습니다!")
                self.log(f"    이는 PATH 변경사항이 아직 반영되지 않았음을 의미합니다")

            results['details'].append(comparison)
            self.log("")

        # Generate summary
        results['summary'] = self._generate_summary(results['details'])
        self._log_summary(results)

        return results

    def _log_comparison_results(self, reg: Dict, exe: Dict, comp: Dict):
        """Log comparison results"""
        self.log(f"  레지스트리 PATH: {'발견됨' if reg['in_registry'] else '찾을 수 없음'}")
        if reg['executable_found']:
            self.log(f"    실행 파일: {reg['executable_path']}")
        if reg['found_paths']:
            self.log(f"    경로에서 발견: {reg['found_paths'][0]}")
        self.log(f"  실행 테스트: {'성공' if exe['status'] == 'success' else '실패'}")
        if exe['status'] == 'success':
            self.log(f"    버전: {exe['version']}")

    def _generate_summary(self, details: List[Dict]) -> Dict:
        """Generate summary"""
        total = len(self.tools)
        reg_found = sum(1 for d in details if d['registry_check']['in_path'])
        exe_success = sum(1 for d in details if d['execution_check']['success'])
        matches = sum(1 for d in details if d['match'])
        return {
            'total_tools': total,
            'registry_found': reg_found,
            'execution_success': exe_success,
            'matches': matches,
            'all_working': exe_success == total,
            'all_match': matches == total
        }

    def _log_summary(self, results: Dict):
        """Log summary"""
        s = results['summary']
        self.log("=" * 60 + "\n요약\n" + "=" * 60)
        self.log(f"레지스트리 PATH에 있는 도구: {s['registry_found']}/{s['total_tools']}")
        self.log(f"정상적으로 실행되는 도구: {s['execution_success']}/{s['total_tools']}")
        self.log(f"일치하는 결과: {s['matches']}/{s['total_tools']}")
        if results['discrepancies']:
            self.log("\n불일치 발견:")
            for disc in results['discrepancies']:
                self.log(f"  - {disc}")
            self.log("\n가능한 원인:\n  1. PATH 변경사항이 현재 세션에 아직 반영되지 않음")
            self.log("  2. 터미널/IDE가 이전 PATH를 캐싱하고 있음\n  3. 터미널 또는 IDE 재시작 필요")

    def verify_all_silent(self) -> List[Dict]:
        """Verify all tools silently - quick verification without comparison"""
        results = []
        self.log("새 프로세스에서 PATH 검증 시작...")
        for tool_name, command_info in self.tools.items():
            self.log(f"{tool_name} 검증 중...")
            result = self.verify_single_tool(tool_name, command_info)
            results.append(result)

            # 실행 가능하면 메시지 없음 (성공 시 조용히)
            if result['status'] == 'success':
                continue  # 성공 시 로그 출력 안 함

            # 실패한 경우만 로그 출력
            status = '실패'
            detail = result.get('version', result['status'])
            self.log(f"  [{status}] {tool_name}: {detail}")
        return results

    def verify_with_visual_feedback(self, parent_window=None) -> List[Dict]:
        """Verify with GUI - delegates to VerificationUI"""
        self.verification_ui = VerificationUI(self)
        return self.verification_ui.show_verification_window(parent_window)

    def verify_in_new_terminal(self):
        """Open terminal for manual verification - delegates to TerminalVerificationUI"""
        self.terminal_ui.open_verification_terminal()

    def get_verification_summary(self, results: List[Dict]) -> Dict:
        """Get verification summary with counts and details"""
        summary = {'total': len(results), 'success': 0, 'failed': 0, 'details': []}
        for result in results:
            if result['status'] == 'success':
                summary['success'] += 1
                summary['details'].append(f"{result['tool']}: 정상 ({result['version']})")
            else:
                summary['failed'] += 1
                summary['details'].append(f"{result['tool']}: 실패 ({result['status']})")
        summary['all_working'] = summary['success'] == summary['total']
        return summary


__all__ = ['PathVerifier']


if __name__ == "__main__":
    v = PathVerifier()
    print("자동 검증 테스트 중...")
    r = v.verify_all_silent()
    s = v.get_verification_summary(r)
    print(f"\n요약: {s['success']}/{s['total']}개 도구가 작동 중")
    v.verify_with_visual_feedback()
    v.verify_in_new_terminal()