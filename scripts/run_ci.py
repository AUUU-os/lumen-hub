"""
LUMEN CI/CD RUNNER
Automates testing and reporting.
"""
import os
import sys
import subprocess
from datetime import datetime

def run_tests():
    print("🐺 CI: Starting Test Suite...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Use raw strings to avoid escape sequence issues like \t
    base_dir = r"E:\LUMEN_HUB"
    tests_dir = os.path.join(base_dir, "tests")
    docs_dir = os.path.join(base_dir, "docs")
    report_file = os.path.join(docs_dir, f"test_report_{timestamp}.html")
    
    # Run Pytest with HTML report
    # We use list format for subprocess to avoid shell interpretation issues
    cmd = [
        sys.executable, 
        "-m", "pytest", 
        tests_dir, 
        f"--html={report_file}", 
        "--self-contained-html"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED.")
    else:
        print("❌ TESTS FAILED or No items found.")
        print(result.stderr)
        
    print(f"📄 Report generated: {report_file}")
    return report_file

if __name__ == "__main__":
    run_tests()