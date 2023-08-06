'''
Create an argument parser using argparse

Functions:
    get_parser() -> parser
'''

import argparse

def get_parser():
    ''''Create a parser object specific to networker'''
    parser = argparse.ArgumentParser(
        "networker",
        description=
        "networker:  a python package to generate and analyse protein similarity networks.",
        epilog="Written by Dr. Thom Booth, 2022."
        )
    parser.add_argument(
        '-f',
        '--faa',
        nargs='?',
        default=None,
        help='path to a fasta file containing amino acid sequences'
        )
    parser.add_argument(
        '-t',
        '--tsv',
        nargs='?',
        default=None,
        help='path to a .tsv containing BLASTP results'
        )
    parser.add_argument(
        '-n',
        '--node',
        nargs='?',
        default=None,
        help='the name of a node for subnetwork analysis'
        )
    parser.add_argument(
        '-th',
        '--threshold',
        type=float,
        nargs='?',
        default=None,
        help='custom identity threshold'
        )
    return parser
