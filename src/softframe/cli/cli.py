"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mml_api` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``ml_api.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``ml_api.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import getopt
import sys
from time import time

from softframe.misc.routines import read_and_convert


def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code
    """
    print('-' * 20 + " Executing " + "-" * 20)
    t0 = time()

    # Put routines here.

    try:
        opts, args = getopt.getopt(argv, "hi:o:d:", ["ifile=", "ofile="])

    except getopt.GetoptError:
        print('usage: python -m cli -i <inputfile> -o <outputfile> -d <file_dir> -a')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('usage: python -m cli -i <inputfile> -o <outputfile> -d <file_dir> -a')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            pass
        elif opt in ("-o", "--ofile"):
            pass
        elif opt == '-d':
            if not isinstance(arg, str):
                print("With -d option <file_dir> string should be given")
                sys.exit()

            read_and_convert(arg)

    t0 = time() - t0
    print("Finished execution in %.4fs" % t0)

    return 0
