# AI Auto Installer

**Windows AI Development Environment - One-Click Setup Tool**

Automatically installs and configures essential AI development tools for Windows with intelligent PATH management and VSCode integration.

## Features

### Automated Installation
- Git version control system
- Node.js runtime and npm package manager
- Claude Code CLI (Anthropic AI coding assistant)
- Google Gemini CLI (Google AI coding assistant)

### Smart Configuration
- Automatic PATH environment variable management
- VSCode terminal integration and optimization
- Registry-based verification system
- Immediate tool availability after installation

### User Experience
- Clean GUI interface with real-time progress tracking
- No manual configuration required
- Silent auto-fix for VSCode terminal issues
- Complete Korean language support

## System Requirements

- **OS**: Windows 10 (1909+) or Windows 11
- **Python**: 3.8 or higher (for development only)
- **Privileges**: Administrator access required
- **Network**: Internet connection for downloads

## Quick Start

### Download and Run

1. Download the latest release: `AI_Auto_Installer.exe`
2. Run as administrator
3. Wait for installation to complete
4. Restart VSCode if using
5. All tools ready to use!

### Build from Source

```bash
# Clone repository
git clone https://github.com/hw5511/AI_installer.git
cd AI_installer

# Install dependencies
pip install pyinstaller pywin32

# Build executable
python build_auto.py

# Output: dist_auto/AI_Auto_Installer.exe (10MB)
```

## Architecture

### Brain Module System v4.0

Modular architecture with clear separation of concerns:

```
AI_installer/
├── auto_main/              # Installation orchestration
│   ├── auto_gui.py         # GUI controller
│   ├── auto_installer.py   # Installation workflow
│   ├── gui_modules/        # UI components
│   └── installer_modules/  # Step executors
│
└── modules/                # Core systems
    ├── core/               # Business logic
    │   ├── config/         # Configuration management
    │   ├── installer/      # Installation components
    │   └── checker/        # Verification systems
    ├── ui/                 # User interface
    └── utils/              # Utilities
        ├── path_manager    # PATH operations
        ├── verifier        # Verification tools
        └── vscode_manager  # VSCode integration
```

### Design Patterns

- **Facade Pattern**: Simplified interfaces for complex subsystems
- **Strategy Pattern**: Pluggable installation steps
- **Builder Pattern**: Flexible UI construction
- **Bridge Pattern**: GUI-installer separation

## Technical Details

### Installation Flow

1. **Step 1**: Chocolatey package manager installation
2. **Step 2**: Git installation and PATH configuration
3. **Step 3**: Node.js and npm setup with User PATH
4. **Step 4**: Claude Code CLI via npm global install
5. **Step 5**: Google Gemini CLI via npm global install
6. **Step 6**: VSCode terminal PATH auto-optimization

### PATH Management

- System PATH for Git and Node.js
- User PATH for npm global packages
- Environment variable expansion support (`%APPDATA%\npm`)
- WM_SETTINGCHANGE broadcast for immediate effect
- No reboot required

### VSCode Integration

Automatically fixes common VSCode terminal issues:

- Detects hardcoded PATH in settings.json
- Adds missing tool paths to terminal environment
- Preserves user configurations
- Silent operation without popups

### Verification System

Three-tier verification for reliability:

1. **File Existence**: Checks installation directories
2. **Registry Check**: Validates PATH entries
3. **Execution Test**: Runs actual commands in new shell

## Project Statistics

- **Total Files**: 62 Python modules
- **Total Lines**: 8,636 lines of code
- **Average File Size**: 139 lines
- **Architecture**: 11 sub-modules with Facade pattern
- **Build Size**: 10MB standalone executable

## Development

### Code Standards

- UTF-8 encoding
- PEP 8 compliance
- Type hints for clarity
- Comprehensive docstrings
- No emoji in code (encoding safety)

### Testing

```bash
# Run from source
python auto_main.py

# Test specific components
python -m modules.utils.vscode_settings_manager
```

### Contributing

This is a personal project, but feel free to fork and adapt for your needs.

## Troubleshooting

### VSCode Not Detecting Tools

1. Completely close VSCode (check Task Manager)
2. Reopen VSCode
3. Open new terminal
4. Test commands: `git -v`, `claude -v`, `gemini -v`

### Manual PATH Refresh (if needed)

In VSCode terminal:
```powershell
$env:PATH = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
```

## Version History

### v3.2 (Current)
- VSCode terminal PATH automatic optimization
- Silent auto-fix for `terminal.integrated.env.windows`
- Enhanced verification system
- 62 files, 8,636 lines

### v3.1
- Complete modularization
- 11 sub-modules with Facade pattern
- SOLID principles implementation

### v3.0
- Initial auto-installation system
- 5-step automated flow
- GUI with progress tracking

## License

MIT License - Free to use and modify

## Acknowledgments

Built with Claude Code AI assistant
- Project architecture design
- Code implementation
- Documentation

## Support

For issues or questions, please open an issue on GitHub.

---

**AI Auto Installer v3.2** - Windows AI Development Environment Setup
