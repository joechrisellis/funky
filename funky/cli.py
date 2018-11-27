import argparse

import compiler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", type=argparse.FileType("w"),
                        required=True,
                        help="File to write compiled program to.")
    parser.add_argument("input", type=argparse.FileType("r"),
                        help="Input program (funky source).")

    args = parser.parse_args()

    source = "\n".join(args.input.readlines())
    output = compiler.compile_to_c(source)

if __name__ == "__main__":
    main()
