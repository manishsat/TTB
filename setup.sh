#!/bin/bash

# TTB Label Verification System - Local Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "=================================="
echo "TTB Label Verification System"
echo "Local Development Setup"
echo "=================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check prerequisites
echo "Checking prerequisites..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi
NODE_VERSION=$(node --version)
print_success "Node.js $NODE_VERSION found"

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi
NPM_VERSION=$(npm --version)
print_success "npm $NPM_VERSION found"

echo ""
echo "=================================="
echo "Setting up Backend"
echo "=================================="
echo ""

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# Install dependencies
print_info "Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
print_success "Python dependencies installed"

# Setup environment variables
if [ ! -f ".env" ]; then
    print_info "Creating backend .env file..."
    cat > .env << EOF
# Backend Configuration
PORT=8000
FLASK_ENV=development
FLASK_DEBUG=True

# CORS (allows frontend on localhost:5173)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
EOF
    print_success "Backend .env file created"
else
    print_info "Backend .env file already exists"
fi

# Run tests to verify setup
print_info "Running backend tests..."
if python -m pytest tests/ -v > /dev/null 2>&1; then
    print_success "Backend tests passed"
else
    print_error "Backend tests failed - check your setup"
fi

cd ..

echo ""
echo "=================================="
echo "Setting up Frontend"
echo "=================================="
echo ""

cd frontend

# Install frontend dependencies
print_info "Installing Node.js dependencies..."
npm install > /dev/null 2>&1
print_success "Node.js dependencies installed"

# Setup environment variables
if [ ! -f ".env" ]; then
    print_info "Creating frontend .env file..."
    cat > .env << EOF
# Frontend Configuration
VITE_API_URL=http://localhost:8000
EOF
    print_success "Frontend .env file created"
else
    print_info "Frontend .env file already exists"
fi

# Install Playwright browsers if not already installed
if [ ! -d "$HOME/.cache/ms-playwright" ]; then
    print_info "Installing Playwright browsers (this may take a few minutes)..."
    npx playwright install chromium > /dev/null 2>&1
    print_success "Playwright browsers installed"
else
    print_info "Playwright browsers already installed"
fi

cd ..

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
print_success "Backend and Frontend are ready to run"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the backend server:"
echo -e "   ${YELLOW}cd backend${NC}"
echo -e "   ${YELLOW}source venv/bin/activate${NC}"
echo -e "   ${YELLOW}python -m uvicorn app.main:app --reload --port 8000${NC}"
echo ""
echo "2. In a new terminal, start the frontend:"
echo -e "   ${YELLOW}cd frontend${NC}"
echo -e "   ${YELLOW}npm run dev${NC}"
echo ""
echo "3. Open your browser:"
echo -e "   ${YELLOW}http://localhost:5173${NC}"
echo ""
echo "Optional - Run tests:"
echo -e "   Backend:  ${YELLOW}cd backend && pytest tests/${NC}"
echo -e "   Frontend: ${YELLOW}cd frontend && npm run test:e2e${NC}"
echo ""
print_success "Happy coding! 🚀"
echo ""
