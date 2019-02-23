from funky import FunkyError

from pkg_resources import resource_filename
libs_directory = resource_filename("funky", "libs/")

class FunkyImportError(FunkyError):
    """Raised when importing code failed."""
    pass
