import pytest


get_view_request = [
    {
        'document': 'my_ddoc',
        'view': 'my_filter'
    }
]


@pytest.mark.conn_required
@pytest.mark.parametrize("payload", get_view_request)
def test_get_view(couch_db_app_conn, payload):
    couchdb = couch_db_app_conn
    response = couchdb.get_view(document=payload['document'], view=payload['view'])

    assert len(response['rows']) == 3


