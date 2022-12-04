# Cli = command line interface
import sys

#from config import setup_logging

#setup_logging()

from gui_app import gui_main
from cli_app import cli_main

import logging

log = logging.getLogger(__name__)


def main():
    #log.info(' program start ')
    print("Start programu")

    args = sys.argv[1:]
    if args:
        cli_main(args)
    else:
        #cli_main('u')
        gui_main()


if __name__ == "__main__":
    main()
