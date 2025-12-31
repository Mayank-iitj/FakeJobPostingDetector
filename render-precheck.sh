#!/bin/bash

# Render Pre-Deployment Check Script
# Verifies your app is ready for Render deployment

echo "======================================================================"
echo "🚀 RENDER DEPLOYMENT PRE-CHECK"
echo "======================================================================"
echo ""

ALL_GOOD=true

# Check required files
echo "📁 CHECKING REQUIRED FILES:"
echo "----------------------------------------------------------------------"

REQUIRED_FILES=(
    "render.yaml"
    "requirements.txt"
    "runtime.txt"
    "api/main.py"
    "api/routes/phishing.py"
    "api/routes/malware.py"
    "api/routes/auth.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - MISSING"
        ALL_GOOD=false
    fi
done

echo ""

# Check optional files
echo "📄 CHECKING OPTIONAL FILES:"
echo "----------------------------------------------------------------------"

OPTIONAL_FILES=(
    ".env.render"
    ".gitignore"
    "RENDER_DEPLOY.md"
    "RENDER_ENV_SETUP.md"
)

for file in "${OPTIONAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "⚠️  $file"
    fi
done

echo ""

# Check Python version
echo "🐍 PYTHON VERSION:"
echo "----------------------------------------------------------------------"
if [ -f "runtime.txt" ]; then
    RUNTIME_VERSION=$(cat runtime.txt)
    echo "✅ Runtime: $RUNTIME_VERSION"
else
    echo "⚠️  runtime.txt not found"
fi

echo ""

# Check for large dependencies
echo "📦 CHECKING DEPENDENCIES:"
echo "----------------------------------------------------------------------"
if grep -q "torch" requirements.txt; then
    echo "✅ PyTorch found - Render handles this well"
fi
if grep -q "transformers" requirements.txt; then
    echo "✅ Transformers found - Render handles this well"
fi
if grep -q "fastapi" requirements.txt; then
    echo "✅ FastAPI found"
fi
if grep -q "uvicorn" requirements.txt; then
    echo "✅ Uvicorn found"
fi

echo ""

# Check render.yaml
echo "⚙️  CHECKING RENDER CONFIGURATION:"
echo "----------------------------------------------------------------------"
if [ -f "render.yaml" ]; then
    echo "✅ render.yaml found"
    if grep -q "buildCommand" render.yaml; then
        echo "✅ Build command configured"
    fi
    if grep -q "startCommand" render.yaml; then
        echo "✅ Start command configured"
    fi
    if grep -q "SECRET_KEY" render.yaml; then
        echo "✅ SECRET_KEY configured in render.yaml"
    fi
else
    echo "⚠️  render.yaml not found - will need manual configuration"
fi

echo ""

# Final summary
echo "======================================================================"
if [ "$ALL_GOOD" = true ]; then
    echo "✅ ALL CRITICAL CHECKS PASSED!"
    echo ""
    echo "🚀 READY TO DEPLOY TO RENDER!"
    echo ""
    echo "Next Steps:"
    echo "1. Push code to GitHub"
    echo "2. Go to render.com and sign up/login"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Connect your GitHub repository"
    echo "5. Deploy!"
    echo ""
    echo "📖 Read RENDER_DEPLOY.md for detailed instructions"
else
    echo "❌ SOME CHECKS FAILED"
    echo "Fix missing required files before deploying"
    exit 1
fi
echo "======================================================================"

exit 0
