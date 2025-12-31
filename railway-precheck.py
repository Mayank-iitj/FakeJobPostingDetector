"""
Railway Deployment Pre-Check Script
Verifies that your application is ready for Railway deployment
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    exists = Path(filepath).exists()
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "REQUIRED" if required else "OPTIONAL"
    print(f"{status} {filepath} - {req_text}")
    return exists

def check_env_variable(var_name, sample_value=None):
    """Check environment variable"""
    value = os.getenv(var_name)
    has_value = value is not None and value != ""
    status = "✅" if has_value else "⚠️"
    
    if has_value:
        # Mask sensitive values
        if "KEY" in var_name or "SECRET" in var_name:
            display = f"{value[:8]}...{value[-8:]}" if len(value) > 16 else "***"
        else:
            display = value[:50] + "..." if len(value) > 50 else value
        print(f"{status} {var_name} = {display}")
    else:
        print(f"{status} {var_name} - Not set (will use Railway variables)")
        if sample_value:
            print(f"    💡 Recommended: {sample_value}")
    
    return has_value

def main():
    """Run all deployment checks"""
    print("=" * 70)
    print("🚀 RAILWAY DEPLOYMENT PRE-CHECK")
    print("=" * 70)
    print()
    
    all_good = True
    
    # Check required files
    print("📁 CHECKING REQUIRED FILES:")
    print("-" * 70)
    required_files = [
        "railway.json",
        "nixpacks.toml",
        "requirements.txt",
        "runtime.txt",
        "api/main.py",
        "api/routes/phishing.py",
        "api/routes/malware.py",
        "api/routes/auth.py",
    ]
    
    for filepath in required_files:
        if not check_file_exists(filepath, required=True):
            all_good = False
    
    print()
    
    # Check optional files
    print("📄 CHECKING OPTIONAL FILES:")
    print("-" * 70)
    optional_files = [
        ".env.railway",
        ".railwayignore",
        ".gitignore",
        "RAILWAY_ENV_SETUP.md",
    ]
    
    for filepath in optional_files:
        check_file_exists(filepath, required=False)
    
    print()
    
    # Check environment variables (local - not required, just informational)
    print("🔧 ENVIRONMENT VARIABLES (will be set in Railway):")
    print("-" * 70)
    check_env_variable("SECRET_KEY", "wf-gMr8kevo-Dyumh0b2p8VD5q0xt_rXSxfLbvL-XwU")
    check_env_variable("ALLOWED_ORIGINS", "*")
    check_env_variable("WORKERS", "4")
    check_env_variable("LOG_LEVEL", "info")
    
    print()
    
    # Check Python version
    print("🐍 PYTHON VERSION:")
    print("-" * 70)
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✅ Current: Python {python_version}")
    
    # Check runtime.txt
    try:
        with open("runtime.txt", "r") as f:
            runtime_version = f.read().strip()
            print(f"✅ Runtime: {runtime_version}")
    except:
        print("⚠️  runtime.txt not found")
    
    print()
    
    # Check model files (optional, expected to be missing)
    print("🤖 ML MODEL FILES (Optional - App works without them):")
    print("-" * 70)
    model_files = [
        "./models/checkpoints/phishing_vit_best.ckpt",
        "./models/checkpoints/malware_ensemble_best.ckpt",
    ]
    
    models_found = False
    for model_path in model_files:
        if check_file_exists(model_path, required=False):
            models_found = True
    
    if not models_found:
        print("💡 No models found - App will run in DEMO MODE with mock predictions")
        print("   This is EXPECTED and the API will work perfectly for testing!")
    
    print()
    
    # Final summary
    print("=" * 70)
    if all_good:
        print("✅ ALL CRITICAL CHECKS PASSED!")
        print()
        print("🚀 NEXT STEPS:")
        print("1. Push code to GitHub")
        print("2. Create Railway project from GitHub repo")
        print("3. Add environment variables (see RAILWAY_ENV_SETUP.md)")
        print("4. Deploy!")
        print()
        print("📖 Read RAILWAY_ENV_SETUP.md for detailed deployment instructions")
    else:
        print("❌ SOME CHECKS FAILED - Fix required files before deploying")
        return 1
    
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
