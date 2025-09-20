#!/usr/bin/env python3

"""
Test cases for load_settings.py
"""
import json
import os
import sys
import tempfile
import unittest
import shutil
from io import StringIO

# Import the module under test
from load_settings import format_json, main, load_and_merge_settings, CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS


class TestLoadSettings(unittest.TestCase):
    """Test cases for the load settings functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create .claude directory
        os.makedirs('.claude', exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)
        
    def test_format_json_valid_file(self):
        """Test format_json with a valid JSON file"""
        test_data = {"key1": "value1", "key2": "value2"}
        test_file = os.path.join(self.test_dir, "test.json")
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
            
        # Capture output
        old_stdout = sys.stdout            
        sys.stdout = StringIO()
        result = format_json(test_file)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertTrue(result)
        self.assertIn("key1: value1", output)
        self.assertIn("key2: value2", output)
        
    def test_format_json_invalid_file(self):
        """Test format_json with invalid JSON"""
        test_file = os.path.join(self.test_dir, "invalid.json")
        
        with open(test_file, 'w') as f:
            f.write("invalid json content")
            
        result = format_json(test_file)
        self.assertFalse(result)
        
    def test_format_json_missing_file(self):
        """Test format_json with missing file"""
        result = format_json("nonexistent.json")
        self.assertFalse(result)
        
    def test_main_with_local_settings(self):
        """Test main function with local settings file - should merge with defaults"""
        test_data = {
            "issue-tracking-provider": "jira",  # Override this
            # default-branch and silent-mode will use defaults
        }
        
        with open(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS, 'w') as f:
            json.dump(test_data, f)
            
        old_stdout = sys.stdout            
        sys.stdout = StringIO()
        main()
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertIn("Using LOCAL settings with SCHEMA defaults", output)
        self.assertIn("issue-tracking-provider: jira", output)  # Local override
        self.assertIn("default-branch: main", output)  # Schema default
        self.assertIn("silent-mode: False", output)  # Schema default
        
    def test_main_with_no_local_settings(self):
        """Test main function with no local settings - should use schema defaults"""
        # Ensure local settings file doesn't exist
        if os.path.exists(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS):
            os.remove(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS)
            
        old_stdout = sys.stdout            
        sys.stdout = StringIO()
        main()
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertIn("Using SCHEMA defaults:", output)
        self.assertIn("issue-tracking-provider: prompt", output)
        
    def test_main_no_settings_files(self):
        """Test main function with no settings files - should use schema defaults"""
        old_stdout = sys.stdout            
        sys.stdout = StringIO()
        main()
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertIn("Using SCHEMA defaults:", output)
        self.assertIn("issue-tracking-provider: prompt", output)
        self.assertIn("default-branch: main", output)
        self.assertIn("silent-mode: False", output)
    
    def test_partial_local_override(self):
        """Test that partial local settings properly merge with defaults"""
        # Only override one setting
        test_data = {"silent-mode": True}
        
        with open(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS, 'w') as f:
            json.dump(test_data, f)
        
        settings = load_and_merge_settings()
        
        # Check merged result
        self.assertEqual(settings["silent-mode"], True)  # Local override
        self.assertEqual(settings["issue-tracking-provider"], "prompt")  # Default
        self.assertEqual(settings["default-branch"], "main")  # Default


if __name__ == "__main__":
    unittest.main()