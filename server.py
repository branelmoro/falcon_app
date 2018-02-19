import falcon

class resource:

	on_get(req, resp):
		resp.body = "here it is"


def create():
    api = falcon.API()
    api.add_route('/', resource()) 
    return api

api = create()



# for TDD

from falcon import testing
import pytest
from app import create


@pytest.fixture(scope='module')
def client():
    return testing.TestClient(create())

def test_get_message(client):
    result = client.simulate_get('/')
    assert result.status_code == 200