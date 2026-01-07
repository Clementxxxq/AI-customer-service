#!/usr/bin/env python3
"""
Pre-Test Verification Script
Checks that all components are in place before running tests
"""
import os
import sys
import sqlite3
from pathlib import Path

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Counters
CHECKS_PASSED = 0
CHECKS_FAILED = 0


def print_header(title: str):
    """Print formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{title:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")


def check_result(check_name: str, passed: bool, details: str = ""):
    """Print check result"""
    global CHECKS_PASSED, CHECKS_FAILED
    
    if passed:
        CHECKS_PASSED += 1
        status = f"{GREEN}✅{RESET}"
    else:
        CHECKS_FAILED += 1
        status = f"{RED}❌{RESET}"
    
    print(f"{status} {check_name}")
    if details:
        print(f"   {YELLOW}→ {details}{RESET}")


def check_file_exists(filepath: str) -> bool:
    """Check if file exists"""
    return os.path.isfile(filepath)


def check_dir_exists(dirpath: str) -> bool:
    """Check if directory exists"""
    return os.path.isdir(dirpath)


def check_python_package(package_name: str) -> bool:
    """Check if Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def check_database():
    """Verify database is properly initialized"""
    db_path = "clinic.db"
    
    if not check_file_exists(db_path):
        check_result("Database File Exists", False, "clinic.db not found")
        return False
    
    check_result("Database File Exists", True, "clinic.db found")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables exist
        tables = [
            "doctors",
            "services",
            "customers",
            "appointments",
            "time_slots"
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            if table in existing_tables:
                check_result(f"  Table '{table}' Exists", True)
            else:
                check_result(f"  Table '{table}' Exists", False, f"Missing table: {table}")
                conn.close()
                return False
        
        # Check data
        cursor.execute("SELECT COUNT(*) FROM doctors")
        doctor_count = cursor.fetchone()[0]
        if doctor_count > 0:
            check_result(f"  Sample Data (Doctors)", True, f"{doctor_count} doctors")
        else:
            check_result(f"  Sample Data (Doctors)", False, "No sample data found")
            conn.close()
            return False
        
        cursor.execute("SELECT COUNT(*) FROM services")
        service_count = cursor.fetchone()[0]
        if service_count > 0:
            check_result(f"  Sample Data (Services)", True, f"{service_count} services")
        else:
            check_result(f"  Sample Data (Services)", False, "No services found")
            conn.close()
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        check_result("Database Validation", False, str(e))
        return False


def main():
    """Run all verification checks"""
    print(f"\n{BOLD}{BLUE}{'*'*70}{RESET}")
    print(f"{BOLD}{BLUE}{'PRE-TEST VERIFICATION SCRIPT':^70}{RESET}")
    print(f"{BOLD}{BLUE}{'*'*70}{RESET}")
    
    # Get current directory
    cwd = os.getcwd()
    print(f"\nWorking Directory: {cwd}")
    
    # ===== PYTHON ENVIRONMENT =====
    print_header("PYTHON ENVIRONMENT")
    
    check_result("Python Version", sys.version_info.major >= 3 and sys.version_info.minor >= 9,
                 f"{sys.version.split()[0]} (required: 3.9+)")
    
    # ===== PYTHON PACKAGES =====
    print_header("PYTHON PACKAGES")
    
    required_packages = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "pydantic": "Pydantic",
        "requests": "Requests",
    }
    
    for package, name in required_packages.items():
        installed = check_python_package(package)
        check_result(f"{name}", installed, "installed" if installed else "NOT FOUND")
    
    # ===== BACKEND FILES =====
    print_header("BACKEND FILES")
    
    backend_files = {
        "backend/main.py": "FastAPI Application",
        "backend/routes/chat.py": "Chat Routes",
        "backend/services/llama_service.py": "NLU Service",
        "backend/services/appointment_service.py": "Business Logic (NEW)",
        "backend/schemas/chat.py": "Chat Schemas (NEW)",
        "backend/config/settings.py": "Settings",
    }
    
    for filepath, description in backend_files.items():
        exists = check_file_exists(filepath)
        check_result(f"{description}", exists, filepath if exists else f"NOT FOUND: {filepath}")
    
    # ===== TEST FILES =====
    print_header("TEST FILES")
    
    test_files = {
        "test_e2e.py": "End-to-End Test Suite (NEW)",
        "docs/E2E_TESTING_GUIDE.md": "Test Documentation (NEW)",
        "TESTING_INSTRUCTIONS.md": "Testing Guide (NEW)",
    }
    
    for filepath, description in test_files.items():
        exists = check_file_exists(filepath)
        check_result(f"{description}", exists, filepath if exists else f"NOT FOUND: {filepath}")
    
    # ===== DOCUMENTATION =====
    print_header("DOCUMENTATION")
    
    doc_files = {
        "README.md": "Project README",
        "QUICK_START.md": "Quick Start Guide (NEW)",
        "SYSTEM_COMPLETE.md": "System Overview (NEW)",
        "COMPLETION_CHECKLIST.md": "Completion Checklist (NEW)",
    }
    
    for filepath, description in doc_files.items():
        exists = check_file_exists(filepath)
        check_result(f"{description}", exists, filepath if exists else f"NOT FOUND")
    
    # ===== DATABASE =====
    print_header("DATABASE")
    
    db_ok = check_database()
    
    # ===== OLLAMA AVAILABILITY =====
    print_header("EXTERNAL SERVICES")
    
    print(f"{YELLOW}Note: These services must be running during tests{RESET}\n")
    
    print(f"{YELLOW}Ollama:{RESET}")
    print(f"  Required: http://127.0.0.1:11434")
    print(f"  Start with: {BOLD}ollama serve{RESET}")
    print(f"  Model needed: {BOLD}llama3.2:3b{RESET}")
    print(f"  Check model: {BOLD}ollama list{RESET}\n")
    
    print(f"{YELLOW}Backend:{RESET}")
    print(f"  Required: http://127.0.0.1:8000")
    print(f"  Start with: {BOLD}cd backend && uvicorn main:app --reload{RESET}\n")
    
    # ===== SUMMARY =====
    print_header("VERIFICATION SUMMARY")
    
    total_checks = CHECKS_PASSED + CHECKS_FAILED
    pass_rate = (CHECKS_PASSED / total_checks * 100) if total_checks > 0 else 0
    
    print(f"Total Checks:  {total_checks}")
    print(f"Passed:        {GREEN}{CHECKS_PASSED}{RESET}")
    print(f"Failed:        {RED}{CHECKS_FAILED}{RESET}")
    print(f"Pass Rate:     {BOLD}{pass_rate:.1f}%{RESET}")
    
    # ===== RECOMMENDATIONS =====
    print_header("NEXT STEPS")
    
    if CHECKS_FAILED == 0 and db_ok:
        print(f"{GREEN}✅ All checks passed! Ready to run tests{RESET}\n")
        
        print(f"{BOLD}To start testing:{RESET}\n")
        print(f"  {YELLOW}Terminal 1 (Backend):{RESET}")
        print(f"    cd backend")
        print(f"    uvicorn main:app --reload\n")
        
        print(f"  {YELLOW}Terminal 2 (Ollama):{RESET}")
        print(f"    ollama serve\n")
        
        print(f"  {YELLOW}Terminal 3 (Tests):{RESET}")
        print(f"    python test_e2e.py\n")
        
        print(f"{GREEN}Expected Result: 100% Pass Rate ✅{RESET}\n")
    else:
        print(f"{RED}❌ Some checks failed. Please fix the issues above.{RESET}\n")
        
        if CHECKS_FAILED > 0:
            print(f"{YELLOW}Common Issues:{RESET}")
            print(f"  1. Missing package: {BOLD}pip install -r requirements.txt{RESET}")
            print(f"  2. Missing file: Check file structure and paths")
            print(f"  3. Database: {BOLD}python init_db.py{RESET}\n")
        
        if not db_ok:
            print(f"{YELLOW}Database Issues:{RESET}")
            print(f"  1. Check clinic.db exists")
            print(f"  2. Run: {BOLD}python init_db.py{RESET}")
            print(f"  3. Verify: {BOLD}sqlite3 clinic.db '.tables'{RESET}\n")
    
    # ===== FILE LISTING =====
    print_header("KEY FILES LOCATION")
    
    print(f"{BOLD}Backend Implementation:{RESET}")
    print(f"  routes/chat.py                    → API orchestration")
    print(f"  services/llama_service.py         → NLU parsing")
    print(f"  services/appointment_service.py   → Business logic (NEW)")
    print(f"  schemas/chat.py                   → Data validation (NEW)\n")
    
    print(f"{BOLD}Testing:{RESET}")
    print(f"  test_e2e.py                       → Automated tests")
    print(f"  docs/E2E_TESTING_GUIDE.md         → Test cases\n")
    
    print(f"{BOLD}Documentation:{RESET}")
    print(f"  QUICK_START.md                    → Get started")
    print(f"  TESTING_INSTRUCTIONS.md           → How to run")
    print(f"  SYSTEM_COMPLETE.md                → Architecture")
    print(f"  PROJECT_SUMMARY.md                → Visual summary\n")
    
    return CHECKS_FAILED == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
