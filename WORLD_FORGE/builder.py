"""
LUMEN HUB — THE BUILDER
CI/CD Pipeline: detects project type, creates isolated env, installs deps.
"""
import os
import subprocess
import sys
from pathlib import Path

APPS_DIR = Path("E:/LUMEN_HUB/BRANCHES")
REPOS_DIR = Path("E:/LUMEN_HUB/repos")


def detect_project_type(project_path: Path) -> str:
    if (project_path / "requirements.txt").exists() or (project_path / "pyproject.toml").exists():
        return "python"
    if (project_path / "package.json").exists():
        return "node"
    if (project_path / "go.mod").exists():
        return "go"
    return "unknown"


def build_python(project_path: Path, app_dir: Path) -> bool:
    print(f"[BUILDER] Python project detected: {project_path.name}")
    venv_dir = app_dir / "venv"

    print("[BUILDER] Creating virtual environment...")
    result = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], capture_output=True)
    if result.returncode != 0:
        print(f"[BUILDER] ERROR: venv creation failed\n{result.stderr.decode()}")
        return False

    pip = venv_dir / "Scripts" / "pip.exe" if sys.platform == "win32" else venv_dir / "bin" / "pip"

    req_file = project_path / "requirements.txt"
    if req_file.exists():
        print("[BUILDER] Installing requirements...")
        result = subprocess.run([str(pip), "install", "-r", str(req_file)], capture_output=True)
        if result.returncode != 0:
            print(f"[BUILDER] ERROR: pip install failed\n{result.stderr.decode()}")
            return False

    # Generate Procfile if missing
    procfile = app_dir / "Procfile"
    if not (project_path / "Procfile").exists():
        # Try to find main entry point
        for candidate in ["main.py", "app.py", "server.py", "api_server.py"]:
            if (project_path / candidate).exists():
                python_bin = venv_dir / "Scripts" / "python.exe" if sys.platform == "win32" else venv_dir / "bin" / "python"
                procfile.write_text(f"web: {python_bin} {project_path / candidate}\n")
                print(f"[BUILDER] Generated Procfile → web: python {candidate}")
                break
    else:
        import shutil
        shutil.copy(project_path / "Procfile", procfile)

    return True


def build_node(project_path: Path, app_dir: Path) -> bool:
    print(f"[BUILDER] Node project detected: {project_path.name}")
    print("[BUILDER] Installing npm dependencies...")
    result = subprocess.run(["npm", "install", "--prefix", str(project_path)], capture_output=True)
    if result.returncode != 0:
        print(f"[BUILDER] ERROR: npm install failed\n{result.stderr.decode()}")
        return False

    procfile = app_dir / "Procfile"
    if not procfile.exists():
        procfile.write_text(f"web: node {project_path / 'index.js'}\n")
        print("[BUILDER] Generated Procfile → web: node index.js")

    return True


def build(app_name: str) -> bool:
    """Main entry point. Build app from repos/ into apps/."""
    repo_path = REPOS_DIR / app_name
    app_dir = APPS_DIR / app_name

    if not repo_path.exists():
        print(f"[BUILDER] ERROR: repo '{app_name}' not found in {REPOS_DIR}")
        return False

    app_dir.mkdir(parents=True, exist_ok=True)

    project_type = detect_project_type(repo_path)

    if project_type == "python":
        success = build_python(repo_path, app_dir)
    elif project_type == "node":
        success = build_node(repo_path, app_dir)
    else:
        print(f"[BUILDER] WARNING: Unknown project type. Skipping dependency install.")
        success = True

    if success:
        # Write build metadata
        import json
        from datetime import datetime
        meta = {"app": app_name, "type": project_type, "built_at": datetime.now().isoformat()}
        (app_dir / "build.json").write_text(json.dumps(meta, indent=2))
        print(f"[BUILDER] ✅ Build complete: {app_name} ({project_type})")

    return success


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python builder.py <app_name>")
    else:
        build(sys.argv[1])
