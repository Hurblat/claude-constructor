#!/usr/bin/env python3
"""
Test script for the check_completion.py Stop hook using unittest framework.
Tests various scenarios to ensure the hook properly detects incomplete work.
"""
import unittest
import sys
import json
import tempfile
import subprocess
import os
from pathlib import Path


class TestCheckCompletion(unittest.TestCase):
    """Test cases for the check_completion.py stop hook."""

    def create_test_transcript(self, messages):
        """Create a temporary transcript file with test messages."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            for msg in messages:
                f.write(json.dumps(msg) + '\n')
            return f.name

    def run_check_completion(self, stop_input):
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

    def run_scenario(self, messages, expected_allow):
        """Helper to run a test scenario."""
        # Create test transcript
        transcript_path = self.create_test_transcript(messages)

        try:
            # Prepare stop hook input
            stop_input = {
                "session_id": "test-session-123",
                "transcript_path": transcript_path,
                "hook_event_name": "Stop",
                "stop_hook_active": False
            }

            # Run the check
            exit_code, output, stderr = self.run_check_completion(stop_input)

            # Check results
            if expected_allow:
                # Should allow stop (exit code 0)
                self.assertEqual(exit_code, 0,
                    f"Should allow stop but got exit code {exit_code}. "
                    f"Reason: {output.get('reason') if output else 'Unknown'}")
            else:
                # Should block stop (exit code 2)
                self.assertEqual(exit_code, 2,
                    f"Should block stop but got exit code {exit_code}")
                if exit_code == 2 and output:
                    self.assertIn('reason', output)

        finally:
            # Clean up transcript file
            try:
                os.unlink(transcript_path)
            except:
                pass

    def test_complete_work(self):
        """Test that completed work allows stop."""
        self.run_scenario([
            {"type": "user_message", "content": "Please update the README file"},
            {"type": "assistant_message", "content": "I've successfully completed updating the README file. All changes have been made."}
        ], expected_allow=True)

    def test_incomplete_todos(self):
        """Test that incomplete todos block stop."""
        self.run_scenario([
            {"type": "user_message", "content": "Help me implement three features"},
            {"type": "assistant_message", "content": 'I\'m updating the todo list with tasks marked as "status": "in_progress" and "status": "pending"'}
        ], expected_allow=False)

    def test_unresolved_error(self):
        """Test that unresolved errors block stop."""
        self.run_scenario([
            {"type": "user_message", "content": "Run the tests"},
            {"type": "assistant_message", "content": "Running tests...\nError: Test failed - TypeError in test_function"}
        ], expected_allow=False)

    def test_resolved_error(self):
        """Test that resolved errors allow stop."""
        self.run_scenario([
            {"type": "user_message", "content": "Run the tests"},
            {"type": "assistant_message", "content": "Error: Test failed"},
            {"type": "assistant_message", "content": "I've fixed the error. Tests are now passing successfully."}
        ], expected_allow=True)

    def test_waiting_for_user_input(self):
        """Test that waiting for user input blocks stop."""
        self.run_scenario([
            {"type": "user_message", "content": "Help me choose a framework"},
            {"type": "assistant_message", "content": "Would you like to use React or Vue for this project?"}
        ], expected_allow=False)

    def test_question_answered(self):
        """Test that answered questions allow stop."""
        self.run_scenario([
            {"type": "assistant_message", "content": "Should I proceed with the implementation?"},
            {"type": "user_message", "content": "No, that's enough for now"},
            {"type": "assistant_message", "content": "Understood. I'll stop here."}
        ], expected_allow=True)

    def test_mid_task_indicators(self):
        """Test that mid-task indicators block stop."""
        self.run_scenario([
            {"type": "user_message", "content": "Implement the feature"},
            {"type": "assistant_message", "content": "I'll now implement the authentication system. Let me start by creating the user model."}
        ], expected_allow=False)

    def test_started_and_completed(self):
        """Test that completed tasks allow stop even if they started with action words."""
        self.run_scenario([
            {"type": "assistant_message", "content": "Let me implement this feature"},
            {"type": "assistant_message", "content": "I've completed the implementation. Everything is working as expected."}
        ], expected_allow=True)

    def test_multiple_incomplete_indicators(self):
        """Test that multiple incomplete indicators block stop."""
        self.run_scenario([
            {"type": "user_message", "content": "Fix all the bugs"},
            {"type": "assistant_message", "content": 'Error: Failed to connect\nLet me investigate this issue\n[in_progress] Debugging connection'}
        ], expected_allow=False)

    def test_stop_hook_already_active(self):
        """Test that stop_hook_active flag prevents infinite loops."""
        transcript_path = self.create_test_transcript([
            {"type": "assistant_message", "content": "Still working..."}
        ])

        try:
            stop_input = {
                "session_id": "test-session",
                "transcript_path": transcript_path,
                "stop_hook_active": True  # This flag should make it allow stop
            }
            exit_code, _, _ = self.run_check_completion(stop_input)
            self.assertEqual(exit_code, 0, "Should allow stop when hook is already active")
        finally:
            try:
                os.unlink(transcript_path)
            except:
                pass

    def test_improved_error_patterns(self):
        """Test that improved error patterns don't match false positives."""
        # Should not block - "error" in normal context
        self.run_scenario([
            {"type": "user_message", "content": "Explain error handling"},
            {"type": "assistant_message", "content": "This error: handling guide is complete. The documentation covers all error scenarios."}
        ], expected_allow=True)

        # Should block - actual error
        self.run_scenario([
            {"type": "user_message", "content": "Run the code"},
            {"type": "assistant_message", "content": "error: compilation failed"}
        ], expected_allow=False)

    def test_context_window_size(self):
        """Test that the increased context window (20 messages) is used."""
        # Create 25 messages total
        messages = []
        for i in range(12):
            messages.append({"type": "user_message", "content": f"Message {i}"})
            messages.append({"type": "assistant_message", "content": f"Response {i}"})

        # Add an incomplete task in message 19 (within new 20-message window)
        messages.append({"type": "assistant_message", "content": "Let me start implementing this feature now."})

        self.run_scenario(messages, expected_allow=False)


if __name__ == '__main__':
    unittest.main()