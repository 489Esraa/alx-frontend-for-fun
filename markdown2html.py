#!/usr/bin/python3
'''
A script that converts markdown to HTML
'''
import sys
import os
import re

if __name__ == '__main__':

    # Test that the number of arguments passed is 2
    if len(sys.argv[1:]) != 2:
        print('Usage:./markdown2html.py README.md README.html',
              file=sys.stderr)
        sys.exit(1)

    # Store the arguments into variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Checks that the markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    ol_opened = False  # Flag to track if we've started an ordered list
    ul_opened = False  # Flag to track if we've started an unordered list
    with open(input_file, encoding='utf-8') as file_1:
        html_content = []
        md_content = [line[:-1] for line in file_1.readlines()]
        for line in md_content:
            heading = re.split(r'#{1,6} ', line)
            if len(heading) > 1:
                # Compute the number of the # present to
                # determine heading level
                h_level = len(line[:line.find(heading[1])-1])
                # Append the html equivalent of the heading
                html_content.append(
                    f'<h{h_level}>{heading[1]}</h{h_level}>\n'
                )
                ol_opened = ul_opened = False  # Reset flags when exiting a heading
            elif line.strip().startswith(('1.', '2.', '3.')):  # Check for ordered list items
                if not ol_opened:
                    html_content.append('<ol>\n')  # Start ordered list
                    ol_opened = True
                    ul_opened = False  # Ensure no unordered list is opened
                html_content.append(f'<li>{line[2:]}</li>\n')
            elif line.startswith('- '):  # Check for unordered list items
                if not ul_opened:
                    html_content.append('<ul>\n')  # Start unordered list
                    ul_opened = True
                    ol_opened = False  # Ensure no ordered list is opened
                html_content.append(f'<li>{line[2:]}</li>\n')
            else:
                html_content.append(line)
                if ul_opened:
                    # End unordered list if necessary
                    html_content.append('</ul>\n')
                    ul_opened = False
                if ol_opened:
                    # End ordered list if necessary
                    html_content.append('</ol>\n')
                    ol_opened = False

    with open(output_file, 'w', encoding='utf-8') as file_2:
        file_2.writelines(html_content)
