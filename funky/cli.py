import argparse
import logging
import time

from funky._version import __version__
import funky.compiler as compiler

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="How much noise should the compiler make?")
    parser.add_argument('-V', '--version', action="version",
                        version='%(prog)s {version}'.format(version=__version__),
                        help="Output the compiler version and quit.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", "-o", type=argparse.FileType("w"),
                        help="File to write compiled program to.")
    group.add_argument("--execute", "-x", action="store_true",
                        help="Do not create an output file, execute directly.")

    parser.add_argument("--dump-lexed", default=False, required=False,
                        action="store_true",
                        help="Dump the lexed source code to stdout.")
    parser.add_argument("--dump-parsed", default=False, required=False,
                        action="store_true",
                        help="Dump the parse tree to stdout.")
    parser.add_argument("--dump-renamed", default=False, required=False,
                        action="store_true",
                        help="Dump the renamed parse tree to stdout.")
    parser.add_argument("--dump-desugared", default=False, required=False,
                        action="store_true",
                        help="Dump the core (desugared) funky code to stdout.")
    parser.add_argument("--dump-types", default=False, required=False,
                        action="store_true",
                        help="Dump the types of all symbols in the core tree "
                             "to stdout.")
    parser.add_argument("--dump-generated", default=False, required=False,
                        action="store_true",
                        help="Dump the generated code to stdout.")
    parser.add_argument("--target", choices=compiler.targets.keys(),
                        help="The target language for compilation.")
    parser.add_argument("input", type=argparse.FileType("r"),
                        help="Input program (funky source).")

    args = parser.parse_args()

    if not (args.execute or args.target):
        print("Please specify a target, e.g. --target=python")
        exit(1)

    args.target = args.target if args.target else "python"

    verbosity_2_loglevel = {
        0  :  logging.WARNING,
        1  :  logging.INFO,
        2  :  logging.DEBUG,
    }

    # set the desired log level
    most_verbose = verbosity_2_loglevel[max(verbosity_2_loglevel)]
    desired_loglevel = verbosity_2_loglevel.get(args.verbose, most_verbose)
    logging.getLogger().setLevel(desired_loglevel)

    lines = args.input.readlines()
    log.info("Will compile {}, with {} lines.".format(args.input.name,
                                                          len(lines)))
    source = "".join(lines)

    start = time.time()
    log.info("Started compilation at UNIX timestamp {}.".format(start))
    output = compiler.compile(source, dump_lexed=args.dump_lexed,
                                      dump_parsed=args.dump_parsed,
                                      dump_renamed=args.dump_renamed,
                                      dump_desugared=args.dump_desugared,
                                      dump_types=args.dump_types,
                                      dump_generated=args.dump_generated,
                                      target=args.target)
    finish = time.time()
    log.info("Finished compilation at UNIX timestamp {}.".format(finish))
    log.info("Compilation completed in {} seconds.".format(finish - start))

    # if the user wants to write to an output file, do that.
    # otherwise, just execute the code we were given.
    if args.output:
        args.output.write(output)
        log.info("Written target code to {}.".format(args.output.name))
        print("Success, compiled program written to "
              "{}.".format(args.output.name))
    else:
        exec(output, {"__name__" : "__main__"})

def start():
    """Exists only for setuptools."""
    main()

if __name__ == "__main__":
    main()
