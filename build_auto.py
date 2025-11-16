#!/usr/bin/env python3
"""
Build script for AI Auto Installer
Creates a single executable file from auto_main.py

Usage:
    python build_auto.py

Output:
    dist_auto/AI_Auto_Installer.exe

This script is specifically for building the AUTO installer,
different from build.py which builds the main AI Setup Tool.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def clean_previous_builds():
    """Remove previous build artifacts"""
    dirs_to_remove = ['build_auto', 'dist_auto']

    for dir_name in dirs_to_remove:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"Removing {dir_name}...")
            shutil.rmtree(dir_path, ignore_errors=True)

    # Remove any auto-related spec files
    for spec_file in Path('.').glob('*Auto*.spec'):
        print(f"Removing {spec_file}...")
        spec_file.unlink()


def build_auto_installer():
    """Build the AI Auto Installer executable"""
    print("=" * 60)
    print("AI Auto Installer Build Script")
    print("=" * 60)
    print("This builds the AUTO version (auto_main.py)")
    print("For main setup tool, use build.py instead")
    print("-" * 60)

    # Clean previous builds
    print("\nCleaning previous builds...")
    clean_previous_builds()

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Single executable file
        "--windowed",          # No console window
        "--uac-admin",         # Request admin privileges (adds shield icon)
        "--icon", "icon.ico",  # Icon file (required for --uac-admin to work!)
        "--name", "AI_Auto_Installer",
        "--manifest", "manifest.xml",  # Administrator privileges manifest
        "--distpath", "dist_auto",
        "--workpath", "build_auto",
        "--clean",
        "--noconfirm",
        "auto_main.py"
    ]

    print("\nExecuting PyInstaller...")
    print("Command: " + " ".join(cmd))
    print("-" * 60)

    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=False, text=True)

    print("-" * 60)

    if result.returncode == 0:
        # Check if exe was created
        exe_path = Path("dist_auto/AI_Auto_Installer.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print("\n[SUCCESS] Build completed successfully!")
            print(f"Output: {exe_path}")
            print(f"Size: {size_mb:.2f} MB")
            print("\nYou can now run: dist_auto\\AI_Auto_Installer.exe")
            return 0
        else:
            print("\n[ERROR] Build failed - executable not found")
            return 1
    else:
        print(f"\n[ERROR] Build failed with exit code: {result.returncode}")
        return 1


def main():
    """Main entry point"""
    # Change to project directory
    os.chdir(Path(__file__).parent)

    print(f"Working directory: {os.getcwd()}\n")

    # Check PyInstaller
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("[ERROR] PyInstaller is not installed")
        print("Install it using: pip install pyinstaller")
        return 1

    # Build
    return build_auto_installer()


if __name__ == "__main__":
    sys.exit(main())