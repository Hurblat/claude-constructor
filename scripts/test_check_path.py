#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import json
import subprocess

# Colors for output (if terminal supports it)
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
if not sys.stdout.isatty():
    GREEN = RED = YELLOW = RESET = ''

def run_check_path(json_input, script_path='check_path.py'):
    """Run the check_path script with given JSON input and return exit code."""
    try:
        # Get the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_script_path = os.path.join(script_dir, script_path)
        
        # Run the script
        process = subprocess.Popen(
            [sys.executable, full_script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Send input and get output
        stdout, stderr = process.communicate(json_input.encode() if hasattr(json_input, 'encode') else json_input)
        
        return process.returncode, stderr.decode() if stderr else ''
    except Exception as e:
        print("Error running script: %s" % str(e))
        return -1, str(e)

def test_case(name, json_data, expected_exit_code, should_block=None):
    """Run a single test case."""
    json_str = json.dumps(json_data) if isinstance(json_data, dict) else json_data
    exit_code, stderr = run_check_path(json_str)
    
    # Determine if test passed
    passed = (exit_code == expected_exit_code)
    if should_block is not None:
        if should_block and exit_code != 2:
            passed = False
        elif not should_block and exit_code == 2:
            passed = False
    
    # Print result
    print("%sTesting:%s %s" % (YELLOW, RESET, name))
    print("  Input: %s" % json_str[:100])
    
    if exit_code == expected_exit_code:
        print("  ✓ Exit code: %d (expected %d)" % (exit_code, expected_exit_code))
    else:
        print("  %s✗ Exit code: %d (expected %d)%s" % (RED, exit_code, expected_exit_code, RESET))
        passed = False
    
    if should_block and stderr:
        if "Edits are not allowed" in stderr:
            print("  ✓ Error message contains: 'Edits are not allowed'")
        else:
            print("  %s✗ Error message: '%s'%s" % (RED, stderr.strip(), RESET))
            passed = False
    
    if passed:
        print("  %s✓ PASS%s" % (GREEN, RESET))
    else:
        print("  %s✗ FAIL%s" % (RED, RESET))
    
    print()
    return passed

def main():
    print("Testing check_path.py...")
    print("Current working directory: %s" % os.getcwd())
    print("-" * 50)
    
    tests_run = 0
    tests_passed = 0
    tests_failed = 0
    
    # ALLOWED PATHS
    print("=== ALLOWED PATHS ===")
    
    # Basic external paths
    for test in [
        ("absolute external path", {"file_path": "/external/dir/file.txt"}, 0, False),
        ("relative path outside current dir", {"file_path": "../outside/file.txt"}, 0, False),
        ("system temp directory", {"file_path": "/tmp/test.txt"}, 0, False),
        ("system var directory", {"file_path": "/var/log/app.log"}, 0, False),
    ]:
        if test_case(*test):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # WSL-specific paths
    print("=== WSL PATHS ===")
    for test in [
        ("WSL Windows C drive mount", {"file_path": "/mnt/c/Users/username/file.txt"}, 0, False),
        ("WSL Windows D drive mount", {"file_path": "/mnt/d/projects/app/file.js"}, 0, False),
        ("Windows WSL UNC path", {"file_path": "\\\\wsl$\\Ubuntu\\home\\user\\file.txt"}, 0, False),
        ("WSL instance mount", {"file_path": "/mnt/wsl/instances/Ubuntu/file.txt"}, 0, False),
    ]:
        if test_case(*test):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # macOS-specific paths
    print("=== macOS PATHS ===")
    for test in [
        ("macOS user directory", {"file_path": "/Users/username/Documents/file.txt"}, 0, False),
        ("macOS application bundle", {"file_path": "/Applications/MyApp.app/Contents/file.txt"}, 0, False),
        ("macOS system library", {"file_path": "/System/Library/file.txt"}, 0, False),
        ("macOS mounted volume", {"file_path": "/Volumes/ExternalDrive/file.txt"}, 0, False),
        ("macOS private temp", {"file_path": "/private/tmp/file.txt"}, 0, False),
    ]:
        if test_case(*test):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # Linux-specific paths
    print("=== LINUX PATHS ===")
    for test in [
        ("Linux user home", {"file_path": "/home/username/project/file.txt"}, 0, False),
        ("Linux usr local", {"file_path": "/usr/local/bin/app"}, 0, False),
        ("Linux opt directory", {"file_path": "/opt/myapp/config.json"}, 0, False),
        ("Linux media mount", {"file_path": "/media/usb/file.txt"}, 0, False),
        ("Linux snap package", {"file_path": "/snap/myapp/current/file.txt"}, 0, False),
    ]:
        if test_case(*test):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # BLOCKED PATHS
    print("=== BLOCKED PATHS ===")
    for test in [
        ("relative path in current dir", {"file_path": "./local_file.txt"}, 2, True),
        ("implicit relative path in current dir", {"file_path": "local_file.txt"}, 2, True),
        ("subdirectory in current dir", {"file_path": "./scripts/test.sh"}, 2, True),
        ("deep subdirectory in current dir", {"file_path": "src/main.js"}, 2, True),
    ]:
        if test_case(*test):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # PATH NORMALIZATION
    print("=== PATH NORMALIZATION ===")
    for test in [
        ("double slashes in external path", {"file_path": "/external//double/slash/file.txt"}, 0, False),
        ("current dir reference in external path", {"file_path": "/external/./current/ref/file.txt"}, 0, False),
        ("parent dir reference in external path", {"file_path": "/external/sub/../parent/file.txt"}, 0, False),
        ("normalized to local path", {"file_path": "./sub/../local_file.txt"}, 2, True),
    ]:
        if test_case(*test):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # Complex path - this one is tricky, depends on actual directory structure
    # Skip or adjust expectation based on actual behavior
    current_dir = os.getcwd()
    complex_path = "../../external/../current/file.txt"
    resolved = os.path.normpath(os.path.join(current_dir, complex_path))
    if resolved.startswith(current_dir):
        expected = 2
    else:
        expected = 0
    
    if test_case("complex path resolution", {"file_path": complex_path}, expected, expected == 2):
        tests_passed += 1
    else:
        tests_failed += 1
    tests_run += 1
    
    # EDGE CASES
    print("=== EDGE CASES ===")
    for test in [
        ("empty JSON object", {}, 0, False),
        ("JSON without file_path", {"other_field": "value"}, 0, False),
        ("empty file_path", {"file_path": ""}, 0, False),
        ("invalid JSON", "invalid json", 0, False),
        ("null file_path", {"file_path": None}, 0, False),
        ("empty input", "", 0, False),
    ]:
        if test_case(*test):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # SPECIAL CHARACTERS
    print("=== SPECIAL CHARACTERS ===")
    for test in [
        ("path with spaces", {"file_path": "/external/file with spaces.txt"}, 0, False),
        ("path with dashes", {"file_path": "/external/file-with-dashes.txt"}, 0, False),
        ("path with underscores", {"file_path": "/external/file_with_underscores.txt"}, 0, False),
        ("path with unicode", {"file_path": "/external/файл.txt"}, 0, False),
    ]:
        if test_case(*test):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # Current directory absolute path - should block
    current_dir = os.getcwd()
    if test_case(
        "absolute path to current directory",
        {"file_path": os.path.join(current_dir, "test.txt")},
        2,
        True
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    tests_run += 1
    
    # Path with .. that resolves to current dir - should block
    if test_case(
        "path with .. that stays in current directory",
        {"file_path": "subdir/../test.txt"},
        2,
        True
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    tests_run += 1
    
    # Just dot (.) - should block
    if test_case(
        "just dot (.)",
        {"file_path": "."},
        2,
        True
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    tests_run += 1
    
    # Just double dot (..) - should allow
    if test_case(
        "just double dot (..)",
        {"file_path": ".."},
        0,
        False
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    tests_run += 1
    
    # Windows-specific tests (only on Windows)
    if sys.platform == 'win32':
        print("=== WINDOWS PATHS ===")
        if test_case(
            "Windows path outside current directory",
            {"file_path": "C:\\temp\\test.txt"},
            0,
            False
        ):
            tests_passed += 1
        else:
            tests_failed += 1
        tests_run += 1
    
    # Summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print("Tests run: %d" % tests_run)
    print("Tests passed: %s%d%s" % (GREEN, tests_passed, RESET))
    print("Tests failed: %s%d%s" % (RED, tests_failed, RESET))
    
    if tests_failed == 0:
        print("%s[SUCCESS]%s All tests passed!" % (GREEN, RESET))
        sys.exit(0)
    else:
        print("%s[FAILURE]%s Some tests failed." % (RED, RESET))
        sys.exit(1)

if __name__ == "__main__":
    main()