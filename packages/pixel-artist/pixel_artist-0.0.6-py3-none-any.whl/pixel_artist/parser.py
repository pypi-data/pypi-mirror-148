"""Parsing utility functions to read and validate command line arguments."""

import sys
from argparse import ArgumentParser

from .constants import RGB, LAB


def build_parser() -> ArgumentParser:
    """
    Builds a parser that can read command ine arguments.

    Returns:
        An ArgumentParser instance initialized with the accepted command line arguments structure.
    """

    parser = ArgumentParser(description='Pixel art tool to generate images with pixelated effects.')
    parser.add_argument("-f", "--filename", nargs=1, help="input filename", required=True)
    parser.add_argument("-p", "--nbits", nargs=1, help="number of bits of the palette, default=24",
                        choices=[3, 8, 9, 24], type=int, default=[24])
    parser.add_argument("-n", "--ncolors", nargs=1, help="number of colors to use: 1-256, default=256", type=int,
                        default=[256])
    parser.add_argument("-g", "--granularity", nargs=1,
                        help="granularity to be used (>0): a bigger value means bigger blocks, default=1", type=int,
                        default=[1])
    parser.add_argument("-l", "--lab", help="use *lab model, default=rgb", action='store_true', default=False)
    parser.add_argument("-v", "--verbose", help="show progress", action='store_true', default=False)
    parser.add_argument("-s", "--save", help="save the output image", action='store_true', default=False)

    return parser


def validate_args(parser: ArgumentParser, args: dict) -> dict:
    """
    Validates the parsed arguments and either returns the validated arguments or aborts the execution of the program,
    issuing an help message.

    Args:
      parser: An ArgumentParser instance initialized with command line definitions. Only used to print the help message,
      in case of invalid input arguments.
      args: A dict containing the parsed arguments to be validated.

    Returns:
        A dict containing all the validated arguments.
    """
    filename = args['filename'][0]
    nbits = args['nbits'][0]
    ncolors = args['ncolors'][0]
    granularity = args['granularity'][0]
    color_space = RGB if not args['lab'] else LAB
    verbose = args["verbose"]
    save = args["save"]

    valid = True
    error_msg = ""
    if filename.split(".")[-1] == "png":
        error_msg = "File format not supported. Try with a .jpg"
        valid = False
    elif ncolors < 1 or ncolors > 256:
        error_msg = "Number of colors should be an integer between 1 and 256"
        valid = False
    elif granularity < 1:
        error_msg = "Granularity should be number greater or equal to 1"
        valid = False
    if not valid:
        if error_msg:
            sys.stdout.write(error_msg)
        parser.print_help()
        sys.exit()

    validated_args = {
        "filename": filename,
        "nbits": nbits,
        "ncolors": ncolors,
        "granularity": granularity,
        "color_space": color_space,
        "verbose": verbose,
        "save": save
    }
    return validated_args


def parse_args(parser: ArgumentParser) -> dict:
    """
    Parses the command line arguments and validates them against the allowed rules.

    Args:
      parser: An ArgumentParser instance initialized and ready to be used.

    Returns:
        A dict containing all the parsed and validated arguments.

    """
    args = vars(parser.parse_args())
    args = validate_args(parser, args)
    return args
