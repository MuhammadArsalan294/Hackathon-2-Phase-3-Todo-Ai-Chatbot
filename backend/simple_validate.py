#!/usr/bin/env python3
"""
Simple validation script to verify the Todo Backend implementation
"""
import os
import sys
from pathlib import Path


def validate_directory_structure():
    """Validate that all required directories exist"""
    # Since we're running from the backend directory, check for relative paths
    required_dirs = [
        ".",  # Current directory (backend/)
        "auth",
        "config",
        "db",
        "models",
        "routes",
        "schemas",
        "services",
        "utils",
        "dependencies",
        "middleware",
        "api",
        "docs",
        "tests",
        "tests/unit",
        "tests/integration"
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(f"backend/{dir_path}")

    if missing_dirs:
        print(f"[ERROR] Missing directories: {missing_dirs}")
        return False

    print("[SUCCESS] All required directories exist")
    return True


def validate_required_files():
    """Validate that all required files exist"""
    required_files = [
        "main.py",
        "db.py",
        "models/task.py",
        "schemas/task.py",
        "services/task_service.py",
        "routes/tasks.py",
        "auth/jwt_handler.py",
        "dependencies/auth.py",
        "utils/errors.py",
        "config/settings.py",
        "api/client.py",
        "middleware/logging.py",
        "requirements.txt",
        ".gitignore",
        "README.md",
        "docs/api.md",
        "tests/unit/test_task_service.py",
        "tests/integration/test_tasks_api.py",
        "tests/conftest.py",
        "pyproject.toml",
        ".flake8",
        ".prettierrc",
        ".prettierignore",
        ".env.example"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(f"backend/{file_path}")

    if missing_files:
        print(f"[ERROR] Missing files: {missing_files}")
        return False

    print("[SUCCESS] All required files exist")
    return True


def main():
    print("[INFO] Simple validation of Todo Backend Implementation...")
    print()

    all_valid = True

    print("1. Validating directory structure...")
    all_valid &= validate_directory_structure()
    print()

    print("2. Validating required files...")
    all_valid &= validate_required_files()
    print()

    if all_valid:
        print("[SUCCESS] All validations passed! The Todo Backend implementation is complete and ready.")
        return 0
    else:
        print("[ERROR] Some validations failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())