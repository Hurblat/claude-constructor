#!/usr/bin/env python3
"""
Stop hook script to detect if Claude Code has actually completed work or stopped prematurely.
Analyzes the conversation transcript to determine if work is incomplete.
"""
import sys
import json
import os
import re
from typing import Dict, List, Tuple

def read_transcript(transcript_path: str) -> List[Dict]:
    """Read and parse the conversation transcript."""
    try:
        transcript = []
        with open(transcript_path, 'r') as f:
            for line in f:
                if line.strip():
                    transcript.append(json.loads(line))
        return transcript
    except Exception as e:
        print(f"Error reading transcript: {e}", file=sys.stderr)
        return []

def extract_recent_messages(transcript: List[Dict], limit: int = 10) -> List[Dict]:
    """Extract the most recent messages from the transcript."""
    recent = []
    for entry in reversed(transcript):
        if entry.get('type') in ['user_message', 'assistant_message']:
            recent.append(entry)
            if len(recent) >= limit:
                break
    return list(reversed(recent))

def check_todos_status(messages: List[Dict]) -> Tuple[bool, str]:
    """Check if there are incomplete todos in recent messages."""
    todo_patterns = [
        r'"status":\s*"in_progress"',
        r'"status":\s*"pending"',
        r'\[in_progress\]',
        r'\[pending\]',
        r'marking.*as in_progress',
        r'Let me start by',
        r'Let me continue with',
        r'Now let me',
        r"I'll start by",
        r"I'll continue",
        r'TodoWrite.*in_progress',
        r'TodoWrite.*pending'
    ]

    completion_patterns = [
        r'"status":\s*"completed"',
        r'\[completed\]',
        r'marking.*as completed',
        r'All.*completed',
        r'Successfully completed',
        r'Task.*finished',
        r'Work.*done'
    ]

    # Look for todos in the last few assistant messages
    incomplete_found = False
    completion_found = False

    for msg in messages:
        if msg.get('type') == 'assistant_message':
            content = msg.get('content', '')

            # Check for incomplete patterns
            for pattern in todo_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    incomplete_found = True

            # Check for completion patterns
            for pattern in completion_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    completion_found = True

    if incomplete_found and not completion_found:
        return False, "Incomplete todos detected. Work appears to be in progress."

    return True, ""

def check_unresolved_errors(messages: List[Dict]) -> Tuple[bool, str]:
    """Check for unresolved errors or failures."""
    error_patterns = [
        r'error:',
        r'Error:',
        r'ERROR',
        r'failed',
        r'Failed',
        r'FAILED',
        r'exception',
        r'Exception',
        r'traceback',
        r'Traceback',
        r'command not found',
        r'permission denied',
        r'cannot find',
        r'unable to'
    ]

    resolution_patterns = [
        r'fixed',
        r'Fixed',
        r'resolved',
        r'Resolved',
        r'addressed',
        r'corrected',
        r'successfully',
        r'working now',
        r'should work'
    ]

    last_error_index = -1
    last_resolution_index = -1

    for i, msg in enumerate(messages):
        if msg.get('type') == 'assistant_message':
            content = msg.get('content', '')

            # Check for errors
            for pattern in error_patterns:
                if re.search(pattern, content):
                    last_error_index = i

            # Check for resolutions
            for pattern in resolution_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    last_resolution_index = i

    # If there's an error after the last resolution, it's unresolved
    if last_error_index > last_resolution_index and last_error_index >= 0:
        return False, "Unresolved errors detected. Please address them before stopping."

    return True, ""

def check_waiting_for_input(messages: List[Dict]) -> Tuple[bool, str]:
    """Check if Claude is waiting for user input."""
    question_patterns = [
        r'\?$',  # Ends with question mark
        r'Would you like',
        r'Do you want',
        r'Should I',
        r'Shall I',
        r'Would you prefer',
        r'Please.*confirm',
        r'Please.*let me know',
        r'What.*would you',
        r'How.*would you'
    ]

    # Check the last assistant message for questions
    for msg in reversed(messages):
        if msg.get('type') == 'assistant_message':
            content = msg.get('content', '')
            for pattern in question_patterns:
                if re.search(pattern, content):
                    # Check if there's a user response after this
                    has_user_response = False
                    for subsequent_msg in messages[messages.index(msg)+1:]:
                        if subsequent_msg.get('type') == 'user_message':
                            has_user_response = True
                            break

                    if not has_user_response:
                        return False, "Waiting for user response to a question."
            break  # Only check the last assistant message

    return True, ""

def check_mid_task_indicators(messages: List[Dict]) -> Tuple[bool, str]:
    """Check for indicators that Claude is in the middle of a task."""
    mid_task_patterns = [
        r"I'm going to",
        r"I'll now",
        r"Let me now",
        r"Next,? I",
        r"Now I need to",
        r"I should now",
        r"I need to",
        r"Let's start",
        r"Starting to",
        r"Beginning to",
        r"I'll begin",
        r"First,? I",
        r"I'll check",
        r"Let me check",
        r"I'll investigate",
        r"Let me search",
        r"Searching for",
        r"Looking for"
    ]

    completion_patterns = [
        r"I've completed",
        r"I've finished",
        r"completed all",
        r"finished all",
        r"Everything.*done",
        r"All.*implemented",
        r"Successfully.*completed",
        r"Task.*complete",
        r"Implementation.*complete",
        r"Work.*finished"
    ]

    # Check the last assistant message
    for msg in reversed(messages):
        if msg.get('type') == 'assistant_message':
            content = msg.get('content', '')

            # Check for completion first
            for pattern in completion_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return True, ""

            # Then check for mid-task indicators
            for pattern in mid_task_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return False, "Task appears to be in progress. Claude indicated more work to do."

            break  # Only check the last assistant message

    return True, ""

def analyze_stop_reason(transcript_path: str) -> Tuple[bool, str]:
    """
    Analyze the conversation transcript to determine if Claude should stop.
    Returns (should_allow_stop, reason_if_blocking)
    """
    transcript = read_transcript(transcript_path)
    if not transcript:
        # If we can't read the transcript, allow the stop
        return True, ""

    messages = extract_recent_messages(transcript)

    # Run all checks
    checks = [
        check_todos_status,
        check_unresolved_errors,
        check_waiting_for_input,
        check_mid_task_indicators
    ]

    for check_func in checks:
        allow_stop, reason = check_func(messages)
        if not allow_stop:
            return False, reason

    return True, ""

def main():
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read()

        # Parse JSON
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            sys.exit(0)  # Allow stop on error

        # Extract fields
        transcript_path = data.get('transcript_path', '')
        stop_hook_active = data.get('stop_hook_active', False)

        # If stop hook is already active, avoid infinite loop
        if stop_hook_active:
            sys.exit(0)

        # Check if transcript path exists
        if not transcript_path or not os.path.exists(transcript_path):
            print(f"Transcript not found: {transcript_path}", file=sys.stderr)
            sys.exit(0)  # Allow stop if no transcript

        # Analyze the stop reason
        allow_stop, reason = analyze_stop_reason(transcript_path)

        if allow_stop:
            # Work appears complete, allow Claude to stop
            sys.exit(0)
        else:
            # Work appears incomplete, block the stop
            output = {
                "decision": "block",
                "reason": f"⚠️ {reason}\n\nPlease complete the current task or explicitly tell me if you want to stop here."
            }
            print(json.dumps(output))
            sys.exit(2)

    except Exception as e:
        # On any unexpected error, allow the stop (fail open)
        print(f"Unexpected error in stop hook: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()