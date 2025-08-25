#!/usr/bin/env python

from __future__ import print_function
import sys
import json
import os

def main():
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read()
        
        # Parse JSON (works in both Python 2 and 3)
        try:
            data = json.loads(input_data)
        except (ValueError, getattr(json, 'JSONDecodeError', ValueError)):
            # If JSON parsing fails, allow the operation
            sys.exit(0)
        
        # Extract file_path from tool_input
        tool_input = data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')
        
        # If no file path found, allow operation
        if not file_path:
            sys.exit(0)
        
        # Get current working directory
        current_dir = os.getcwd()
        
        # Check for Windows UNC paths (they should always be external)
        if file_path.startswith('\\\\') or file_path.startswith('//'):
            # UNC paths are always external/network paths
            sys.exit(0)
        
        # Normalize the path
        if os.path.isabs(file_path):
            # Already absolute
            abs_file_path = os.path.normpath(file_path)
        else:
            # Make it absolute relative to current directory
            abs_file_path = os.path.normpath(os.path.join(current_dir, file_path))
            # Also get the real path to handle symlinks and complex relative paths
            try:
                abs_file_path = os.path.realpath(abs_file_path)
            except:
                pass
        
        # Check if file is under current directory
        # Python 2/3 compatible path comparison
        try:
            # Try Python 3.5+ method first
            if hasattr(os.path, 'commonpath'):
                common = os.path.commonpath([abs_file_path, current_dir])
                if common == current_dir:
                    print("Edits are not allowed in this repository. Use external directories added with /add-dir.", file=sys.stderr)
                    sys.exit(2)
            else:
                # Python 2 fallback: use commonprefix with normalization
                # Ensure paths end with separator for accurate comparison
                abs_file_with_sep = abs_file_path + os.sep if not abs_file_path.endswith(os.sep) else abs_file_path
                current_with_sep = current_dir + os.sep
                
                # Check if file path starts with current directory
                if abs_file_with_sep.startswith(current_with_sep) or abs_file_path == current_dir:
                    print("Edits are not allowed in this repository. Use external directories added with /add-dir.", file=sys.stderr)
                    sys.exit(2)
        except (ValueError, AttributeError):
            # Paths are on different drives (Windows) or can't be compared
            # Allow the operation
            pass
        
        sys.exit(0)
        
    except Exception:
        # On any error, allow the operation (fail open)
        sys.exit(0)

if __name__ == "__main__":
    main()