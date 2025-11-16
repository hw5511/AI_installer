"""
Custom exception classes for AI Setup Tool
"""

class AISetupError(Exception):
    """Base exception for AI Setup Tool"""
    pass

class ToolInstallationError(AISetupError):
    """Exception raised during tool installation"""
    pass

class ToolUninstallationError(AISetupError):
    """Exception raised during tool uninstallation"""
    pass

class ToolCheckError(AISetupError):
    """Exception raised when checking tool status"""
    pass

class AdminPrivilegeError(AISetupError):
    """Exception raised when admin privileges are required"""
    pass

class ChocolateyNotFoundError(AISetupError):
    """Exception raised when Chocolatey is not installed"""
    pass

class CommandExecutionError(AISetupError):
    """Exception raised during command execution"""
    def __init__(self, command, return_code, error_message=""):
        self.command = command
        self.return_code = return_code
        self.error_message = error_message
        super().__init__(f"Command failed: {command} (code: {return_code})")