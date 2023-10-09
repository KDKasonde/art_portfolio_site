from mdurocherart.db import CouchdbConnection
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

couchdb = CouchdbConnection(
    user=os.getenv('COUCHDB_USERNAME'),
    password=os.getenv('COUCHDB_PASSWORD'),
    database=os.getenv('COUCHDB_DATABASE'),
    host=os.getenv('COUCHDB_HOST', default='127.0.0.1'),
    port=os.getenv('COUCHDB_PORT', default=5984),
)

VIEWS_FOLDER = Path(__file__).parent
VIEWS = sorted(VIEWS_FOLDER.glob('**/*.txt'))
views = {}
for view in VIEWS:
    view_name = view.stem

    with open(file=view, mode='r') as file:
        mapping = file.read().strip()
    views[str(view_name)] = {'map': mapping}

couchdb.put_view(document='images', view=views)


