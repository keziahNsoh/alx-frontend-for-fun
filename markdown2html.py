#!/usr/bin/python3
"""markdown2html.py

A script that converts Markdown files to HTML format. It checks for
the existence of the Markdown file and handles command-line arguments
appropriately.
"""

import sys
import os


def print_usage_and_exit():
    """Print usage instructions and exit with status 1."""
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)


def check_file_exists(filename):
    """Check if the given file exists."""
    if not os.path.exists(filename):
        print(f"Missing {filename}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to check command-line arguments and file existence."""
    # Check the number of arguments
    if len(sys.argv) < 3:
        print_usage_and_exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    check_file_exists(input_file)

    # If everything is okay, just exit with status 0
    sys.exit(0)


if __name__ == "__main__":
    main()
