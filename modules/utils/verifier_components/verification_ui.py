"""
Verification UI Module
GUI for PATH verification
Brain Module System v4.0
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import subprocess
import tempfile
import os
from typing import Callable, Optional, List, Dict, Any


class VerificationUI:
    """GUI for PATH verification progress"""

    def __init__(self, verifier_callback: Callable):
        """Initialize verification UI"""
        self.verifier = verifier_callback
        self.verify_window = None
        self.status_labels = {}
        self.results = []

    def show_verification_window(self, parent_window: Optional[tk.Tk] = None) -> List[Dict[str, Any]]:
        """Show verification progress window"""
        self.verify_window = tk.Toplevel(parent_window) if parent_window else tk.Tk()
        self.verify_window.title("PATH 검증 도구")
        self.verify_window.geometry("500x400")
        self.verify_window.configure(bg='#2C3E50')

        self._center_window()
        self._build_ui()

        if not parent_window:
            self.verify_window.mainloop()

        return self.results

    def _center_window(self):
        """Center the window on screen"""
        self.verify_window.update_idletasks()
        x = (self.verify_window.winfo_screenwidth() // 2) - 250
        y = (self.verify_window.winfo_screenheight() // 2) - 200
        self.verify_window.geometry(f"500x400+{x}+{y}")

    def _build_ui(self):
        """Build all UI components and start verification"""
        # Title
        tk.Label(self.verify_window, text="새 프로세스에서 도구 검증 중",
                font=('Segoe UI', 14, 'bold'), fg='white', bg='#2C3E50').pack(pady=20)

        # Progress frame
        progress_frame = tk.Frame(self.verify_window, bg='#34495E')
        progress_frame.pack(padx=20, pady=10, fill='both', expand=True)

        for i, (tool_name, _) in enumerate(self.verifier.tools.items()):
            frame = tk.Frame(progress_frame, bg='#34495E')
            frame.grid(row=i, column=0, sticky='ew', padx=20, pady=10)

            tk.Label(frame, text=f"{tool_name}:", font=('Segoe UI', 11),
                    fg='white', bg='#34495E', width=12, anchor='w').grid(row=0, column=0, sticky='w')

            status_label = tk.Label(frame, text="확인 중...", font=('Segoe UI', 10),
                                   fg='#F39C12', bg='#34495E', width=30, anchor='w')
            status_label.grid(row=0, column=1, padx=(10, 0))
            self.status_labels[tool_name] = status_label

        # Progress bar
        progress_bar = ttk.Progressbar(self.verify_window, mode='indeterminate', length=460)
        progress_bar.pack(pady=20)
        progress_bar.start(10)

        # Result text
        result_text = tk.Text(self.verify_window, height=4, bg='#1A252F', fg='white',
                            font=('Consolas', 9), wrap='word')
        result_text.pack(padx=20, pady=(0, 10), fill='x')

        # Close button
        close_button = tk.Button(self.verify_window, text="닫기",
                                command=self.verify_window.destroy,
                                bg='#3498DB', fg='white', font=('Segoe UI', 10),
                                state='disabled')
        close_button.pack(pady=10)

        # Start verification
        threading.Thread(target=lambda: self._run_verification(progress_bar, result_text, close_button),
                        daemon=True).start()

    def _run_verification(self, progress_bar, result_text, close_button):
        """Run verification in background"""
        self.results = []

        for tool_name, command_info in self.verifier.tools.items():
            result = self.verifier.verify_single_tool(tool_name, command_info)
            self.results.append(result)

            self.verify_window.after(0, lambda t=tool_name, r=result:
                                    self._update_status(t, r, result_text))
            time.sleep(0.5)

        self.verify_window.after(0, lambda: self._finalize(progress_bar, result_text, close_button))

    def _update_status(self, tool_name: str, result: Dict[str, Any], result_text: tk.Text):
        """Update tool status"""
        if result['status'] == 'success':
            self.status_labels[tool_name].config(text=f"정상 - {result['version']}", fg='#27AE60')
            result_text.insert('end', f"[정상] {tool_name}: {result['version']}\n")
        else:
            self.status_labels[tool_name].config(text=f"실패 - {result['status']}", fg='#E74C3C')
            result_text.insert('end', f"[실패] {tool_name}: {result['status']}\n")

    def _finalize(self, progress_bar, result_text, close_button):
        """Finalize verification"""
        progress_bar.stop()
        progress_bar.pack_forget()
        close_button.config(state='normal')

        success = sum(1 for r in self.results if r['status'] == 'success')
        total = len(self.results)
        summary = f"\n{'='*50}\n검증 완료: {success}/{total}개 도구가 작동 중\n"
        summary += "모든 도구가 정상적으로 구성되었습니다!" if success == total else "일부 도구에 문제가 있습니다."
        result_text.insert('end', summary)


class TerminalVerificationUI:
    """Terminal-based verification UI for manual testing"""

    def __init__(self, log_callback: Optional[Callable] = None, config=None):
        """Initialize terminal verification UI"""
        self.log_callback = log_callback
        self.config = config

    def log(self, message: str):
        """Log a message"""
        if self.log_callback:
            self.log_callback(message)
        print(message)

    def open_verification_terminal(self):
        """Open new PowerShell terminal for manual verification"""
        script = self._get_verification_script()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
            f.write(script)
            script_path = f.name

        try:
            creationflags = self.config.get_subprocess_flags() if self.config else 0
            subprocess.run([
                'powershell', '-Command',
                f"Start-Process powershell -ArgumentList '-NoExit', '-ExecutionPolicy', "
                f"'Bypass', '-File', '{script_path}' -Verb RunAs"
            ], creationflags=creationflags)

            self.log("수동 검증을 위한 새 터미널이 열렸습니다")

        except Exception as e:
            self.log(f"검증 터미널 열기 실패: {e}")

        finally:
            threading.Thread(target=lambda: self._cleanup_script(script_path), daemon=True).start()

    def _get_verification_script(self) -> str:
        """Get PowerShell verification script"""
        return '''
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "   PATH 검증 테스트" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

$MachinePath = [Environment]::GetEnvironmentVariable('PATH', 'Machine')
$UserPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
$env:PATH = "$MachinePath;$UserPath"

Write-Host "설치된 도구 테스트 중..." -ForegroundColor Yellow
Write-Host ""

@('git', 'node', 'npm', 'claude') | ForEach-Object {
    $tool = $_
    $displayName = @{'git'='Git'; 'node'='Node.js'; 'npm'='NPM'; 'claude'='Claude CLI'}[$tool]
    Write-Host "$displayName : " -NoNewline -ForegroundColor White

    try {
        $version = & $tool --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host $version -ForegroundColor Green
        } else {
            Write-Host "찾을 수 없음" -ForegroundColor Red
        }
    } catch {
        Write-Host "찾을 수 없음" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "현재 PATH:" -ForegroundColor Yellow
$env:PATH -split ';' | Where-Object { $_ -ne '' } | ForEach-Object {
    Write-Host "  $_" -ForegroundColor Gray
}
Write-Host ""
Write-Host "아무 키나 누르면 닫힙니다..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
'''

    def _cleanup_script(self, script_path: str):
        """Clean up temporary script file"""
        time.sleep(5)
        try:
            os.unlink(script_path)
        except:
            pass


__all__ = ['VerificationUI', 'TerminalVerificationUI']
