import traceback
from datetime import datetime
from http.client import HTTPException

import pytest

from project.api import auth, user, photo
from project.extension import api, app, db


@pytest.fixture(scope='module')
def test_client():
    application = app
    application.config['TESTING'] = True

    api.register_blueprint(auth.blp)
    api.register_blueprint(user.blp)
    api.register_blueprint(photo.blp)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        with open('log/cli.log', 'a') as log:
            log.write('##### ' + str(datetime.now()) + ' #####')
            log.write(traceback.format_exc())
            log.close()

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = application.test_client()

    # Establish an application context before running the tests.
    ctx = application.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
