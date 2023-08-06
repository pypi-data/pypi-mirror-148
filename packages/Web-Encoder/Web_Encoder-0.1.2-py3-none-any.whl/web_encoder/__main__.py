import argparse
import sys

from .main import WebEncoder

PROGRAM = "WebEncoder"
USAGE = "python -m web_encoder [ e | d ] data [ --no-compress ]"
DESCRIPTION = """
------------------------------------------------------------------------------

Description:


This module was created to encode and decode data in a a web-friendly format.
Its use the urlsafe functions of the base64 standard library.

By default WebEncoder will try to compress the data.
To compress the data its use the function compress of zlib standard library.
If it manages to compress the data, the encoded data started with '.'.

If you prefer your data not to be compressed use the --no-compress flag.

------------------------------------------------------------------------------

Arguments:

"""
EPILOG = "Copyrights @CesarMerjan"


def get_parser(
    prog: str, usage: str, descrption: str, epilog: str
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        usage=usage,
        description=descrption,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
    )
    return parser


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "option",
        type=str,
        choices=("e", "d"),
        metavar="option",
        help="use 'e' to encode data and 'd' to decode data",
    )

    parser.add_argument(
        "data",
        type=str,
        metavar="data",
        help="the data in string format to be encoded or decoded",
    )

    parser.add_argument(
        "-n",
        "--no-compress",
        dest="compress",
        action="store_false",
        default=True,
        help="use to not compress data before encode",
    )


def main(args: argparse.Namespace) -> None:

    web_encoder = WebEncoder()

    if args.option == "e":
        result = web_encoder.encode(args.data, args.compress)
    else:
        result = web_encoder.decode(args.data)

    print(result)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.argv.append("--help")

    parser = get_parser(PROGRAM, USAGE, DESCRIPTION, EPILOG)
    add_arguments(parser)
    args = parser.parse_args()
    main(args)
