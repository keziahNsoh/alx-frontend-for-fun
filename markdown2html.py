#!/usr/bin/python3
"""markdown2html.py

A script that converts Markdown files to HTML format. It checks for
the existence of the Markdown file and handles command-line arguments
appropriately.
"""

import sys
import os
import re

def print_usage_and_exit():
    """Print usage instructions and exit with status 1."""
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

def check_file_exists(filename):
    """Check if the given file exists."""
    if not os.path.exists(filename):
        print(f"Missing {filename}", file=sys.stderr)
        sys.exit(1)

def convert_headings(line):
    """Convert Markdown headings to HTML."""
    heading_match = re.match(r'^(#+)\s*(.*)', line)
    if heading_match:
        level = len(heading_match.group(1))  # Count the number of '#' characters
        title = heading_match.group(2).strip()
        return f"<h{level}>{title}</h{level}>"
    return None

def main():
    """Main function to check command-line arguments and file existence."""
    # Check the number of arguments
    if len(sys.argv) < 3:
        print_usage_and_exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    check_file_exists(input_file)

    # Read the Markdown file and convert to HTML
    with open(input_file, 'r') as file:
        lines = file.readlines()

    html_lines = []
    for line in lines:
        heading_html = convert_headings(line)
        if heading_html:
            html_lines.append(heading_html)

    # Write the HTML output to the output file
    with open(output_file, 'w') as file:
        for html_line in html_lines:
            file.write(html_line + "\n")

    # If everything is okay, just exit with status 0
    sys.exit(0)

if __name__ == "__main__":
    main()

