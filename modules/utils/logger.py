"""
Logger Module for AI Setup Tool
Manages logging functionality for the GUI application
"""

import datetime
import os


class LogManager:
    """
    Manages logging functionality for the GUI application.
    Provides methods for logging messages, clearing logs, and saving to files.
    """

    def __init__(self, log_widget, enable_timestamp=True):
        """
        Initialize LogManager with a tkinter ScrolledText widget.

        Args:
            log_widget: tkinter ScrolledText widget for displaying logs
            enable_timestamp (bool): Whether to automatically add timestamps to messages
        """
        self.log_widget = log_widget
        self.enable_timestamp = enable_timestamp
        self.log_history = []

        # Define color mapping for different log levels
        self.level_colors = {
            'INFO': '#000000',      # Black
            'WARNING': '#FF8C00',   # Dark Orange
            'ERROR': '#FF0000',     # Red
            'SUCCESS': '#008000',   # Green
            'DEBUG': '#808080'      # Gray
        }

        # Configure text widget tags for colored text (prepare for future use)
        self._configure_text_tags()

    def _configure_text_tags(self):
        """Configure text tags for different log levels with colors."""
        for level, color in self.level_colors.items():
            self.log_widget.tag_configure(level, foreground=color)

    def _get_timestamp(self):
        """Get current timestamp string."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, message, level='INFO'):
        """
        Add message to log window with specified level.

        Args:
            message (str): Message to log
            level (str): Log level (INFO, WARNING, ERROR, SUCCESS, DEBUG)
        """
        if level.upper() not in self.level_colors:
            level = 'INFO'

        # Format message with timestamp if enabled
        if self.enable_timestamp:
            formatted_message = f"[{self._get_timestamp()}] [{level.upper()}] {message}"
        else:
            formatted_message = f"[{level.upper()}] {message}"

        # Add to log history
        self.log_history.append(formatted_message)

        # Insert message into log widget
        self.log_widget.insert('end', f"{formatted_message}\n")
        self.log_widget.see('end')

        # Update the GUI to show the new message
        try:
            self.log_widget.update_idletasks()
        except:
            pass  # Handle case where widget is destroyed

    def clear(self):
        """Clear all log messages from the widget and history."""
        self.log_widget.delete('1.0', 'end')
        self.log_history.clear()

    def save_to_file(self, filepath):
        """
        Save log history to a file.

        Args:
            filepath (str): Path to save the log file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Write log history to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Log file generated on: {self._get_timestamp()}\n")
                f.write("=" * 50 + "\n\n")

                for log_entry in self.log_history:
                    f.write(log_entry + "\n")

            return True

        except Exception as e:
            self.log(f"로그 파일 저장에 실패했습니다: {str(e)}", 'ERROR')
            return False

    def get_log_count(self):
        """Get the number of log entries."""
        return len(self.log_history)

    def get_log_history(self):
        """Get a copy of the log history."""
        return self.log_history.copy()

    def set_timestamp_enabled(self, enabled):
        """Enable or disable timestamp for future log messages."""
        self.enable_timestamp = enabled