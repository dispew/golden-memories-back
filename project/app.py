import uuid

from flask_security import utils, MongoEngineUserDatastore, Security

from project.extension import app, api, db
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
security = Security(app, user_datastore)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.before_first_request
def create_user():
    # user_role = user_datastore.find_or_create_role('user')
    # user = user_datastore.find_user(email='user@golden.memories')
    # if not user:
    #     user_datastore.create_user(
    #         name='User', email='user@golden.memories', password=utils.hash_password('abc123'),
    #         roles=[user_role], fs_uniquifier=str(uuid.uuid4())
    #     )
    admin_role = user_datastore.find_or_create_role('admin')
    admin = user_datastore.find_user(email='admin@golden.memories')
    if not admin:
        user_datastore.create_user(
            name='Admin', email='admin@golden.memories', password=utils.hash_password('abcd1234'),
            roles=[admin_role], fs_uniquifier=str(uuid.uuid4())
        )

    # import os
    # from project.models.photo import PhotoModel
    # from PIL import Image
    #
    # PhotoModel.objects().delete()
    #
    # for f in os.listdir('/home/dispew/anchor/golden-front/src/assets/marriage/'):
    #     print(f)
    #     if f != '.' and f != '..':
    #         image = Image.open(os.path.join('/home/dispew/anchor/golden-front/src/assets/marriage/', f))
    #         thumb_image = image.resize((300, int(image.size[1]/(image.size[0]/300))))
    #         thumb_image.save(os.path.join('/home/dispew/anchor/golden-front/src/assets/marriage/', 'thumb-'+f))
    #         photo = PhotoModel.objects(photo=f).first()
    #         if not photo:
    #             photo = PhotoModel()
    #             photo.photo = os.path.join('http://127.0.0.1:3000/src/assets/marriage/', f)
    #             photo.thumb = os.path.join('http://127.0.0.1:3000/src/assets/marriage/', 'thumb-'+f)
    #             photo.owner = admin
    #             photo.message = ' '.join(f.split('-')[1:3])
    #             photo.approved = True
    #             photo.save()

