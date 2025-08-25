#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load settings and inject them as additional context for Claude Code sessions
This script loads claude-constructor settings (local overrides or defaults)
Compatible with Python 2 and Python 3
"""

from __future__ import print_function
import json
import os
import sys

CLAUDE_CONSTRUCTOR_DEFAULT_SETTINGS = ".claude/settings.claude-constructor.json"
CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS = ".claude/settings.claude-constructor.local.json"

def format_json(file_path):
    """Parse JSON file and format as key: value pairs"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Format each key-value pair
        for key, value in data.items():
            print("{}: {}".format(key, value))
    except (IOError, OSError) as e:
        print("Error reading file {}: {}".format(file_path, e), file=sys.stderr)
        return False
    except ValueError as e:  # json.JSONDecodeError doesn't exist in Python 2
        print("Error parsing JSON in {}: {}".format(file_path, e), file=sys.stderr)
        return False
    except Exception as e:
        print("Unexpected error processing {}: {}".format(file_path, e), file=sys.stderr)
        return False
    
    return True

def main():
    """Main function to load and display settings"""
    # Check for claude-constructor specific local settings first, then defaults
    if os.path.isfile(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS):
        print("Using LOCAL settings:")
        format_json(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS)
    elif os.path.isfile(CLAUDE_CONSTRUCTOR_DEFAULT_SETTINGS):
        print("Using DEFAULT settings:")
        format_json(CLAUDE_CONSTRUCTOR_DEFAULT_SETTINGS)
    else:
        print("No settings file found")



if __name__ == "__main__":
    main()