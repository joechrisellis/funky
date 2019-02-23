"""Handles importing."""

import os

from funky.imports import FunkyImportError, libs_directory
from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.parse.funky_parser import FunkyParser

# list of locations to search for imported files 
SEARCH_PATHS = [libs_directory]

def create_imports_source(imports):
    print("!! creating import")
    parser = FunkyParser()
    parser.build()

    decls = []
    for imp in imports:
        source = get_import_source(imp)
        parsed = parser.do_parse(source)
        decls.extend(parsed.body.toplevel_declarations)

    return decls

def get_import_source(import_name, search_paths=SEARCH_PATHS):
    filename = search_for_import(import_name, search_paths=search_paths)
    with open(filename, "r") as f:
        return f.read()

def search_for_import(import_name, search_paths=SEARCH_PATHS):
    for search_path in search_paths:
        candidate_path = os.path.join(search_path, import_name)
        try:
            with open(candidate_path, "r") as f:
                return candidate_path
        except FileNotFoundError:
            pass

    raise FunkyImportError("Cannot find import '{}'.".format(import_name))
