import logging

from flask import app, current_app, session, request, redirect, url_for
from functools import wraps
from hashlib import sha512
import bcrypt
USER_ID = 'Artist'


class LoginManager:
    """
    This object contains all verification methods for the artist to
    edit their works, remove, or upload new ones. This class is written
    with only one user in mind.
    """
    def __init__(self, username: str, password: str, rounds: int):
        self.username = username
        self.password = self.hash(password, rounds)
        self._session_identifier_generator = _create_identifier
        self._active_id = None

    @property
    def active_id(self):
        return self._active_id

    @active_id.setter
    def active_id(self, identifier: str):
        self._active_id = identifier

    @active_id.deleter
    def active_id(self):
        del self._active_id

    @staticmethod
    def hash(password: str, rounds: int):
        """
        This function salts and hashes strings for safer storage.
        Parameters
        ----------
        password: str
            This denotes the string we want to encode using bcrypt
        rounds: int
            the number of bcrypt rounds. (cost factor)
        Returns
        -------
        HashedString
            This functions returns the byte string which is the hashed
            string.
            This is the salt that the string is gets appended before
            hashing takes place.
        """
        byte_string = password.encode('utf-8')

        salt = bcrypt.gensalt(rounds=rounds)
        hashed_string = bcrypt.hashpw(byte_string, salt)

        return hashed_string

    def verify(self, username: str, password: bytes):
        if username != self.username:
            return False
        return bcrypt.checkpw(password=password, hashed_password=self.password)

    def verify_session_failed(self):
        """Checks session if user is logged in"""
        sess = session._get_current_object()
        ident = self._session_identifier_generator()

        if not sess:
            return True
        if ident != sess.get("_id", None) or self.active_id != sess.get("_id", None):
            for k in ['_id', '_fresh', "_remember_seconds", "_remember"]:
                sess.pop(k, None)

            sess["_remember"] = "clear"

            return True
        return False

    def unauthorised(self):
        return redirect(url_for('upload.home'))

    def init_app(self, flask_app):
        flask_app.login_manager = self


def login_user(fresh=True, remember=True, duration=None):
    session["_fresh"] = fresh
    session["_id"] = current_app.login_manager._session_identifier_generator()
    current_app.login_manager.active_id = session["_id"]
    if remember:
        session["_remember"] = "set"
        if duration is not None:
            try:
                # equal to timedelta.total_seconds() but works with Python 2.6
                session["_remember_seconds"] = (
                           duration.microseconds
                           + (duration.seconds + duration.days * 24 * 3600) * 10 ** 6
                   ) / 10.0 ** 6
            except AttributeError as e:
                raise Exception(
                    f"duration must be a datetime.timedelta, instead got: {duration}"
                ) from e

    return True


def _get_remote_addr():
    address = request.headers.get("X-Forwarded-For", request.remote_addr)
    if address is not None:
        # An 'X-Forwarded-For' header includes a comma separated list of the
        # addresses, the first address being the actual remote address.
        address = address.encode("utf-8").split(b",")[0].strip()
    return address


def _create_identifier():
    user_agent = request.headers.get("User-Agent")
    if user_agent is not None:
        user_agent = user_agent.encode("utf-8")
    base = f"{_get_remote_addr()}|{user_agent}"
    if str is bytes:
        base = str(base, "utf-8", errors="replace")  # pragma: no cover
    h = sha512()
    h.update(base.encode("utf8"))
    return h.hexdigest()


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):

        if current_app.login_manager.verify_session_failed():
            return current_app.login_manager.unauthorised()

        return current_app.ensure_sync(func)(*args, **kwargs)
    return decorated_view
