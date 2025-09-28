#!/usr/bin/env python3
"""
Test script for the check_completion.py Stop hook.
Tests various scenarios to ensure the hook properly detects incomplete work.
"""
import sys
import json
import tempfile
import subprocess
import os
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def create_test_transcript(messages):
    """Create a temporary transcript file with test messages."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for msg in messages:
            f.write(json.dumps(msg) + '\n')
        return f.name

def run_check_completion(stop_input):
    """Run the check_completion.py script with given input."""
    script_path = Path(__file__).parent / "check_completion.py"

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            input=json.dumps(stop_input),
            capture_output=True,
            text=True,
            timeout=5
        )

        # Try to parse output as JSON
        output = None
        if result.stdout:
            try:
                output = json.loads(result.stdout)
            except json.JSONDecodeError:
                pass

        return result.returncode, output, result.stderr
    except subprocess.TimeoutExpired:
        return -1, None, "Timeout"
    except Exception as e:
        return -1, None, str(e)

def test_scenario(name, messages, expected_allow, description=""):
    """Test a specific scenario."""
    print(f"\nTesting: {name}")
    if description:
        print(f"  Description: {description}")

    # Create test transcript
    transcript_path = create_test_transcript(messages)

    try:
        # Prepare stop hook input
        stop_input = {
            "session_id": "test-session-123",
            "transcript_path": transcript_path,
            "hook_event_name": "Stop",
            "stop_hook_active": False
        }

        # Run the check
        exit_code, output, stderr = run_check_completion(stop_input)

        # Check results
        if expected_allow:
            # Should allow stop (exit code 0)
            if exit_code == 0:
                print(f"  {GREEN}✓ Correctly allowed stop{RESET}")
                return True
            else:
                print(f"  {RED}✗ Incorrectly blocked stop{RESET}")
                if output and 'reason' in output:
                    print(f"    Reason: {output['reason']}")
                return False
        else:
            # Should block stop (exit code 2)
            if exit_code == 2:
                print(f"  {GREEN}✓ Correctly blocked stop{RESET}")
                if output and 'reason' in output:
                    print(f"    Reason: {output['reason']}")
                return True
            else:
                print(f"  {RED}✗ Incorrectly allowed stop{RESET}")
                return False

    finally:
        # Clean up transcript file
        try:
            os.unlink(transcript_path)
        except:
            pass

def main():
    print(f"{YELLOW}Testing Stop Hook: check_completion.py{RESET}")
    print("=" * 60)

    test_results = []

    # Test 1: Complete work - should allow stop
    test_results.append(test_scenario(
        "Complete Work",
        [
            {"type": "user_message", "content": "Please update the README file"},
            {"type": "assistant_message", "content": "I've successfully completed updating the README file. All changes have been made."}
        ],
        expected_allow=True,
        description="Work is clearly completed"
    ))

    # Test 2: Incomplete todos - should block stop
    test_results.append(test_scenario(
        "Incomplete Todos",
        [
            {"type": "user_message", "content": "Help me implement three features"},
            {"type": "assistant_message", "content": 'I\'m updating the todo list with tasks marked as "status": "in_progress" and "status": "pending"'}
        ],
        expected_allow=False,
        description="Todos are still in progress or pending"
    ))

    # Test 3: Unresolved error - should block stop
    test_results.append(test_scenario(
        "Unresolved Error",
        [
            {"type": "user_message", "content": "Run the tests"},
            {"type": "assistant_message", "content": "Running tests...\nError: Test failed - TypeError in test_function"}
        ],
        expected_allow=False,
        description="Error occurred without resolution"
    ))

    # Test 4: Resolved error - should allow stop
    test_results.append(test_scenario(
        "Resolved Error",
        [
            {"type": "user_message", "content": "Run the tests"},
            {"type": "assistant_message", "content": "Error: Test failed"},
            {"type": "assistant_message", "content": "I've fixed the error. Tests are now passing successfully."}
        ],
        expected_allow=True,
        description="Error was resolved"
    ))

    # Test 5: Waiting for user input - should block stop
    test_results.append(test_scenario(
        "Waiting for User Input",
        [
            {"type": "user_message", "content": "Help me choose a framework"},
            {"type": "assistant_message", "content": "Would you like to use React or Vue for this project?"}
        ],
        expected_allow=False,
        description="Asked a question, waiting for response"
    ))

    # Test 6: Question answered - should allow stop
    test_results.append(test_scenario(
        "Question Answered",
        [
            {"type": "assistant_message", "content": "Should I proceed with the implementation?"},
            {"type": "user_message", "content": "No, that's enough for now"},
            {"type": "assistant_message", "content": "Understood. I'll stop here."}
        ],
        expected_allow=True,
        description="User responded to question"
    ))

    # Test 7: Mid-task indicators - should block stop
    test_results.append(test_scenario(
        "Mid-Task Indicators",
        [
            {"type": "user_message", "content": "Implement the feature"},
            {"type": "assistant_message", "content": "I'll now implement the authentication system. Let me start by creating the user model."}
        ],
        expected_allow=False,
        description="Indicates more work to do"
    ))

    # Test 8: Starting but then completing - should allow stop
    test_results.append(test_scenario(
        "Started and Completed",
        [
            {"type": "assistant_message", "content": "Let me implement this feature"},
            {"type": "assistant_message", "content": "I've completed the implementation. Everything is working as expected."}
        ],
        expected_allow=True,
        description="Started task but then completed it"
    ))

    # Test 9: Multiple indicators of incompleteness - should block stop
    test_results.append(test_scenario(
        "Multiple Incomplete Indicators",
        [
            {"type": "user_message", "content": "Fix all the bugs"},
            {"type": "assistant_message", "content": 'Error: Failed to connect\nLet me investigate this issue\n[in_progress] Debugging connection'}
        ],
        expected_allow=False,
        description="Multiple signs of incomplete work"
    ))

    # Test 10: Stop hook already active - should allow stop
    test_results.append(test_scenario(
        "Stop Hook Active",
        [
            {"type": "assistant_message", "content": "Let me continue working on this"}
        ],
        expected_allow=True,
        description="Avoiding infinite loop when stop_hook_active=true"
    ))

    # Special test for stop_hook_active flag
    print(f"\nTesting: Stop Hook Already Active")
    print(f"  Description: Should allow stop to prevent infinite loop")
    transcript_path = create_test_transcript([
        {"type": "assistant_message", "content": "Still working..."}
    ])
    try:
        stop_input = {
            "session_id": "test-session",
            "transcript_path": transcript_path,
            "stop_hook_active": True  # This flag should make it allow stop
        }
        exit_code, _, _ = run_check_completion(stop_input)
        if exit_code == 0:
            print(f"  {GREEN}✓ Correctly allowed stop when hook active{RESET}")
            test_results.append(True)
        else:
            print(f"  {RED}✗ Should have allowed stop when hook active{RESET}")
            test_results.append(False)
    finally:
        try:
            os.unlink(transcript_path)
        except:
            pass

    # Summary
    print("\n" + "=" * 60)
    passed = sum(test_results)
    total = len(test_results)

    if passed == total:
        print(f"{GREEN}✓ All {total} tests passed!{RESET}")
        return 0
    else:
        print(f"{RED}✗ {total - passed}/{total} tests failed{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())