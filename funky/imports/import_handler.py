"""Provides utility methods for finding and recursively importing files."""

import logging
import os

from funky.imports import FunkyImportError, libs_directory
from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.parse.funky_parser import FunkyParser

log = logging.getLogger(__name__)

SEARCH_PATHS = [libs_directory]

def get_imported_declarations(base_path, imports, imported=None):
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
    log.info("Finding declarations for imports '{}' relative to {}.".format(
        ", ".join(imports), base_path
    ))

    if imported is None:
        imported = set([base_path])
    else:
        log.debug("'{}' already imported.".format(", ".join(imported)))
        imported.add(base_path)

    base_path = os.path.abspath(base_path) # just in case...
    if not os.path.isdir(base_path):
        base_dir = os.path.dirname(base_path)
    else:
        log.debug("Base path is a directory; you are probably running the REPL.")
        base_dir = base_path

    decls = []

    log.debug("Building parser to read imported source files...")
    parser = FunkyParser()
    parser.build()
    log.debug("Done building parser.")

    def do_import(base_dir, imp):
        filename = search_for_import(imp, [base_dir] + SEARCH_PATHS)
        if filename in imported: return
        imported.add(filename)

        with open(filename, "r") as f:
            source = f.read()

        parsed = parser.do_parse(source)
        for sub_imp in parsed.body.imports:
            log.debug("Found more imports, handling them.")
            new_base_dir = os.path.dirname(filename)
            do_import(new_base_dir, sub_imp)

        decls.extend(parsed.body.toplevel_declarations)

    for imp in imports:
        do_import(base_dir, imp)

    log.info("Found all imported declarations.")
    return decls

def search_for_import(import_name, search_paths):
    """Given a user-provided import and a priority-ordered list of search
    paths, gives the first path where the import can be found.
    
    :param import_name str:    the name of the import as given by the user
    :param search_paths [str]: a priority-ordered list of search paths
    :return:                   the path where the desired import can be found
    """
    log.info("Searching for import '{}' in '{}'.".format(
        import_name, ", ".join(search_paths)
    ))

    for search_path in search_paths:
        log.debug("Searching in '{}'...".format(search_path))
        candidate_path = os.path.join(search_path, import_name)
        try:
            with open(candidate_path, "r") as f:
                log.debug("Found match: '{}'".format(candidate_path))
                return candidate_path
        except FileNotFoundError:
            pass
        log.debug("No match found in '{}'.".format(search_path))

    log.debug("No matches found -- import failed, raising error.")
    if len(search_paths) >= 2:
        tried_paths_str = ", ".join(search_paths[:-1])
        tried_paths_str += ", and {}".format(search_paths[-1])
    else:
        tried_paths_str = search_paths[0]
    raise FunkyImportError("Cannot find import '{}'.\n"
                           "I tried looking in {}".format(import_name,
                                                          tried_paths_str))
