import traceback
from datetime import datetime
from http.client import HTTPException

import pytest
from flask_security import MongoEngineUserDatastore

from project.api import auth, user, photo
from project.extension import api, app, db, security
from project.models.role import RoleModel
from project.models.user import UserModel


@pytest.fixture(scope='module')
def test_client():
    application = app
    application.config['TESTING'] = True

    api.register_blueprint(auth.blp)
    api.register_blueprint(user.blp)
    api.register_blueprint(photo.blp)

    user_datastore = MongoEngineUserDatastore(db, UserModel, RoleModel)
    security.init_app(app, user_datastore)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = application.test_client()

    # Establish an application context before running the tests.
    ctx = application.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
