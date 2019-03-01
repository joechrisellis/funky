"""Provides utility methods for finding and recursively importing files."""

import os

from funky.imports import FunkyImportError, libs_directory
from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.parse.funky_parser import FunkyParser

SEARCH_PATHS = [libs_directory]

def get_imported_declarations(base_path, imports):
    """Given a list of imports and a list of paths to search for them in,
    return a list of declarations containing the imported declarations. The
    returned list of declarations can then be prepended to the the declarations
    in the input file. This function will recursively import if required.
    
    :param base_file str: the absolute path to the file we are currently
                          compiling
    :param imports [str]: a list of imports -- these are relative paths to
                          .fky files
    :return:              a list of declarations from the imported files
    """

    base_path = os.path.abspath(base_path) # just in case...
    base_dir = os.path.dirname(base_path)

    decls, imported = [], set([base_path])
    parser = FunkyParser()
    parser.build()

    def do_import(base_dir, imp):
        filename = search_for_import(imp, [base_dir] + SEARCH_PATHS)
        if filename in imported: return
        imported.add(filename)

        with open(filename, "r") as f:
            source = f.read()

        parsed = parser.do_parse(source)
        for sub_imp in parsed.body.imports:
            new_base_dir = os.path.dirname(filename)
            do_import(new_base_dir, sub_imp)
        decls.extend(parsed.body.toplevel_declarations)

    for imp in imports:
        do_import(base_dir, imp)

    return decls

def search_for_import(import_name, search_paths):
    """Given a user-provided import and a priority-ordered list of search
    paths, gives the first path where the import can be found.
    
    :param import_name str:    the name of the import as given by the user
    :param search_paths [str]: a priority-ordered list of search paths
    :return:                   the path where the desired import can be found
    """
    for search_path in search_paths:
        candidate_path = os.path.join(search_path, import_name)
        try:
            with open(candidate_path, "r") as f:
                return candidate_path
        except FileNotFoundError:
            pass

    if len(search_paths) >= 2:
        tried_paths_str = ", ".join(search_paths[:-1])
        tried_paths_str += ", and {}".format(search_paths[-1])
    else:
        tried_paths_str = search_paths[0]
    raise FunkyImportError("Cannot find import '{}'.\n"
                           "I tried looking in {}".format(import_name,
                                                          tried_paths_str))
