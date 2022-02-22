import pytest

from app import create_app
from app.views import home, sign_generator
from config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    app.add_url_rule('/', view_func=home)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


# @pytest.mark.parametrize('data, result', [
#     ({'shop_order_id': '1010ytv', 'amount': '100', 'currency': 'eur', 'description': 'Qwerty'},
#      'f6282eaf294ea510b89bc52f9af007750a1d5adbab4b2f765c5249785a05de97'),
#     ({'shop_order_id': 'bgk1xnasoq', 'amount': '1', 'currency': 'usd', 'description': 'some_description'},
#      'dc28bef1c844fd6a1028886e4642d5640d1faff6fc7f5959fcf32548ca8d34ad')
# ])
# def test_sign(data, result):
#     assert result == sign_generator.generate(data)

