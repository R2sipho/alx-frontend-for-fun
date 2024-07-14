#!/usr/bin/python3
"""
A script to convert a Markdown file into an HTML file.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: The path to the Markdown file to be converted.
    output_file: The path where the output HTML file will be saved.

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import pathlib
import re
import sys

def convert_md_to_html(input_file, output_file):
    """
    Converts the contents of a Markdown file to HTML and saves it to the specified output file.

    Args:
        input_file (str): The path to the input Markdown file.
        output_file (str): The path to the output HTML file.
    """

    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    in_list = False  

    for line in md_content:
        match = re.match(r'^(#{1,6}) (.*)', line)
        if match:
            h_level = len(match.group(1))  
            h_content = match.group(2)     
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')  

        elif re.match(r'^\* (.*)', line):
            if not in_list:
                html_content.append('<ul>\n')  
                in_list = True
            item_content = re.sub(r'^\* ', '', line)  
            html_content.append(f'  <li>{item_content}</li>\n')  

        elif re.match(r'^\d+\. (.*)', line):
            if not in_list:
                html_content.append('<ol>\n')  
                in_list = True
            item_content = re.sub(r'^\d+\. ', '', line)  
            html_content.append(f'  <li>{item_content}</li>\n')  

        else:
            if in_list:
                html_content.append('</ul>\n' if re.match(r'^\* ', line) else '</ol>\n')
                in_list = False
            html_content.append(line)  
    
    if in_list:
        html_content.append('</ul>\n')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a Markdown file to an HTML file.')
    parser.add_argument('input_file', help='Path to the Markdown file to be converted.')
    parser.add_argument('output_file', help='Path to save the resulting HTML file.')
    args = parser.parse_args()

    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Error: The file "{input_path}" does not exist.', file=sys.stderr)
        sys.exit(1)

    convert_md_to_html(args.input_file, args.output_file)

