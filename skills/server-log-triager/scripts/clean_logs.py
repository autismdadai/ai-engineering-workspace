#!/usr/bin/env python3
import os
import sys
import re
import argparse

def mask_text(text):
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    text = re.sub(ip_pattern, "[REDACTED_IP]", text)
    text = re.sub(email_pattern, "[REDACTED_EMAIL]", text)
    return text

def main():
    parser = argparse.ArgumentParser(description="Non-interactive log parser and PII scrubber.")
    parser.add_argument("--input", required=True, help="Path to raw source log file")
    parser.add_argument("--output", required=True, help="Path to target markdown file destination")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"CRITICAL ERROR: Input log target file not found at: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"CRITICAL ERROR: Failed reading source log buffer: {str(e)}", file=sys.stderr)
        sys.exit(1)

    md_table = ["| Timestamp | Severity Level | System Module | Sanitized Event Message |",
                "| :--- | :--- | :--- | :--- |"]
    
    log_regex = re.compile(r'^([\d\-\s:]+)\s+\[([A-Z]+)\]\s+([A-Za-z0-9_\-]+):\s+(.*)$')
    parsed_count = 0

    for line in lines:
        match = log_regex.match(line.strip())
        if match:
            timestamp, level, module, message = match.groups()
            if level in ["ERROR", "CRITICAL", "FATAL"]:
                sanitized_msg = mask_text(message)
                md_table.append(f"| {timestamp} | {level} | {module} | {sanitized_msg} |")
                parsed_count += 1
        else:
            if any(flag in line.upper() for flag in ["ERROR", "EXCEPTION", "FAIL"]):
                sanitized_line = mask_text(line.strip())
                md_table.append(f"| [UNKNOWN] | ERROR | [UNPARSED] | {sanitized_line} |")
                parsed_count += 1

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_table) + "\n")
        print(f"SUCCESS: Generated sanitized log analysis suite report. Parsed {parsed_count} incident events rows.")
        sys.exit(0)
    except Exception as e:
        print(f"CRITICAL ERROR: Failed compiling file generation buffers on filesystem disk: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
