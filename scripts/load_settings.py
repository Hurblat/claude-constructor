#!/usr/bin/env python3

"""
Load settings and inject them as additional context for Claude Code sessions
This script loads claude-constructor settings (local overrides or defaults)
Falls back to schema defaults if no settings files exist
"""
import json
import os
import sys

CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS = ".claude/settings.claude-constructor.local.json"
CLAUDE_CONSTRUCTOR_SCHEMA = ".claude/settings.claude-constructor.schema.json"

def format_json(file_path):
    """Parse JSON file and format as key: value pairs"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Format each key-value pair
        for key, value in data.items():
            print(f"{key}: {value}")
    except (IOError, OSError) as e:
        print(f"Error reading file {file_path}: {e}", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON in {file_path}: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error processing {file_path}: {e}", file=sys.stderr)
        return False
    
    return True

def load_schema_defaults():
    """Load default values from the JSON schema"""
    try:
        with open(CLAUDE_CONSTRUCTOR_SCHEMA, 'r') as f:
            schema = json.load(f)
        
        defaults = {}
        for prop, config in schema.get('properties', {}).items():
            if prop == '$schema':
                continue
            if 'default' in config:
                defaults[prop] = config['default']
        
        return defaults
    except (IOError, OSError, json.JSONDecodeError):
        # If schema doesn't exist or is invalid, return hardcoded defaults
        return {
            "issue-tracking-provider": "prompt",
            "default-branch": "main",
            "silent-mode": False
        }

def load_and_merge_settings():
    """Load settings, merging local overrides with schema defaults"""
    # Start with schema defaults
    settings = load_schema_defaults()
    
    # If local settings exist, merge them (local overrides defaults)
    if os.path.isfile(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS):
        try:
            with open(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS, 'r') as f:
                local_settings = json.load(f)
                # Skip $schema field when merging
                for key, value in local_settings.items():
                    if key != '$schema':
                        settings[key] = value
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Warning: Invalid local settings file: {e}", file=sys.stderr)
            print("Using default settings instead.", file=sys.stderr)
    
    return settings

def main():
    """Main function to load and display settings"""
    settings = load_and_merge_settings()
    
    # Determine source message
    if os.path.isfile(CLAUDE_CONSTRUCTOR_LOCAL_SETTINGS):
        print("Using LOCAL settings with SCHEMA defaults for missing values:")
    else:
        print("Using SCHEMA defaults:")
    
    # Display merged settings
    for key, value in settings.items():
        print(f"{key}: {value}")



if __name__ == "__main__":
    main()