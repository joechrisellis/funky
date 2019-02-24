"""Provides utility methods for finding and recursively importing files."""

import os

from funky.imports import FunkyImportError, libs_directory
from funky.parse import FunkyParsingError, FunkyLexingError, FunkySyntaxError
from funky.parse.funky_parser import FunkyParser

def get_imported_declarations(imports, search_paths):
    """Given a list of imports and a list of paths to search for them in,
    return a list of declarations containing the imported declarations. The
    returned list of declarations can then be prepended to the the declarations
    in the input file. This function will recursively import if required.
    
    :param imports [str]:      a list of imports -- these are relative paths to
                               .fky files
    :param search_paths [str]: a list of paths to use as the 'base path' when
                               searching for imports -- i.e if the user
                               supplies 'test.fky' as an import and ['/libs',
                               '/var'] as a search path, we will try to import
                               '/libs/test.fky' first, and failing that try to
                               import '/var/test.fky'
    :return:                   a list of declarations from the imported files
    """

    decls, imported = [], set()
    parser = FunkyParser()
    parser.build()

    def do_import(imp):
        if imp in imported: return

        filename = search_for_import(imp, search_paths)
        imported.add(filename)
        with open(filename, "r") as f:
            source = f.read()

        parsed = parser.do_parse(source)
        for sub_imp in parsed.body.imports:
            do_import(sub_imp)
        decls.extend(parsed.body.toplevel_declarations)

    for imp in imports:
        do_import(imp)

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

    raise FunkyImportError("Cannot find import '{}'.".format(import_name))
