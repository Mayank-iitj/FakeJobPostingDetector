"""
Quick Test Runner - Run all tests and generate reports
"""

import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run all tests with coverage"""
    print("🧪 Running Test Suite\n")
    print("=" * 60)
    
    # Run pytest
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--cov=.",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-report=xml"
        ],
        cwd=Path(__file__).parent
    )
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("📊 Coverage report: htmlcov/index.html")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Some tests failed")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
