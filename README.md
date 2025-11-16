# AI Auto Installer

Windows AI development environment one-click setup tool.

## What It Does

Automatically installs:
- Git
- Node.js & npm
- Claude Code CLI
- Google Gemini CLI
- VSCode terminal PATH optimization

## Usage

1. Download `AI_Auto_Installer.exe`
2. Run as administrator
3. Wait for completion
4. Restart VSCode
5. Done!

## Build from Source

```bash
git clone https://github.com/hw5511/AI_installer.git
cd AI_installer
pip install pyinstaller pywin32
python build_auto.py
```

Output: `dist_auto/AI_Auto_Installer.exe` (10MB)

## Requirements

- Windows 10/11
- Administrator privileges
- Internet connection

## Features

- Automatic PATH management
- VSCode terminal integration
- No manual configuration
- Korean UI support

## Technical Details

- 62 Python files, 8,636 lines
- Brain Module System v4.0
- Modular architecture with Facade pattern

## License

MIT License

## Built With

Claude Code AI Assistant

---

**AI Auto Installer v3.2**
