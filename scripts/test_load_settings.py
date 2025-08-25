#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test cases for load_settings.py
Compatible with Python 2 and Python 3
"""

from __future__ import print_function
import json
import os
import sys
import tempfile
import unittest
import shutil

# Import the module under test
from load_settings import format_json, main, CLAUDE_CONSTRUCTOR_DEFAULT_SETTINGS, CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS


class TestLoadSettings(unittest.TestCase):
    """Test cases for the load settings functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create .claude directory
        try:
            os.makedirs('.claude')
        except OSError:
            pass  # Directory might already exist
        
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
        try:
            from io import StringIO
        except ImportError:
            from StringIO import StringIO
            
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
        """Test main function with local settings file"""
        test_data = {"local-setting": "local-value"}
        
        with open(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS, 'w') as f:
            json.dump(test_data, f)
            
        old_stdout = sys.stdout
        try:
            from io import StringIO
        except ImportError:
            from StringIO import StringIO
            
        sys.stdout = StringIO()
        main()
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertIn("Using LOCAL settings:", output)
        self.assertIn("local-setting: local-value", output)
        
    def test_main_with_default_settings_only(self):
        """Test main function with only default settings file"""
        test_data = {"default-setting": "default-value"}
        
        with open(CLAUDE_CONSTRUCTOR_DEFAULT_SETTINGS, 'w') as f:
            json.dump(test_data, f)
            
        old_stdout = sys.stdout
        try:
            from io import StringIO
        except ImportError:
            from StringIO import StringIO
            
        sys.stdout = StringIO()
        main()
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertIn("Using DEFAULT settings:", output)
        self.assertIn("default-setting: default-value", output)
        
    def test_main_no_settings_files(self):
        """Test main function with no settings files"""
        old_stdout = sys.stdout
        try:
            from io import StringIO
        except ImportError:
            from StringIO import StringIO
            
        sys.stdout = StringIO()
        main()
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        self.assertIn("No settings file found", output)


if __name__ == "__main__":
    unittest.main()