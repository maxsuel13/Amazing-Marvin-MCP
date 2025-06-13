#!/usr/bin/env python3
"""Release script for Amazing Marvin MCP."""

import re
import subprocess
import sys
from pathlib import Path
from typing import Literal


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()

    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")

    return match.group(1)


def bump_version(current: str, bump_type: Literal["patch", "minor", "major"]) -> str:
    """Bump version according to semver."""
    major, minor, patch = map(int, current.split("."))

    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0

    return f"{major}.{minor}.{patch}"


def update_version_in_pyproject(new_version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()

    new_content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)

    pyproject_path.write_text(new_content)
    print(f"✅ Updated pyproject.toml to version {new_version}")


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"🔧 Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check)


def main():
    """Main release function."""
    if len(sys.argv) != 2 or sys.argv[1] not in ["patch", "minor", "major"]:
        print("Usage: python scripts/release.py [patch|minor|major]")
        sys.exit(1)

    bump_type = sys.argv[1]

    # Get current version
    current_version = get_current_version()
    new_version = bump_version(current_version, bump_type)

    print(f"🚀 Releasing {current_version} → {new_version} ({bump_type} bump)")

    # Run checks first
    print("\n📋 Running pre-release checks...")
    run_command(["ruff", "check", "src/"])
    run_command(["mypy", "src/amazing_marvin_mcp/"])
    run_command(["pytest", "tests/", "-x"])

    # Update version
    update_version_in_pyproject(new_version)

    # Git operations
    print("\n📝 Creating git commit and tag...")
    run_command(["git", "add", "pyproject.toml"])
    run_command(["git", "commit", "-m", f"Release v{new_version}"])
    run_command(["git", "tag", f"v{new_version}"])

    print(f"\n✅ Release v{new_version} ready!")
    print("\nNext steps:")
    print("1. Review the changes:")
    print("   git show HEAD")
    print("2. Push to trigger CI and PyPI publish:")
    print("   git push origin main")
    print(f"   git push origin v{new_version}")
    print("\n🚀 This will automatically:")
    print("   - Run tests on multiple Python versions")
    print("   - Publish to PyPI")


if __name__ == "__main__":
    main()
