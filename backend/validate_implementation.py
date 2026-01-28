#!/usr/bin/env python3
"""
Validation script to verify the Todo Backend implementation
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
        ".prettierignore"
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


def validate_imports():
    """Validate that key modules can be imported without errors"""
    import_errors = []

    modules_to_test = [
        ("main", "app"),
        ("db", "engine"),
        ("models.task", "Task"),
        ("services.task_service", "TaskService"),
        ("auth.jwt_handler", "verify_token_and_get_user_id"),
        ("dependencies.auth", "CurrentUser"),
        ("utils.errors", "APIError"),
        ("config.settings", "settings"),
    ]

    # Add current directory to Python path temporarily
    sys.path.insert(0, ".")

    for module_path, attribute in modules_to_test:
        try:
            # Replace slashes with dots for import
            module_name = module_path.replace('/', '.').replace('\\', '.')
            module = __import__(module_name, fromlist=[attribute])

            # Check if the required attribute exists
            getattr(module, attribute)
        except ImportError as e:
            import_errors.append(f"backend.{module_path}: {e}")
        except AttributeError as e:
            import_errors.append(f"backend.{module_path}: Attribute {attribute} not found - {e}")

    if import_errors:
        print(f"[ERROR] Import errors: {import_errors}")
        return False

    print("[SUCCESS] All modules import successfully")
    return True


def validate_functionality():
    """Basic validation of functionality"""
    try:
        # Test that the main app can be imported and has expected routes
        import main
        app = main.app

        # Check that the expected routes are registered
        route_paths = [route.path for route in app.routes]

        expected_routes = [
            "/api/tasks",
            "/api/tasks/{task_id}",
            "/api/tasks/{task_id}/complete",
            "/"
        ]

        missing_routes = []
        for route in expected_routes:
            if route not in route_paths and f"/api{route}" not in route_paths:
                missing_routes.append(route)

        if missing_routes:
            print(f"[ERROR] Missing routes: {missing_routes}")
            return False

        print("[SUCCESS] All expected routes are registered")
        return True

    except Exception as e:
        print(f"[ERROR] Functionality validation failed: {e}")
        return False


def main():
    print("[INFO] Validating Todo Backend Implementation...")
    print()

    all_valid = True

    print("1. Validating directory structure...")
    all_valid &= validate_directory_structure()
    print()

    print("2. Validating required files...")
    all_valid &= validate_required_files()
    print()

    print("3. Validating imports...")
    all_valid &= validate_imports()
    print()

    print("4. Validating functionality...")
    all_valid &= validate_functionality()
    print()

    if all_valid:
        print("[SUCCESS] All validations passed! The Todo Backend implementation is complete and ready.")
        return 0
    else:
        print("[ERROR] Some validations failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())