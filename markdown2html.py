#!/usr/bin/python3
"""
markdown2html.py

A script that converts Markdown files to HTML format. It checks for
the existence of the Markdown file and handles command-line arguments
appropriately.
"""

import sys
import os


def markdown_to_html(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        return 1

    with open(input_file, "r") as md_file:
        lines = md_file.readlines()

    html_lines = []
    in_list = False
    paragraph_lines = []

    for line in lines:
        line = line.rstrip()  # Remove trailing whitespace

        if line.startswith("#"):  # Handle headings
            if paragraph_lines:
                html_lines.append(f"<p>{'<br />'.join(paragraph_lines)}</p>")
                paragraph_lines = []
            level = line.count("#")
            content = line[level:].strip()
            html_lines.append(f"<h{level}>{content}</h{level}>")

        elif line.startswith("- "):  # Handle unordered list
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")

        elif line.startswith("* "):  # Handle ordered list
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")

        elif line.strip() == "":  # Handle empty line (end of a paragraph)
            if paragraph_lines:
                html_lines.append(f"<p>{'<br />'.join(paragraph_lines)}</p>")
                paragraph_lines = []
            if in_list:
                html_lines.append("</ul>")
                in_list = False

        else:  # Handle normal text
            paragraph_lines.append(line)

    # Finalize any remaining content
    if paragraph_lines:
        html_lines.append(f"<p>{'<br />'.join(paragraph_lines)}</p>")

    # Close any open list tags if still in a list
    if in_list:
        html_lines.append("</ul>")

    # Write to output file
    with open(output_file, "w") as html_file:
        html_file.write("\n".join(html_lines))

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    sys.exit(markdown_to_html(input_file, output_file))
