#!/usr/bin/env python3
import sys
import json
import os

def main():
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read()
        
        # Parse JSON
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError:
            # If JSON parsing fails, allow the operation
            sys.exit(0)
        
        # Extract file_path from tool_input or directly from data
        # Support both formats: {"tool_input": {"file_path": "..."}} and {"file_path": "..."}
        tool_input = data.get('tool_input', {})
        file_path = tool_input.get('file_path', '') or data.get('file_path', '')
        
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
        try:
            common = os.path.commonpath([abs_file_path, current_dir])
            if common == current_dir:
                # Check if file is in workflow_files directory (allowed)
                workflow_files_dir = os.path.normpath(os.path.join(current_dir, 'workflow_files'))
                try:
                    workflow_common = os.path.commonpath([abs_file_path, workflow_files_dir])
                    if workflow_common == workflow_files_dir:
                        # File is in workflow_files, allow it
                        sys.exit(0)
                except ValueError:
                    # Not in workflow_files
                    pass

                print("Edits are not allowed in this repository. Use external directories added with /add-dir.", file=sys.stderr)
                sys.exit(2)
        except ValueError:
            # Paths are on different drives (Windows) or can't be compared
            # Allow the operation
            pass
        
        sys.exit(0)
        
    except Exception:
        # On any error, allow the operation (fail open)
        sys.exit(0)

if __name__ == "__main__":
    main()