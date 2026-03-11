"""
TEST INFRASTRUCTURE
Checks if the LUMEN HUB environment is correctly scaffolded.
"""
import os
import pytest

REQUIRED_DIRS = [
    "repos",
    "orchestrator",
    "apps",
    "data",
    "docs",
    "scripts"
]

def test_directories_exist():
    """Verify core directories are present."""
    base_path = r"E:\LUMEN_HUB"
    for d in REQUIRED_DIRS:
        path = os.path.join(base_path, d)
        assert os.path.exists(path), f"CRITICAL: Directory missing: {d}"

def test_readme_exists_and_valid():
    """Verify README contains the project manifesto."""
    readme_path = r"E:\LUMEN_HUB\README.md"
    assert os.path.exists(readme_path), "README.md is missing"
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "LUMEN ORCHESTRATOR" in content, "README missing correct title"
        assert "SHAD" in content, "README missing Operator name"

def test_write_permissions():
    """Verify we can write to the data directory."""
    test_file = r"E:\LUMEN_HUB\data\write_test.tmp"
    try:
        with open(test_file, "w") as f:
            f.write("test")
        assert os.path.exists(test_file)
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
