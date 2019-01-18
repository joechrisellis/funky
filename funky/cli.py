import argparse
import logging
import time

import funky.compiler as compiler

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", type=argparse.FileType("w"),
                        required=True,
                        help="File to write compiled program to.")
    parser.add_argument("--dump-parsed", default=False, required=False,
                        action="store_true",
                        help="Dump the parse tree to stdout.")
    parser.add_argument("--dump-renamed", default=False, required=False,
                        action="store_true",
                        help="Dump the renamed parse tree to stdout.")
    parser.add_argument("--dump-desugared", default=False, required=False,
                        action="store_true",
                        help="Dump the core (desugared) funky code to stdout.")
    parser.add_argument("input", type=argparse.FileType("r"),
                        help="Input program (funky source).")

    args = parser.parse_args()

    lines = args.input.readlines()
    log.info("Will compile {}, with {} lines.".format(args.input.name,
                                                          len(lines)))
    source = "\n".join(lines)

    start = time.time()
    log.info("Started compilation at UNIX timestamp {}.".format(start))
    output = compiler.compile_to_c(source, dump_parsed=args.dump_parsed,
                                           dump_renamed=args.dump_renamed,
                                           dump_desugared=args.dump_desugared)
    finish = time.time()
    log.info("Finished compilation at UNIX timestamp {}.".format(finish))
    log.info("Compilation completed in {} seconds.".format(finish - start))

def start():
    """Exists only for setuptools."""
    log.debug("Funky compiler started via command-line.")
    main()

if __name__ == "__main__":
    log.debug("Funky compiler started.")
    main()
