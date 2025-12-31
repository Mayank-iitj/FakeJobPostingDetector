"""
Railway Deployment Test Script
Tests if the application is correctly configured for Railway
"""

import os
import sys
from pathlib import Path


def test_file_exists(filepath, description):
    """Test if required file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False


def test_procfile():
    """Test Procfile exists and is valid"""
    if not test_file_exists("Procfile", "Procfile"):
        return False
    
    with open("Procfile", "r") as f:
        content = f.read()
        if "uvicorn" in content and "$PORT" in content:
            print("   ✓ Procfile contains correct start command")
            return True
        else:
            print("   ✗ Procfile missing uvicorn or $PORT")
            return False


def test_requirements():
    """Test requirements.txt exists"""
    if not test_file_exists("requirements.txt", "Requirements file"):
        return False
    
    with open("requirements.txt", "r") as f:
        content = f.read()
        required = ["fastapi", "uvicorn", "pytorch"]
        missing = [pkg for pkg in required if pkg not in content.lower()]
        
        if not missing:
            print("   ✓ All key dependencies present")
            return True
        else:
            print(f"   ✗ Missing dependencies: {missing}")
            return False


def test_railway_config():
    """Test Railway configuration files"""
    return test_file_exists("railway.json", "Railway config")


def test_api_main():
    """Test API main file exists"""
    return test_file_exists("api/main.py", "API entry point")


def test_environment():
    """Test environment configuration"""
    return test_file_exists(".env.railway", "Railway env template")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Railway Deployment Configuration Test")
    print("="*60 + "\n")
    
    tests = [
        ("Procfile Configuration", test_procfile),
        ("Requirements File", test_requirements),
        ("Railway Config", test_railway_config),
        ("API Entry Point", test_api_main),
        ("Environment Template", test_environment),
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"\n{name}:")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ready for Railway deployment.")
        print("\nNext steps:")
        print("1. Run: railway-up.bat (Windows) or ./railway-up.sh (Linux/Mac)")
        print("2. Set environment variables in Railway dashboard")
        print("3. Test deployment: railway open")
        return 0
    else:
        print("\n⚠️ Some tests failed. Fix issues before deploying.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
