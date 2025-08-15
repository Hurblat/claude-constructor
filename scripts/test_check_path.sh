#!/bin/bash

# Test script for check_path.sh
# Tests various path scenarios across different platforms (WSL, macOS, Linux)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK_PATH_SCRIPT="$SCRIPT_DIR/check_path.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

test_case() {
    local input="$1"
    local expected_exit="$2"
    local description="$3"
    local expected_stderr="$4"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    
    echo -e "${YELLOW}Testing:${NC} $description"
    echo "  Input: $input"
    
    # Run the test and capture output
    local stderr_output
    stderr_output=$(echo "$input" | "$CHECK_PATH_SCRIPT" 2>&1)
    local actual_exit=$?
    
    local test_passed=true
    
    # Check exit code
    if [ $actual_exit -eq $expected_exit ]; then
        echo "  ✓ Exit code: $actual_exit (expected $expected_exit)"
    else
        echo -e "  ${RED}✗ Exit code: $actual_exit (expected $expected_exit)${NC}"
        test_passed=false
    fi
    
    # Check stderr if expected
    if [ -n "$expected_stderr" ]; then
        if [[ "$stderr_output" == *"$expected_stderr"* ]]; then
            echo "  ✓ Error message contains: '$expected_stderr'"
        else
            echo -e "  ${RED}✗ Error message: '$stderr_output' (expected to contain '$expected_stderr')${NC}"
            test_passed=false
        fi
    fi
    
    if [ "$test_passed" = true ]; then
        echo -e "  ${GREEN}✓ PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "  ${RED}✗ FAIL${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    echo
}

echo "Testing check_path.sh across different platforms..."
echo "Current working directory: $(pwd)"
echo

# Basic allowed cases (external paths)
echo "=== ALLOWED PATHS ==="
test_case '{"file_path": "/external/dir/file.txt"}' 0 "absolute external path"
test_case '{"file_path": "../outside/file.txt"}' 0 "relative path outside current dir"
test_case '{"file_path": "/tmp/test.txt"}' 0 "system temp directory"
test_case '{"file_path": "/var/log/app.log"}' 0 "system var directory"

# WSL-specific paths
echo "=== WSL PATHS ==="
test_case '{"file_path": "/mnt/c/Users/username/file.txt"}' 0 "WSL Windows C drive mount"
test_case '{"file_path": "/mnt/d/projects/app/file.js"}' 0 "WSL Windows D drive mount"
test_case '{"file_path": "\\\\wsl$\\Ubuntu\\home\\user\\file.txt"}' 0 "Windows WSL UNC path (escaped)"
test_case '{"file_path": "/mnt/wsl/instances/Ubuntu/file.txt"}' 0 "WSL instance mount"

# macOS-specific paths
echo "=== macOS PATHS ==="
test_case '{"file_path": "/Users/username/Documents/file.txt"}' 0 "macOS user directory"
test_case '{"file_path": "/Applications/MyApp.app/Contents/file.txt"}' 0 "macOS application bundle"
test_case '{"file_path": "/System/Library/file.txt"}' 0 "macOS system library"
test_case '{"file_path": "/Volumes/ExternalDrive/file.txt"}' 0 "macOS mounted volume"
test_case '{"file_path": "/private/tmp/file.txt"}' 0 "macOS private temp"

# Linux-specific paths
echo "=== LINUX PATHS ==="
test_case '{"file_path": "/home/username/project/file.txt"}' 0 "Linux user home"
test_case '{"file_path": "/usr/local/bin/app"}' 0 "Linux usr local"
test_case '{"file_path": "/opt/myapp/config.json"}' 0 "Linux opt directory"
test_case '{"file_path": "/media/usb/file.txt"}' 0 "Linux media mount"
test_case '{"file_path": "/snap/myapp/current/file.txt"}' 0 "Linux snap package"

# Blocked cases (current directory)
echo "=== BLOCKED PATHS ==="
test_case '{"file_path": "./local_file.txt"}' 2 "relative path in current dir" "Edits are not allowed"
test_case '{"file_path": "local_file.txt"}' 2 "implicit relative path in current dir" "Edits are not allowed"
test_case '{"file_path": "./scripts/test.sh"}' 2 "subdirectory in current dir" "Edits are not allowed"
test_case '{"file_path": "src/main.js"}' 2 "deep subdirectory in current dir" "Edits are not allowed"

# Complex path normalization
echo "=== PATH NORMALIZATION ==="
test_case '{"file_path": "/external//double/slash/file.txt"}' 0 "double slashes in external path"
test_case '{"file_path": "/external/./current/ref/file.txt"}' 0 "current dir reference in external path"
test_case '{"file_path": "/external/sub/../parent/file.txt"}' 0 "parent dir reference in external path"
test_case '{"file_path": "./sub/../local_file.txt"}' 2 "normalized to local path" "Edits are not allowed"
test_case '{"file_path": "../../external/../current/file.txt"}' 2 "complex path that resolves to current dir" "Edits are not allowed"

# Edge cases
echo "=== EDGE CASES ==="
test_case '{}' 0 "empty JSON object"
test_case '{"other_field": "value"}' 0 "JSON without file_path"
test_case '{"file_path": ""}' 0 "empty file_path"
test_case 'invalid json' 0 "invalid JSON"
test_case '{"file_path": null}' 0 "null file_path"
test_case '' 0 "empty input"

# Special characters and encoding
echo "=== SPECIAL CHARACTERS ==="
test_case '{"file_path": "/external/file with spaces.txt"}' 0 "path with spaces"
test_case '{"file_path": "/external/file-with-dashes.txt"}' 0 "path with dashes"
test_case '{"file_path": "/external/file_with_underscores.txt"}' 0 "path with underscores"
test_case '{"file_path": "/external/файл.txt"}' 0 "path with unicode characters"

# Summary
echo "===================="
echo "TEST SUMMARY"
echo "===================="
echo "Tests run: $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi