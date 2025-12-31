#!/usr/bin/env python3
"""
Comprehensive Installation and Setup Script
Threat Intelligence Platform
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import platform


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def run_command(cmd, description, check=True):
    """Run shell command with description"""
    print(f"\n{Colors.BOLD}📌 {description}{Colors.END}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(description)
            return True
        else:
            if check:
                print_error(f"{description} failed")
                print(result.stderr)
                return False
            return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed: {e}")
        return False


def check_python_version():
    """Check if Python version is >= 3.10"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Detected: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print_success("Python version is compatible")
        return True
    else:
        print_error("Python 3.10+ required")
        return False


def create_virtual_environment():
    """Create Python virtual environment"""
    print_header("Creating Virtual Environment")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print_warning("Virtual environment already exists")
        return True
    
    return run_command(
        f"{sys.executable} -m venv venv",
        "Creating virtual environment"
    )


def get_pip_path():
    """Get pip executable path based on OS"""
    if platform.system() == "Windows":
        return str(Path("venv") / "Scripts" / "pip")
    else:
        return str(Path("venv") / "bin" / "pip")


def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    pip_path = get_pip_path()
    
    # Upgrade pip
    if not run_command(
        f"{pip_path} install --upgrade pip",
        "Upgrading pip"
    ):
        return False
    
    # Install requirements
    if not run_command(
        f"{pip_path} install -r requirements.txt",
        "Installing project dependencies (this may take a few minutes)"
    ):
        return False
    
    return True


def create_env_file():
    """Create .env from template"""
    print_header("Configuring Environment")
    
    env_path = Path(".env")
    env_example = Path(".env.example")
    
    if env_path.exists():
        print_warning(".env file already exists")
        return True
    
    if not env_example.exists():
        print_error(".env.example not found")
        return False
    
    shutil.copy(env_example, env_path)
    print_success("Created .env file")
    print_warning("⚠️  Please edit .env with your configuration before starting services")
    
    return True


def create_directories():
    """Create necessary directories"""
    print_header("Creating Project Directories")
    
    directories = [
        "data/phishing",
        "data/malware",
        "data/screenshots",
        "models/checkpoints",
        "logs",
        "mlruns"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print_success(f"Created {len(directories)} directories")
    return True


def check_docker():
    """Check if Docker is installed"""
    print_header("Checking Docker")
    
    result = subprocess.run(
        "docker --version",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success(f"Docker detected: {result.stdout.strip()}")
        
        # Check docker-compose
        result = subprocess.run(
            "docker-compose --version",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"Docker Compose detected: {result.stdout.strip()}")
        else:
            print_warning("Docker Compose not found (optional)")
        
        return True
    else:
        print_warning("Docker not installed (optional for local development)")
        return True


def run_tests():
    """Run test suite"""
    print_header("Running Tests")
    
    python_path = sys.executable if Path("venv").exists() else "python"
    
    result = subprocess.run(
        f"{python_path} -m pytest tests/ -v --tb=short",
        shell=True,
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.returncode == 0:
        print_success("All tests passed")
        return True
    else:
        print_warning("Some tests failed (this is OK for initial setup)")
        return True


def print_next_steps():
    """Print next steps for user"""
    print_header("Setup Complete!")
    
    is_windows = platform.system() == "Windows"
    activate_cmd = "venv\\Scripts\\activate" if is_windows else "source venv/bin/activate"
    
    print(f"""
{Colors.BOLD}Next Steps:{Colors.END}

1️⃣  {Colors.BOLD}Activate virtual environment:{Colors.END}
   {Colors.YELLOW}{activate_cmd}{Colors.END}

2️⃣  {Colors.BOLD}Edit configuration:{Colors.END}
   Open .env and update with your API keys

3️⃣  {Colors.BOLD}Start the API:{Colors.END}
   {Colors.YELLOW}python -m api.main{Colors.END}

4️⃣  {Colors.BOLD}Access the platform:{Colors.END}
   📚 API Docs:        http://localhost:8000/docs
   🎨 Gradio UI:       http://localhost:7860
   📊 Dashboard:       http://localhost:8501

5️⃣  {Colors.BOLD}Run with Docker (optional):{Colors.END}
   {Colors.YELLOW}cd docker{Colors.END}
   {Colors.YELLOW}docker-compose up -d{Colors.END}

6️⃣  {Colors.BOLD}Deploy to production:{Colors.END}
   {Colors.YELLOW}./deploy_railway.bat{Colors.END}  (Windows)
   {Colors.YELLOW}./deploy_railway.sh{Colors.END}   (Linux/Mac)

{Colors.BOLD}📖 Documentation:{Colors.END}
   README.md          - Project overview
   API.md             - API documentation
   DEPLOYMENT.md      - Deployment guide

{Colors.BOLD}🧪 Testing:{Colors.END}
   {Colors.YELLOW}python run_tests.py{Colors.END}

{Colors.BOLD}🎓 Demo Credentials:{Colors.END}
   Username: demo
   Password: demopassword

{Colors.GREEN}Happy coding! 🚀{Colors.END}
    """)


def main():
    """Main installation workflow"""
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔══════════════════════════════════════════════════════════╗
║  🛡️  Threat Intelligence Platform - Setup Script  🛡️   ║
║  Enterprise-Grade Cybersecurity ML System               ║
╚══════════════════════════════════════════════════════════╝
{Colors.END}
    """)
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Step 3: Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Step 4: Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Step 5: Create directories
    if not create_directories():
        sys.exit(1)
    
    # Step 6: Check Docker (optional)
    check_docker()
    
    # Step 7: Run tests (optional)
    print("\n")
    user_input = input("Run tests now? (y/N): ").strip().lower()
    if user_input == 'y':
        run_tests()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Setup failed: {e}{Colors.END}")
        sys.exit(1)
