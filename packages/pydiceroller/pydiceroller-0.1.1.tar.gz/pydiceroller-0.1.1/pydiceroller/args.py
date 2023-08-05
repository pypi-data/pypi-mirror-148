"""
pygitscrum argparse gestion
"""

import argparse
import sys
from argparse import RawTextHelpFormatter



def compute_args():
    """
    check args and return them
    """
    my_parser = argparse.ArgumentParser(
        description="""
Synopsis : minimal dice roller
        """,
        epilog="""
Full documentation at: <https://github.com/thib1984/pydiceroller>
Report bugs to <https://github.com/thib1984/pydiceroller/issues>
MIT Licence
This is free software: you are free to change and redistribute it
There is NO WARRANTY, to the extent permitted by law
Written by thib1984."""
        , formatter_class=RawTextHelpFormatter
    )  
    my_parser.add_argument(
        "dices",
        metavar="dices",
        type=str,
        nargs="*",
        help="dices, with format example : 6, D6, 2D10, S3D10 (for sum), 2S2D6 -can give one or more parameters-",
    ) 
    my_parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="self-update, alternatively, use pip(3) install --upgrade pydiceroller for manual update",
    ), 
    my_parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="minimal output, use for pip commands",
    ),
    my_parser.add_argument(
        "-i",
        "--infinite",
        action="store_true",
        help="press entry to relaunch same dices, ctrl-c to exit",
    ),                        

    args = my_parser.parse_args()
    return args
