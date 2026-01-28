"""
Script to check backend routes without loading full configuration
"""
import ast
import os
from pathlib import Path

# Temporarily set environment variables to avoid validation errors
os.environ['NEON_DATABASE_URL'] = 'postgresql+asyncpg://test:test@test:5432/test'
os.environ['BETTER_AUTH_SECRET'] = 'test_secret'

# Add backend to path
import sys
sys.path.insert(0, '.')

def extract_routes_from_file(filepath):
    """Extract route information from a Python file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    tree = ast.parse(content)

    routes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Look for route decorators
            if isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
                if func_name in ['get', 'post', 'put', 'delete', 'patch']:
                    # Look for path argument
                    for keyword in node.keywords:
                        if keyword.arg == 'path':
                            if isinstance(keyword.value, ast.Constant):
                                path = keyword.value.value
                            elif isinstance(keyword.value, ast.Str):  # For older Python versions
                                path = keyword.value.s
                            else:
                                continue

                            method = func_name.upper()
                            routes.append((method, path))

    return routes

# Check the tasks routes file
tasks_routes_file = Path('routes/tasks.py')
if tasks_routes_file.exists():
    print("Routes in routes/tasks.py:")
    routes = extract_routes_from_file(str(tasks_routes_file))
    for method, path in routes:
        print(f"  {method} {path}")

print("\nLooking for other route files...")
route_files = list(Path('routes').glob('*.py'))
for route_file in route_files:
    if route_file.name != '__init__.py':
        print(f"\nRoutes in {route_file}:")
        routes = extract_routes_from_file(str(route_file))
        for method, path in routes:
            print(f"  {method} {path}")

print("\nChecking main.py for included routers...")
with open('main.py', 'r') as f:
    main_content = f.read()
    if 'include_router' in main_content:
        print("Router inclusion found in main.py")
        # Look for prefixes
        import re
        prefixes = re.findall(r'prefix="([^"]*)"', main_content)
        for prefix in prefixes:
            print(f"  Router prefix: {prefix}")