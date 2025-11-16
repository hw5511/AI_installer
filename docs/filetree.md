# AI Setup Tool - Project Structure

**Simple AI Setup Tool v3.1** - Brain Module System v4.0

## Project Overview
- **Total Files**: 62 Python files
- **Total Lines**: 8,636 lines
- **Average File Size**: 139 lines
- **Modular Architecture**: 11 sub-modules with Facade pattern

## Project Structure

```
new_ai_setup/
├── auto_main.py              # Main entry point (186)
├── build_auto.py             # PyInstaller build script (115)
├── README.md
├── icon.ico
├── manifest.xml
│
├── auto_main/                # Auto-installation system (1,163)
│   ├── auto_gui.py           # GUI controller - Facade pattern (114)
│   ├── auto_installer.py     # Installation orchestrator (148)
│   ├── gui_modules/          # GUI sub-modules (518)
│   │   ├── gui_widgets.py    # Widget factory (240)
│   │   ├── gui_logger.py     # Log manager (98)
│   │   └── gui_installer_bridge.py  # Bridge pattern (170)
│   └── installer_modules/    # Installation executor (376)
│       └── installation_step_executor.py  # 5-step installer (368)
│
└── modules/                  # Brain Module System v4.0 (6,898)
    │
    ├── core/                 # Core business logic (3,176)
    │   ├── config.py         # Config Facade (151)
    │   ├── installer.py      # Installer Facade (160)
    │   ├── status_checker.py # Status verification (292)
    │   ├── exceptions.py     # Custom exceptions (34)
    │   │
    │   ├── config_modules/   # Config sub-modules (433)
    │   │   ├── config_constants.py   # System constants (149)
    │   │   ├── config_commands.py    # Command definitions (111)
    │   │   ├── config_ui.py          # UI settings (45)
    │   │   └── config_messages.py    # Message templates (64)
    │   │
    │   ├── installer_components/     # Installer components (953)
    │   │   ├── package_manager_detector.py  # PM detection (210)
    │   │   ├── software_installer.py        # Software installation (182)
    │   │   ├── installation_verifier.py     # Installation verification (161)
    │   │   └── tool_installer.py            # Tool-specific installers (384)
    │   │
    │   └── checker_modules/          # Checker components (1,123)
    │       ├── checker_utils.py      # Common utilities (58)
    │       ├── tool_checkers.py      # Git/Node checkers (262)
    │       ├── cli_checkers.py       # Claude/Gemini checkers (472)
    │       └── system_explorer.py    # System exploration (310)
    │
    ├── ui/                   # User interface (520)
    │   ├── components.py     # UI Components Facade (61)
    │   ├── themes.py         # Color system (43)
    │   └── component_modules/  # UI sub-modules (390)
    │       ├── status_components.py   # Status display (59)
    │       ├── button_components.py   # Button components (70)
    │       ├── display_components.py  # Display components (67)
    │       ├── layout_components.py   # Layout components (84)
    │       └── ui_builder.py          # UI Builder pattern (110)
    │
    └── utils/                # Utilities (3,365)
        ├── logger.py         # Logging system (123)
        ├── error_logger.py   # Error logging (174)
        ├── path_manager.py   # PATH Manager Facade (107)
        ├── path_repair.py    # PATH Repair Facade (37)
        ├── path_verifier.py  # PATH Verifier Facade (251)
        ├── system_utils.py   # System utilities (277)
        ├── vscode_settings_manager.py  # VSCode settings auto-fix (163)
        │
        ├── path_operations/  # PATH operations (1,188)
        │   ├── registry_operations.py    # Registry access (278)
        │   ├── broadcast_manager.py      # ENV broadcast (211)
        │   ├── powershell_integration.py # PowerShell exec (295)
        │   └── path_operations.py        # High-level API (387)
        │
        ├── verifier_components/  # Verification (514)
        │   ├── registry_checker.py   # Registry checker (161)
        │   ├── tool_executor.py      # Tool executor (124)
        │   └── verification_ui.py    # Verification UI (219)
        │
        └── repair_components/    # PATH repair (483)
            ├── path_discovery.py     # Path discovery (135)
            ├── path_registry.py      # Registry reader (65)
            └── path_repair_core.py   # Repair orchestrator (268)
```

## Code Statistics

### Module Breakdown

| Module | Files | Lines | Avg | Description |
|--------|-------|-------|-----|-------------|
| **Root** | 2 | 301 | 151 | Entry point & build script |
| **auto_main/** | 7 | 1,163 | 166 | Auto-installation system |
| **core/** | 20 | 3,176 | 159 | Core business logic |
| **ui/** | 8 | 520 | 65 | User interface |
| **utils/** | 24 | 3,365 | 140 | Utility functions |
| **scripts/** | 1 | 111 | 111 | Development tools |
| **Total** | **62** | **8,636** | **139** | Complete project |

### Modularization Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Large files (300+ lines)** | 9 | 0 | ✅ -100% |
| **Average file size** | ~300 | ~139 | ✅ -54% |
| **Sub-module directories** | 0 | 11 | ✅ Clear hierarchy |
| **Facade patterns** | 0 | 9 | ✅ Consistent API |
| **Total lines** | 6,387 | 8,636 | +35% (structure overhead) |

## Architecture

### Design Patterns Applied

- **Facade Pattern** (9): config.py, installer.py, status_checker.py, path_manager.py, path_repair.py, path_verifier.py, components.py, auto_gui.py, auto_installer.py
- **Builder Pattern**: ui_builder.py, component builders
- **Strategy Pattern**: installation_step_executor.py, checker modules
- **Bridge Pattern**: gui_installer_bridge.py
- **Factory Pattern**: gui_widgets.py

### Core Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Injection**: Loose coupling between components
3. **Configuration-Based**: Centralized config management
4. **Modular Structure**: Independent, extensible components
5. **Consistent Interface**: Facade pattern for complex subsystems

## Key Features

### Auto-Installation System (auto_main/)
- **5-step automated flow**: Chocolatey → Git → Node.js → Claude/Gemini CLI
- **GUI controller**: Orchestrates widget assembly and module communication
- **Installation executor**: Manages installation steps with progress tracking
- **Bridge pattern**: Connects GUI and installer logic

### Core Modules (modules/core/)
- **Config system**: Centralized settings with sub-modules for constants, commands, UI, messages
- **Installer system**: Package manager detection, software installation, verification
- **Checker system**: Tool detection (Git, Node, Claude, Gemini), system exploration
- **Facade pattern**: Simplified interfaces for complex subsystems

### UI System (modules/ui/)
- **Component-based**: Status, button, display, layout components
- **Builder pattern**: UI assembly with clear separation
- **Theme system**: Centralized color management

### Utility System (modules/utils/)
- **PATH management**: Registry operations, broadcast, PowerShell integration
- **Verification**: Registry checker, tool executor, verification UI
- **Repair system**: Path discovery, repair orchestration
- **Logging**: Separate systems for general and error logging
- **VSCode integration**: Automatic terminal PATH optimization

## Build System

**PyInstaller automation** via `build_auto.py`:
- Bundles all modules (auto_main + modules)
- Includes icon.ico and manifest.xml
- Output: `AI_Auto_Installer.exe` (11MB)
- Production mode: Hidden PowerShell windows

## Development Guidelines

### File Creation Rules
- ✅ New .py files in module directories
- ✅ Extensions in auto_main/ directory
- ✅ Components in sub-modules
- ❌ Temporary files in root
- ❌ Emoji in code (encoding issues)

### Coding Standards
- **Encoding**: UTF-8, English comments
- **Style**: PEP 8 compliance
- **Type hints**: typing module
- **Docstrings**: All functions and classes
- **Error handling**: Custom exception classes
- **Logging**: logger.py and error_logger.py
- **PATH management**: path_manager.py unified API

### Extension Methods
1. **Add installation step**: Edit installation_step_executor.py
2. **Add new software**: Edit tool_installer.py
3. **Improve UI**: Add component to component_modules/
4. **Extend PATH**: Expand path_operations/ sub-module
5. **Add utility**: Create new module in utils/

### Modularization Maintenance
- **Max lines**: Keep files under 320 lines
- **Single responsibility**: One clear role per module
- **Facade usage**: External interfaces use Facade pattern
- **Backward compatibility**: Maintain existing import paths

## Version History

### v3.2 (Current) - VSCode Terminal Auto-Fix
- 🆕 VSCode terminal PATH automatic optimization
- 🆕 vscode_settings_manager.py utility module
- ✅ Silent auto-fix for terminal.integrated.env.windows
- ✅ No user interaction required
- ✅ 62 files, 8,636 lines total

### v3.1 - Complete Modularization
- ✅ Full modularization: Phase 1, 2, 3 complete
- ✅ 11 sub-modules with clear hierarchy
- ✅ 9 Facade patterns for consistent interfaces
- ✅ 61 files with 139-line average (high maintainability)
- ✅ Zero large files (300+ lines)
- ✅ SOLID principles: SRP, DI, Facade pattern

### v3.0 - Auto-Installation System
- Auto-installation with 5-step flow
- auto_main package (968 lines)
- Thread-based async processing
- Log saving functionality

### v2.8 - Korean Localization
- Complete Korean UI (383+ texts)
- Production build with hidden PowerShell
- 10.26MB optimized build

---

**Simple AI Setup Tool v3.2** - Brain Module System v4.0
Last Updated: 2025-11-17 (VSCode Terminal Auto-Fix)
