"""
GUI Logger Module
Log management for auto installation GUI
Brain Module System v4.0
"""

import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import queue
from datetime import datetime


class GUILogger:
    """Handles log display and management"""

    def __init__(self, log_text: scrolledtext.ScrolledText, root: tk.Tk):
        """
        Initialize logger

        Args:
            log_text: ScrolledText widget for displaying logs
            root: Tkinter root window for scheduling
        """
        self.log_text = log_text
        self.root = root
        self.log_queue = queue.Queue()

        # 로그 큐 처리 시작
        self.root.after(100, self._process_log_queue)

    def add_log(self, message: str):
        """로그 메시지를 큐에 추가 (스레드 안전)"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}")

    def _process_log_queue(self):
        """로그 큐 처리"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self._append_log_directly(message)
        except queue.Empty:
            pass

        # 다음 처리 예약
        self.root.after(100, self._process_log_queue)

    def _append_log_directly(self, message: str):
        """로그 텍스트에 직접 추가"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def clear_log(self):
        """로그 지우기"""
        response = messagebox.askyesno(
            "로그 지우기",
            "로그를 모두 지우시겠습니까?",
            icon="question"
        )

        if response:
            self.log_text.config(state="normal")
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state="disabled")
            self.add_log("로그가 지워졌습니다.")

    def save_log(self):
        """로그 저장"""
        try:
            filename = filedialog.asksaveasfilename(
                title="로그 저장",
                defaultextension=".txt",
                filetypes=[
                    ("텍스트 파일", "*.txt"),
                    ("모든 파일", "*.*")
                ],
                initialfile=f"ai_setup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )

            if filename:
                log_content = self.log_text.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"AI 개발 환경 자동 설치 로그\n")
                    f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 70 + "\n\n")
                    f.write(log_content)

                self.add_log(f"로그가 저장되었습니다: {filename}")
                messagebox.showinfo("저장 완료", f"로그가 저장되었습니다:\n{filename}")

        except Exception as e:
            self.add_log(f"로그 저장 실패: {str(e)}")
            messagebox.showerror("저장 실패", f"로그 저장 중 오류가 발생했습니다:\n{str(e)}")


__all__ = ['GUILogger']
