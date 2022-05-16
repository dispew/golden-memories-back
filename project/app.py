import uuid

from flask_security import utils, MongoEngineUserDatastore

from project.extension import app, api, db, security
from project.api import auth, user, photo

from project.models.role import RoleModel
from project.models.user import UserModel

"""
    REST Api
"""
api.register_blueprint(auth.blp)
api.register_blueprint(user.blp)
api.register_blueprint(photo.blp)

user_datastore = MongoEngineUserDatastore(db, UserModel, RoleModel)
security.init_app(app, user_datastore)


@app.route("/")
def home():
    return ""


@app.before_first_request
def create_user():
    admin_role = user_datastore.find_or_create_role('admin')
    admin = user_datastore.find_user(email='admin@golden.memories')
    if not admin:
        user_datastore.create_user(
            name='Admin', email='admin@golden.memories', password=utils.hash_password('abcd1234'),
            roles=[admin_role], fs_uniquifier=str(uuid.uuid4())
        )

