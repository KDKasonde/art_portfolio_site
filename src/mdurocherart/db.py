import requests
from typing import Tuple, Dict
from json import loads, dumps

from errors import JavaScriptCompilationError, ViewNotFoundError


class CouchdbConnection:
    """
    This class is meant to set up and tear down the connection to a couch db
    instance.
    """
    def __init__(self, user: str, password: str, database: str, host: str = '127.0.0.1', port: int = 5984):
        """

        Parameters
        ----------
        user: str
            Database User.
        password: str
            Auth for the defined user.
        database: str
            Database name connection is for.
        host: str, default: '127.0.0.1'
            The host IP address for the couchdb instance.
        port: int, default: 5984
            The port the couchdb instance is connected to.
        """
        self.user = user
        self.password = password
        self.database = database
        self.port = str(port)
        self.host = host

    @property
    def end_point(self):
        return "http://" + self.user + ":" + self.password + "@" + self.host + ":" + self.port + "/" + self.database

    def get_revision(self, document: str, design_doc: bool = False) -> str:
        """
        Function to get the current revision of the document
        Parameters
        ----------
        document: str
            The document we want to get the latest revision id from.
        design_doc: bool, default: False
            A bool denoting whether the document is a design document.
        Returns
        -------
        revision_id: str
            The revision id of the document requested.
        """
        if design_doc:
            end_point = self.end_point + "/_design/" + document
        else:
            end_point = self.end_point + "/" + document
        response = requests.get(url=end_point).json()
        if "error" in response.keys():
            if response["error"] == "not_found":
                msg = f"""Couchdb returned {response["reason"]}, as there was an issue finding the document: {document}, please ensure it exists in couch db.
                """
                raise ViewNotFoundError(msg=msg)
        if "_rev" in response.keys():
            return response
        else:
            return None

    def get_view(self, design_document: str, view: str) -> Dict:
        """
        The get_view method takes a design_document and view name and returns the output of the view input.
        Parameters
        ----------
        design_document: str
            This is the name of the design document that holds the view requested.
        view: str
            This is the name of the view requested, this must be defined beforehand.
        Returns
        -------
        response: Dict
            The response returns the views outputs.
        """
        end_point = self.end_point + "/_design/" + design_document + "/_view/" + view
        response = requests.get(url=end_point).json()
        if "error" in response.keys():
            if response["error"] == "not_found":
                msg = f"""Couchdb returned {response["reason"]}, as there was an issue finding the document: {design_document} and view: {view}, please ensure these exist in couch db.
                """
                raise ViewNotFoundError(msg=msg)
        return response

    def put_view(self, design_document: str, view: str, mapping: str) -> Dict:
        """
        The put_view method takes a design_document, view name and a view_map then forms a
        payload for updating the design doc. It will also check if the doc already exists
        and retrieve the revision id before updating it.
        Parameters
        ----------
        design_document: str
            This is the name of the design document that holds the view requested.
        view: str
            This is the name of the view requested, this must be defined beforehand.
        mapping: str
            This is the map the view should provide. Written in JavaScript syntax.

        Returns
        -------
        Response: Dict
            This is the response JSON from the put request.
        """
        revision_payload = self.get_revision(document=design_document, design_doc=True)
        end_point = self.end_point + "/_design/" + design_document
        if "_rev" in revision_payload.keys():
            payload = dumps(
                {
                    "_rev": revision_payload["_rev"],
                    "views": {
                        view: {
                            "map": mapping
                        }
                    }
                }
            )
        else:
            payload = dumps(
                {
                    "views": {
                        view: {
                            "map": mapping
                        }
                    }
                }
            )
        response = requests.put(url=end_point, data=payload).json()
        if "error" in response.keys():
            if response["error"] == "compilation_error":
                raise JavaScriptCompilationError(msg=response["reason"])

        return response
