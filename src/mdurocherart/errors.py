class Error(Exception):
    """
    Base class for all error messages for couch db.
    """
    def __init__(self, error, reason, status_code, request, request_body=None):
        self.error = error
        self.reason = reason
        self.status_code = status_code
        self.request = request
        if request_body:
            self.request_body = request_body
        fmt = {'error': self.error, 'status_code': self.status_code, 'reason': self.reason}
        self._full_msg = '{error} {status_code}: {reason}'.format(**fmt)

    def __str__(self) -> str:
        return self._full_msg


class InterfaceError(Error):
    """
    Class for all errors related to the interface created for couchdb.
    """


class DatabaseError(Error):
    """
    Class for all errors related to the database itself.
    """


class JavaScriptCompilationError(DatabaseError):
    """
    This error is raised when the javascript given as part of a map has a syntax error.
    """


class NotFoundError(DatabaseError):
    """
    This error is raised when a get request to unknown view, document or database is requested.
    """


class ServiceUnavailableError(DatabaseError):
    """
    This error is raised when a get request to unknown document is requested.
    """


class BadRequestError(InterfaceError):
    """
    This error is for when the request made is badly formatted
    """