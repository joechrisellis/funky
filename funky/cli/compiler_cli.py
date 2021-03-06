"""Command line interface for the main compiler."""

import argparse
import logging
import time

from funky._version import __version__

import funky.globals
from funky.cli.verbosity import set_verbosity
import funky.compiler as compiler

log = logging.getLogger(__name__)

def main():
    funky.globals.CURRENT_MODE = funky.globals.Mode.COMPILER

    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action="version",
                        version='%(prog)s {version}'.format(version=__version__),
                        help="Output %(prog)s's version and quit.")
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Be verbose. You can stack this flag, i.e. -vvv.")
    parser.add_argument('-q', '--quiet', action='count', default=0,
                        help="Be quiet. You can stack this flag, i.e. -qqq.")

    parser.add_argument('-u', '--no-unicode', action='store_true',
                        help="Do not use unicode characters in output (for old "
                             "terminals).")
    parser.add_argument('-c', '--no-colors', action='store_true',
                        help="Do not use coloured output (for boring people).")
    parser.add_argument('-e', '--show-exception-traces', action='store_true',
                        help="Show full exception traces.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", "-o", metavar="output_filename",
                       help="File to write compiled program to.")
    group.add_argument("--execute", "-x", action="store_true",
                        help="Do not create an output file, execute directly.")

    parser.add_argument("--dump-pretty", default=False, required=False,
                        action="store_true",
                        help="Dump the prettified source code to stdout with "
                             "syntax highlighting.")
    parser.add_argument("--dump-lexed", default=False, required=False,
                        action="store_true",
                        help="Dump the lexed (disambiguated) source code to stdout.")
    parser.add_argument("--dump-parsed", default=False, required=False,
                        action="store_true",
                        help="Dump the parse tree to stdout.")
    parser.add_argument("--dump-imports", default=False, required=False,
                        action="store_true",
                        help="Dump the parse tree (with imports included) to "
                             "stdout.")
    parser.add_argument("--dump-renamed", default=False, required=False,
                        action="store_true",
                        help="Dump the renamed parse tree to stdout (alongside "
                             "renamer mapping for top-level objects).")
    parser.add_argument("--dump-desugared", default=False, required=False,
                        action="store_true",
                        help="Dump the core (desugared) funky code to stdout.")
    parser.add_argument("--dump-types", default=False, required=False,
                        action="store_true",
                        help="Dump the types of all top-level objects in the "
                             "core tree to stdout.")
    parser.add_argument("--dump-generated", default=False, required=False,
                        action="store_true",
                        help="Dump the generated code to stdout.")

    parser.add_argument("--target", choices=compiler.targets.keys(),
                        help="The target language for compilation (choose "
                             "'intermediate' if you want to output the "
                             "intermediate code as a serialised Python "
                             "object).")
    parser.add_argument("input", type=argparse.FileType("r"),
                        help="Input program (funky source).")

    args = parser.parse_args()

    funky.globals.USE_UNICODE           = not args.no_unicode
    funky.globals.USE_COLORS            = not args.no_colors
    funky.globals.SHOW_EXCEPTION_TRACES = args.show_exception_traces

    if not (args.execute or args.target):
        print("Please specify a target, e.g. --target=python")
        exit(1)

    args.target = args.target if args.target else "python"

    verbosity = args.verbose - args.quiet
    set_verbosity(verbosity)

    log.info("Will compile {}.".format(args.input.name))

    start = time.time()
    log.info("Started compilation at UNIX timestamp {}.".format(start))
    output = compiler.compile_file(args.input, dump_pretty=args.dump_pretty,
                                               dump_lexed=args.dump_lexed,
                                               dump_parsed=args.dump_parsed,
                                               dump_imports=args.dump_imports,
                                               dump_renamed=args.dump_renamed,
                                               dump_desugared=args.dump_desugared,
                                               dump_types=args.dump_types,
                                               dump_generated=args.dump_generated,
                                               target=args.target)
    finish = time.time()
    log.info("Finished compilation at UNIX timestamp {}.".format(finish))
    log.info("Compilation completed in {0:.3f} seconds.".format(finish - start))

    # if the user wants to write to an output file, do that.
    # otherwise, just execute the code we were given.
    if args.output:
        mode = "w" if type(output) == str else "wb"
        with open(args.output, mode) as output_file:
            output_file.write(output)
            log.info("Written target code to {}.".format(args.output))
            print("Compilation completed in {0:.3f} seconds.".format(finish - start))
            print("Success, compiled program written to "
                  "{}.".format(args.output))
    else:
        exec(output, {"__name__" : "__main__"})

def start():
    """Exists only for setuptools."""
    main()

if __name__ == "__main__":
    main()
