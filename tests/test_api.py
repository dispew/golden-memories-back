"""API tests"""
# pylint: disable=invalid-name
import secrets
import string
import uuid
import datetime as dt
from typing import io

import faker
import werkzeug
from PIL import Image

DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
USERS_URL = '/api/users/'
PHOTOS_URL = '/api/photos/'
AUTH_URL = '/api/auth/'


class TestApi:
    """TEST API"""
    jwt_token = None

    def test_login_jwt(self, test_client):
        """Login for JWT token"""
        ret = test_client.post(AUTH_URL+'signin', json={
            'username': 'admin@golden.memories', 'password': 'abcd1234'})
        ret_val = ret.get_json()
        assert ret.status_code == 200
        TestApi.jwt_token = ret_val.pop('access_token')

    def test_users_url(self, test_client):
        """GET USERS_URL """
        ret = test_client.get(USERS_URL+'list', headers={'Authorization': 'Bearer ' + TestApi.jwt_token})
        assert ret.status_code == 200
        assert ret.json != []

    def test_users_get404(self, test_client):
        """PUT USERS with wrong ID"""
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
        }
        ret = test_client.get(
            USERS_URL + 'get/' + '000000000000000000000000',
            headers=headers_jwt
        )
        assert ret.status_code == 404

    def test_photos_url(self, test_client):
        """GET PHOTOS """
        ret = test_client.get(PHOTOS_URL+'list', headers={'Authorization': 'Bearer ' + TestApi.jwt_token})
        assert ret.status_code == 200
        assert ret.json != []

    def test_photos_get404(self, test_client):
        """PUT PHOTOS with wrong ID"""
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
        }
        ret = test_client.get(
            PHOTOS_URL + 'get/' + '000000000000000000000000',
            headers=headers_jwt
        )
        assert ret.status_code == 404

    def test_users_get401(self, test_client):
        """GET USERS without header"""
        ret = test_client.get(
            USERS_URL + 'get/' + '000000000000000000000000'
        )
        assert ret.status_code == 401

    def test_photos_get401(self, test_client):
        """GET PHOTOS without header"""
        ret = test_client.get(
            PHOTOS_URL + 'get/' + '000000000000000000000000'
        )
        assert ret.status_code == 401
