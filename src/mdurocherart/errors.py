class Error(Exception):
    """
    Base class for all error messages for couch db.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class JavaScriptCompilationError(Error):
    """
    This error is raised when the javascript given as part of a map has a syntax error.
    """


class ViewNotFoundError(Error):
    """
    This error is raised when a get request to unknown view is requested.
    """