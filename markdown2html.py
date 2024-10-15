#!/usr/bin/python3

import sys
import os
import hashlib
import re


def print_usage_and_exit():
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)


def check_file_exists(filename):
    if not os.path.exists(filename):
        print(f"Missing {filename}", file=sys.stderr)
        sys.exit(1)


def markdown_to_html(markdown):
    lines = markdown.splitlines()
    html_lines = []
    in_list = False
    current_list_type = None

    for line in lines:
        line = line.rstrip()  # Remove trailing whitespace

        # Handle headings
        if line.startswith("#"):
            header_level = line.count("#")
            content = line[header_level:].strip()
            html_lines.append(f"<h{header_level}>{content}</h{header_level}>")
            continue

        # Handle unordered lists
        if line.startswith("- "):
            if current_list_type != "ul":
                if in_list:
                    html_lines.append("</ul>")
                html_lines.append("<ul>")
                in_list = True
                current_list_type = "ul"
            item = line[2:].strip()
            html_lines.append(f"<li>{item}</li>")
            continue

        # Handle ordered lists
        if line.startswith("* "):
            if current_list_type != "ol":
                if in_list:
                    html_lines.append("</ol>")
                html_lines.append("<ol>")
                in_list = True
                current_list_type = "ol"
            item = line[2:].strip()
            html_lines.append(f"<li>{item}</li>")
            continue

        # Close list if needed
        if in_list:
            if current_list_type == "ul":
                html_lines.append("</ul>")
            elif current_list_type == "ol":
                html_lines.append("</ol>")
            in_list = False
            current_list_type = None

        # Handle paragraphs and formatting
        if line.strip():  # Non-empty line
            line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"__(.*?)__", r"<em>\1</em>", line)
            line = re.sub(
                r"\[\[(.*?)\]\]",
                lambda m: hashlib.md5(m.group(1).encode()).hexdigest(),
                line,
            )
            line = re.sub(
                r"\(\(.*?c.*?\)\)",
                lambda m: m.group(0).replace("c", "").replace("C", ""),
                line,
            )
            html_lines.append(f"<p>{line}</p>")
        else:
            # Add a <br/> for empty lines between paragraphs
            if html_lines and not html_lines[-1].endswith("</p>"):
                html_lines.append("<br/>")

    # Close any open list at the end
    if in_list:
        if current_list_type == "ul":
            html_lines.append("</ul>")
        elif current_list_type == "ol":
            html_lines.append("</ol>")

    return "\n".join(html_lines)


def main():
    if len(sys.argv) < 3:
        print_usage_and_exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    check_file_exists(input_file)

    with open(input_file, "r") as f:
        markdown_content = f.read()

    html_content = markdown_to_html(markdown_content)

    with open(output_file, "w") as f:
        f.write(html_content)


if __name__ == "__main__":
    main()
