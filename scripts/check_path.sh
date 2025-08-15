#!/bin/bash

# Read JSON from stdin and extract file_path using simpler pattern matching
input=$(cat)

# Extract file_path using a simpler approach
file_path=$(echo "$input" | grep -o '"file_path" *: *"[^"]*"' | cut -d'"' -f4)

# If no file path found, try alternative extraction
if [ -z "$file_path" ]; then
    file_path=$(echo "$input" | sed -n 's/.*"file_path" *: *"\([^"]*\)".*/\1/p')
fi

# If still no file path, allow operation
if [ -z "$file_path" ]; then
    exit 0
fi

# Get current working directory
current_dir=$(pwd)

# Simple approach: just check if path starts with current directory or relative patterns
# Convert to absolute path for absolute paths only
if [[ "$file_path" = /* ]] || [[ "$file_path" = \\\\* ]]; then
    abs_file_path="$file_path"
    # Simple cleanup for absolute paths
    abs_file_path=$(echo "$abs_file_path" | sed 's|//\+|/|g')
else
    # For relative paths, check common patterns that indicate current directory
    case "$file_path" in
        ./* | */../* | */. | */.. | . | .. )
            # These patterns might resolve to current directory, block them
            abs_file_path="$current_dir/$file_path"
            ;;
        ../* )
            # Paths starting with ../ should be allowed (going outside)
            abs_file_path="external_path"
            ;;
        * )
            # Other relative paths (no ./ prefix) are in current directory
            abs_file_path="$current_dir/$file_path"
            ;;
    esac
fi

# Check if file is under current directory
case "$abs_file_path" in
    "$current_dir"/*)
        echo "Edits are not allowed in this repository. Use external directories added with /add-dir." >&2
        exit 2
        ;;
    *)
        exit 0
        ;;
esac
