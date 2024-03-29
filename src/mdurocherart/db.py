import logging

import requests
from typing import Dict, List
from flask import app

from mdurocherart.errors import JavaScriptCompilationError, NotFoundError, BadRequestError


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

    def init_app(self, app: app.Flask):
        app.couchdb = self


    @classmethod
    def from_flask_config(cls, flask_app: app.Flask):
        """
        Init method for flask config objects as opposed to directly inputting each argument.
        Parameters
        ----------
        flask_app: app.Flask
            flask app in use.

        Returns
        -------
            A class instance of the CouchdbConnection.
        """
        config = flask_app.config
        user = config.get('COUCHDB_USERNAME')
        password = config.get('COUCHDB_PASSWORD')
        database = config.get('COUCHDB_DATABASE')
        host = config.get('COUCHDB_HOST')
        port = config.get('COUCHDB_PORT')
        return cls(user=user, password=password, database=database, host=host, port=port)

    @property
    def end_point(self):
        return "http://" + self.user + ":" + self.password + "@" + self.host + ":" + self.port + "/" + self.database

    def get_revision(self, document: str, data: Dict = None, design_doc: bool = False) -> str:
        """
        Function to get the current revision of the document
        Parameters
        ----------
        document: str
            The document we want to get the latest revision id from.
        data: Dict, default: None
            The payload being sent to the end point, if no payload is given
            the function returns the revision id as a string as opposed to
            updating the data dict.
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

        if "_rev" in response.keys() and data:
            data.update({"_rev": response["_rev"]})
            return data
        elif data:
            return data
        elif "_rev" in response.keys():
            return {"_rev": response["_rev"]}

        return None

    def get_view(self, document: str, view: str, keys: str | List[str] = None) -> Dict:
        """
        The get_view method takes a document and view name and returns the output of the view input.
        Parameters
        ----------
        document: str
            This is the name of the design document that holds the view requested.
        view: str
            This is the name of the view requested, this must be defined beforehand.
        keys: Dict[str, str | List[str]]
            This is a dictionary with key value pairs for couch db to interpret.
        Returns
        -------
        response: Dict
            The response returns the views outputs.
        """
        end_point = self.end_point + "/_design/" + document + "/_view/" + view

        if keys:
            end_point += "?key=" + _format_keys(keys)

        response = requests.get(url=end_point)
        response_dict = response.json()
        if response.status_code == 404:
            raise NotFoundError(
                error=response_dict['error'],
                reason=response_dict['reason'],
                status_code=response.status_code,
                request=end_point,
            )
        elif response.status_code == 400:
            raise BadRequestError(
                error=response_dict['error'],
                reason=response_dict['reason'],
                status_code=response.status_code,
                request=end_point,
            )
        return response_dict

    def put_view(self, document: str, view: Dict[str, str]) -> Dict:
        """
        The put_view method takes a document, view name and a view_map then forms a
        payload for updating the design doc. It will also check if the doc already exists
        and retrieve the revision id before updating it.
        Parameters
        ----------
        document: str
            This is the name of the design document that holds the view requested.
        view: str
            This is the name of the view requested, and its map & reduce functions attached,
            this must be defined beforehand. If there are errors in syntax error will be returned.

        Returns
        -------
        Response: Dict
            This is the response JSON from the put request.
        """
        payload = {
            "views": view
        }
        payload = self.get_revision(document=document, design_doc=True, data=payload)
        end_point = self.end_point + "/_design/" + document
        response = requests.put(url=end_point, json=payload)
        response_dict = response.json()
        if response.status_code == 404:
            raise NotFoundError(
                error=response_dict['error'],
                reason=response_dict['reason'],
                status_code=response.status_code,
                request=end_point,
            )
        elif response.status_code == 400:
            raise BadRequestError(
                error=response_dict['error'],
                reason=response_dict['reason'],
                status_code=response.status_code,
                request=end_point,
            )

        return response_dict

    def post_document(self, data: Dict) -> Dict:
        """
        Post document takes a dictionary of data (which will be coerced to json) and creates
        a new document with it. If you want to specify an id use `put_document`.
        Parameters
        ----------
        data: Dict
            Data to be stored in the couchdb database.

        Returns
        -------
        response_payload: Dict
            This payload contains information about the upload, whether it was successful,
            the id of the document and the revision of the document.
        """

        endpoint = self.end_point
        response = requests.post(endpoint, json=data).json()
        return response

    def put_document(self, document_id: str, data: Dict) -> Dict:
        """
        Post document takes a document_id and dictionary of data (which will be coerced to json) and creates/updates
        a document with it. If you don't want to specify an id and create a new document use `post_document`.
        Parameters
        ----------
        document_id: str
            The id of the document you want to create/update.
        data: Dict
            Data to be stored in the couchdb database.

        Returns
        -------
        response_payload: Dict
            This payload contains information about the upload, whether it was successful,
            the id of the document and the revision of the document.
        """
        data = self.get_revision(document=document_id, design_doc=False, data=data)
        end_point = self.end_point + "/" + document_id
        response = requests.put(end_point, json=data).json()

        return response

    def delete_document(self, document_id: str) -> Dict:
        """
        Takes a document_id to identify the document required then deletes it using that document_id.

        Parameters
        ----------
        document_id: str
            The id of the document you want to create/update.
        Returns
        -------
        response_payload: Dict
            This payload contains information about the upload, whether it was successful,
            the id of the document and the revision of the document.
        """
        end_point = self.end_point + "/" + document_id
        revision = self.get_revision(document=document_id, design_doc=False)
        if revision:
            end_point += "?rev=" + revision['_rev']

        response = requests.delete(end_point)
        if response.status_code == 404:
            if response["error"] == "not_found":
                msg = f"""Couchdb returned {response["reason"]}, as there was an issue finding the document: 
                {document_id} please ensure these exist in couch db.
                """
                raise NotFoundError(msg=msg)

        return response.status_code, response.json()



def _format_keys(keys: str | List[str]):

    if isinstance(keys, str):
        return _jsonify_string(keys)
    else:
        keys = map(_jsonify_string, keys)
        return "[" + ",".join(keys) + "]"


def _jsonify_string(string: str):
    return "%22" + string + '%22'
