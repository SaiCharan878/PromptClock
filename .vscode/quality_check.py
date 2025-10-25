import subprocess
import sys
import pathlib

print("🧹 Running code quality checks...\n")

# Use the current venv's Python executable explicitly
python_exe = sys.executable
root = pathlib.Path(__file__).resolve().parents[1]


def run_tool(module: str, *args: str) -> None:
    """Run a Python module within the same venv."""
    print(f"▶ Running: {module} {' '.join(args)}")
    subprocess.run([python_exe, "-m", module, *args], cwd=root, check=True)


try:
    run_tool("black", ".")
    run_tool("ruff", "check", ".")
    run_tool("mypy", "promptclock")
    print("\n✅ All quality checks completed successfully!")
except subprocess.CalledProcessError as e:
    print(f"\n❌ A quality check failed with exit code {e.returncode}")
    sys.exit(e.returncode)
