"""
Entry point to convert pylint output txt to junit
"""
import sys
import argparse

from pylint2junit.parse import parse_input_lines
from pylint2junit.tojunit import pylint_to_junit

sys.path.append('')


def main():
    """
    Given input file of pylint output; converts to a junit XML file.

    Input file is expected to be --output-format=parseable or text from pylint.

    Example usage
    ```
    pylint --output-format=parseable --rcfile=pylintrc rf tests \
        > ./test-output/pylint_results.txt

    pylint2junit \
        --input=./test-output/pylint_results.txt \
        --output=./test-output/pylint_results.xml
    ```
    """
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-i', '--input',
        help='Path to input pylint file',
        required=True,
    )
    parser.add_argument(
        '-o', '--output',
        help='Path to output junit xml file',
        required=True,
    )
    pargs = parser.parse_args()

    with open(pargs.input, 'r') as input_file:
        input_lines = input_file.readlines()

    xml_str = pylint_to_junit(
        parse_input_lines(input_lines),
    )

    with open(pargs.output, 'w') as output_file:
        output_file.write(xml_str)

if __name__ == "__main__":
    main()
