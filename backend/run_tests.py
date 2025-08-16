#!/usr/bin/env python3
"""Test runner for LaudatorAI backend."""

import sys
import time
import subprocess
from pathlib import Path

def run_test_file(test_file: str, description: str) -> bool:
    """Run a test file and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 Running {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} PASSED ({duration:.2f}s)")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} FAILED ({duration:.2f}s)")
            if result.stdout:
                print("STDOUT:")
                print(result.stdout)
            if result.stderr:
                print("STDERR:")
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ {description} ERROR: {e}")
        return False

def run_pytest_tests() -> bool:
    """Run pytest tests."""
    print(f"\n{'='*60}")
    print("🧪 Running pytest tests")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ pytest tests PASSED ({duration:.2f}s)")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ pytest tests FAILED ({duration:.2f}s)")
            if result.stdout:
                print("STDOUT:")
                print(result.stdout)
            if result.stderr:
                print("STDERR:")
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ pytest tests ERROR: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting LaudatorAI Backend Test Suite")
    print("=" * 60)
    
    # Test files to run
    test_files = [
        ("tests/test_integration.py", "Integration Tests"),
        ("tests/test_e2e.py", "End-to-End Tests"),
        ("tests/test_performance.py", "Performance Tests"),
        ("tests/test_security.py", "Security Tests"),
        ("tests/test_complete_integration.py", "Complete Integration Tests"),
    ]
    
    # Results tracking
    results = []
    total_start_time = time.time()
    
    # Run individual test files
    for test_file, description in test_files:
        success = run_test_file(test_file, description)
        results.append((description, success))
    
    # Run pytest tests
    pytest_success = run_pytest_tests()
    results.append(("Pytest Tests", pytest_success))
    
    # Calculate total time
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {description}")
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    print(f"Total time: {total_duration:.2f}s")
    
    if passed == total:
        print("\n🎉 All tests passed! The backend is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
