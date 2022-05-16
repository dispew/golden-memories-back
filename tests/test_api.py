"""API tests"""
# pylint: disable=invalid-name
import secrets
import string
import uuid
import datetime as dt
import faker

DUMMY_ID = str(uuid.UUID('00000000-0000-0000-0000-000000000000'))
USERS_URL = '/api/users/'
PHOTOS_URL = '/api/photos/'
AUTH_URL = '/api/auth/'


class TestApi:
    """TEST API"""
    jwt_token = None
    user_1_id = user_1_etag = user_1 = None
    photo_1_id = photo_1_etag = photo_1 = None
    photo_2_id = photo_2_etag = photo_2 = None

    def test_login_jwt(self, test_client):
        """Login for JWT token"""
        ret = test_client.post(AUTH_URL+'signint', json={'username': 'user', 'password': 'pass'})
        ret_val = ret.get_json()
        assert ret.status_code == 200
        TestApi.jwt_token = ret_val.pop('access_token')

    def test_users_url(self, test_client):
        """GET USERS_URL """
        ret = test_client.get(USERS_URL+'list', headers={'Authorization': 'Bearer ' + TestApi.jwt_token})
        assert ret.status_code == 200
        assert ret.json != []

    def test_users_post(self, test_client):
        """ADD AUTHORS"""
        TestApi.user_1 = {
            "name": "John",
            "email": "doe@",
            "birth_date": dt.datetime(1958, 10, 2).strftime('%Y-%m-%d')
        }
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token)
        }

        ret = test_client.post(USERS_URL, json=TestApi.user_1, headers=headers_jwt)
        assert ret.status_code == 201
        ret_val = ret.json
        TestApi.user_1_id = ret_val.pop('id')
        TestApi.user_1_etag = ret.headers['ETag']
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        assert ret_val == TestApi.user_1

    def test_users_getlist(self, test_client):
        """GET LIST"""
        ret = test_client.get(USERS_URL)
        assert ret.status_code == 200
        ret_val = ret.json
        assert len(ret_val) == 1
        assert ret_val[0]['id'] == TestApi.user_1_id

    def test_users_getid(self, test_client):
        """GET AUTHORS  by ID"""
        ret = test_client.get(USERS_URL + TestApi.user_1_id)
        assert ret.status_code == 200
        assert ret.headers['ETag'] == TestApi.user_1_etag
        ret_val = ret.json
        ret_val.pop('id')
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        assert ret_val == TestApi.user_1

    def test_users_put(self, test_client):
        """PUT AUTHORS"""
        TestApi.user_1.update({'first_name': 'John2'})

        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
            'If-Match': TestApi.user_1_etag
        }

        ret = test_client.put(
            USERS_URL + TestApi.user_1_id,
            json=TestApi.user_1,
            headers=headers_jwt
        )
        assert ret.status_code == 200
        ret_val = ret.json
        ret_val.pop('id')
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        TestApi.user_1_etag = ret.headers['ETag']
        assert ret_val == TestApi.user_1

    def test_users_put404(self, test_client):
        """PUT AUTHORS  with wrong ID"""
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
            'If-Match': TestApi.user_1_etag
        }
        ret = test_client.put(
            USERS_URL + DUMMY_ID,
            json=TestApi.user_1,
            headers=headers_jwt
        )
        assert ret.status_code == 404

    def test_users_get_filter(self, test_client):
        """GET AUTHORS  WITH FILTERS"""
        ret = test_client.get(USERS_URL,
                              query_string={'first_name': TestApi.user_1.get("first_name")}
                              )
        assert ret.status_code == 200
        ret_val = ret.json

        assert len(ret_val) == 1
        assert set(v['id'] for v in ret_val) == {TestApi.user_1_id}

    def test_books_url(self, test_client):
        """GET BOOKS"""
        ret = test_client.get(PHOTOS_URL)
        assert ret.status_code == 200
        # assert ret.json == []

    def test_books_post(self, test_client):
        """POST AUTHORS"""
        TestApi.photo_1 = {
            'title': 'Ghostbusters',
            'author_id': TestApi.user_1_id
        }
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
        }

        ret = test_client.post(PHOTOS_URL, json=TestApi.photo_1, headers=headers_jwt)
        assert ret.status_code == 201
        ret_val = ret.json
        TestApi.photo_1_id = ret_val.pop('id')
        TestApi.photo_1_etag = ret.headers['ETag']
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        assert ret_val == TestApi.photo_1

    def test_books_post2(self, test_client):
        """POST BOOKS AGAIN"""
        TestApi.photo_2 = {
            'title': 'Ghostbusters2',
            'author_id': DUMMY_ID
        }
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
        }

        ret = test_client.post(PHOTOS_URL, json=TestApi.photo_2, headers=headers_jwt)
        assert ret.status_code == 400

        TestApi.photo_2.update({'author_id': TestApi.user_1_id})
        ret = test_client.post(PHOTOS_URL, json=TestApi.photo_2, headers=headers_jwt)
        assert ret.status_code == 201
        ret_val = ret.json
        TestApi.photo_2_id = ret_val.pop('id')
        TestApi.photo_2_etag = ret.headers['ETag']
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        assert ret_val == TestApi.photo_2

    def test_books_getid(self, test_client):
        """GET BOOK BY ID"""
        ret = test_client.get(PHOTOS_URL + TestApi.photo_1_id)
        assert ret.status_code == 200
        assert ret.headers['ETag'] == TestApi.photo_1_etag
        ret_val = ret.json
        ret_val.pop('id')
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        assert ret_val == TestApi.photo_1

    def test_books_put(self, test_client):
        """PUT BOOKS"""
        TestApi.photo_1.update({'title': 'Ghostbusters1-m'})
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
            'If-Match': TestApi.photo_1_etag
        }

        ret = test_client.put(
            PHOTOS_URL + TestApi.photo_1_id, json=TestApi.photo_1, headers=headers_jwt
        )
        assert ret.status_code == 200
        ret_val = ret.json
        ret_val.pop('id')
        ret_val.pop('created_at')
        ret_val.pop('updated_at')
        TestApi.photo_1_etag = ret.headers['ETag']
        assert ret_val == TestApi.photo_1

    def test_books_put404(self, test_client):
        """PUT BOOKS with wrong ID"""
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
            'If-Match': TestApi.photo_1_etag
        }
        # PUT wrong ID -> 404
        ret = test_client.put(
            PHOTOS_URL + DUMMY_ID, json=TestApi.photo_1, headers=headers_jwt
        )
        assert ret.status_code == 404

    def test_books_put400(self, test_client):
        """PUT BOOKS WITH unknow ID"""
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
            'If-Match': TestApi.photo_1_etag
        }
        TestApi.photo_1.update({'author_id': DUMMY_ID})

        # PUT wrong author ID -> 400
        ret = test_client.put(
            PHOTOS_URL + TestApi.photo_1_id, json=TestApi.photo_1, headers=headers_jwt
        )
        assert ret.status_code == 400

    def test_books_get_filter_authorid(self, test_client):
        """GET books with author_id 1 filter"""
        ret = test_client.get(PHOTOS_URL, query_string={'author_id': TestApi.user_1_id})
        assert ret.status_code == 200
        ret_val = ret.json

        assert len(ret_val) == 2
        assert set(v['id'] for v in ret_val) == {TestApi.photo_1_id, TestApi.photo_2_id}

    def test_books_delete(self, test_client):
        """DELETE BOOKS"""
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
            'If-Match': TestApi.photo_1_etag
        }
        # DELETE
        ret = test_client.delete(
            PHOTOS_URL + TestApi.photo_1_id, headers=headers_jwt
        )
        assert ret.status_code == 204

    def test_users_delete(self, test_client):
        """DELETE AUTHORS  ==> DELETE BOOKS with cascade"""
        headers_jwt = {
            'Authorization': 'Bearer {}'.format(TestApi.jwt_token),
            'If-Match': TestApi.user_1_etag
        }
        # DELETE
        ret = test_client.delete(
            USERS_URL + TestApi.user_1_id, headers=headers_jwt
        )
        assert ret.status_code == 204

        # GET by id users -> 404
        ret = test_client.get(USERS_URL + TestApi.user_1_id)
        assert ret.status_code == 404

        # GET by id books -> 404
        ret = test_client.get(PHOTOS_URL + TestApi.photo_1_id)
        assert ret.status_code == 404