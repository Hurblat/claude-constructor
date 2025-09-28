#!/usr/bin/env python3
"""
Test script for the check_path.py hook using unittest framework.
Tests path validation for various file paths.
"""
import unittest
import sys
import os
import json
import subprocess


class TestCheckPath(unittest.TestCase):
    """Test cases for the check_path.py hook."""

    def run_check_path(self, json_input, script_path='check_path.py'):
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
            stdout, stderr = process.communicate(json_input.encode())

            return process.returncode, stderr.decode('utf-8') if stderr else ''
        except Exception as e:
            self.fail(f"Error running script: {str(e)}")

    def run_test_case(self, json_data, expected_exit_code, should_block=None):
        """Run a single test case."""
        json_str = json.dumps(json_data) if isinstance(json_data, dict) else json_data
        exit_code, stderr = self.run_check_path(json_str)

        # Check exit code
        self.assertEqual(exit_code, expected_exit_code,
                         f"Expected exit code {expected_exit_code}, got {exit_code}. "
                         f"Stderr: {stderr}")

        # Additional check for blocking behavior
        if should_block is not None:
            if should_block:
                self.assertEqual(exit_code, 2, f"Should block but got exit code {exit_code}")
            else:
                self.assertNotEqual(exit_code, 2, f"Should not block but got exit code {exit_code}")

    def test_valid_simple_filename(self):
        """Test valid simple filename - should block as it's in current repo."""
        self.run_test_case(
            {"file_path": "test.txt"},
            2,  # Should block edits in current repo
            True
        )

    def test_valid_relative_path(self):
        """Test valid relative path in current directory - should block."""
        self.run_test_case(
            {"file_path": "./subdir/test.txt"},
            2,  # Should block edits in current repo
            True
        )

    def test_parent_directory_traversal(self):
        """Test parent directory traversal (..) - goes outside repo."""
        self.run_test_case(
            {"file_path": "../test.txt"},
            0,  # Goes to parent directory, outside repo
            False
        )

    def test_parent_directory_in_middle(self):
        """Test parent directory in middle of path - should block."""
        self.run_test_case(
            {"file_path": "subdir/../test.txt"},
            2,  # Still in current repo
            True
        )

    def test_absolute_unix_path(self):
        """Test absolute path on Unix systems."""
        if sys.platform != 'win32':
            self.run_test_case(
                {"file_path": "/etc/hosts"},
                0,
                False
            )

    def test_absolute_windows_path(self):
        """Test absolute path on Windows systems."""
        if sys.platform == 'win32':
            self.run_test_case(
                {"file_path": "C:\\temp\\test.txt"},
                0,
                False
            )

    def test_malformed_json(self):
        """Test malformed JSON input."""
        exit_code, stderr = self.run_check_path("{invalid json")
        # Should allow (exit 0) on invalid JSON
        self.assertEqual(exit_code, 0, f"Should handle malformed JSON gracefully, got {exit_code}")

    def test_missing_file_path(self):
        """Test missing file_path field."""
        self.run_test_case(
            {"other_field": "value"},
            0,  # Should allow on missing file_path
            False
        )

    def test_empty_file_path(self):
        """Test empty file path."""
        self.run_test_case(
            {"file_path": ""},
            0,  # Should allow on empty path
            False
        )

    def test_null_file_path(self):
        """Test null file path."""
        self.run_test_case(
            {"file_path": None},
            0,  # Should allow on null
            False
        )

    def test_just_double_dot(self):
        """Test path that is just '..' - parent dir outside repo."""
        self.run_test_case(
            {"file_path": ".."},
            0,  # Parent directory is outside repo
            False
        )

    def test_multiple_parent_directories(self):
        """Test multiple parent directory traversals - may escape repo."""
        # This might escape the repo depending on depth
        # We'll test it allows (exit 0) assuming it escapes
        self.run_test_case(
            {"file_path": "../../../../../../../test.txt"},
            0,  # Should escape repo with enough parent dirs
            False
        )

    def test_hidden_file(self):
        """Test hidden file (starts with dot) - should block in repo."""
        self.run_test_case(
            {"file_path": ".gitignore"},
            2,  # Still in current repo
            True
        )

    def test_special_characters(self):
        """Test file path with special characters - should block in repo."""
        self.run_test_case(
            {"file_path": "test file (v2).txt"},
            2,  # Still in current repo
            True
        )

    def test_unicode_characters(self):
        """Test file path with unicode characters - should block in repo."""
        self.run_test_case(
            {"file_path": "文档.txt"},
            2,  # Still in current repo
            True
        )

    def test_external_tmp_directory(self):
        """Test absolute path to /tmp - should allow as it's external."""
        self.run_test_case(
            {"file_path": "/tmp/test.txt"},
            0,  # External to repo
            False
        )

    def test_external_home_directory(self):
        """Test absolute path to home - should allow as it's external."""
        import os
        home_path = os.path.expanduser("~/Desktop/test.txt")
        self.run_test_case(
            {"file_path": home_path},
            0,  # External to repo
            False
        )


if __name__ == '__main__':
    unittest.main()