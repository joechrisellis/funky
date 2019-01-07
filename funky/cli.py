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
    parser.add_argument("input", type=argparse.FileType("r"),
                        help="Input program (funky source).")

    args = parser.parse_args()

    lines = args.input.readlines()
    log.info("Will compile {}, with {} lines.".format(args.input.name,
                                                          len(lines)))
    source = "\n".join(lines)

    start = time.time()
    log.info("Started compilation at UNIX timestamp {}.".format(start))
    output = compiler.compile_to_c(source)
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
