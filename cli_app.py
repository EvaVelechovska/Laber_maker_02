import argparse
import logging
import textwrap
from pathlib import Path

from inputs import csv_input, user_input
from outputs import to_word

log = logging.getLogger()


def cli_main(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Label maker
            ----------------------
                default to user input from console
                if you wish, you may specify input and template file
                input must be a csv file, output then a jinja formatted docx
            """
        ))

    parser.add_argument("data_input",
                        choices=["file", "user", "u"],
                        default="file",
                        const="file",
                        nargs="?")

    parser.add_argument(
        "-i",
        "--input-file",
        type=Path,
        default="input/sample_data.csv",
        const="input/sample_data.csv",
        nargs="?",
        help="specify input data csv file (defaults to: %(default)s)",
    )

    args = parser.parse_args(args)

    data = []
    data_input = args.data_input

    if data_input == "user" or data_input == "u":
        data = user_input()
    elif data_input == "csv":
        file_path = args.input_file
        data = csv_input(file_path)
    else:
        log.warning(f"neznám možnost vstupu: {data_input}")
        exit()
        # print("neznám")

    to_word(data, 'templates/labels_template.docx')
    log.info(' program end '.center(80, '-'))

    print("teď jsem v cli")
    print("tvoje argumenty jsou: ", args)
