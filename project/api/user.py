import hashlib
import io
import uuid

from PIL import Image
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_security import utils
from flask_smorest import Blueprint

from project.extension import awsS3
from project.models.role import RoleModel
from project.models.user import UserModel
from project.schemas.schemas import UserSchema, MessageSchema, UserCreateSchema

blp = Blueprint(
    'Users',
    'Users',
    url_prefix='/api/users',
    description="Users endpoint"
)


@blp.route("/list")
class Users(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """List Users"""
        return UserModel.objects()


@blp.route("/get/<user_id>")
class UserById(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, UserSchema)
    def post(self, user_id):
        """Get user data by ID"""
        user = UserModel.objects.get_or_404(_id=user_id)
        if user:
            return user

        return jsonify({'message': 'User not found.'}), 404


@blp.route("/register")
class RegisterUser(MethodView):

    @blp.arguments(UserCreateSchema, location='files')
    @blp.response(200, MessageSchema)
    def post(self, args):
        """Register a new User"""
        print(request.files)
        file = request.files.get('image', None)

        if file:
            email = request.form.get("email", None)
            user = UserModel.objects(email=email).first()
            if not user:
                s3_key = hashlib.sha3_256((email + file.filename).encode('utf-8')).hexdigest()

                role_user = RoleModel.objects(name='user').first()

                image_bytes = io.BytesIO()
                image = Image.open(file.stream)
                image = image.resize((100, int(image.size[1] * (100 / image.size[0]))), Image.ANTIALIAS)
                image.save(image_bytes, format='WEBP', quality=75)
                image_bytes.seek(0)

                if awsS3.upload_to_aws(image_bytes, f'profile-{s3_key}.webp'):
                    user = UserModel(
                        name=request.form.get('name', None),
                        email=email,
                        s3_key=s3_key,
                        password=utils.hash_password(request.form.get('password', None)),
                        fs_uniquifier=str(uuid.uuid4())
                    )
                    user.roles.append(role_user)

                    if user.save():
                        return jsonify({'message': 'User registred successfully!'}), 200

                return jsonify({'message': 'User persist error.'}), 400

            return jsonify({'message': 'E-mail already registred'}), 400

        return jsonify({'message': 'User photo upload error.'}), 400


@blp.route("/allow/<user_id>")
class AllowUserById(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, MessageSchema)
    def post(self, user_id):
        """Get user data by ID"""
        user = UserModel.objects(id=user_id).first()
        if user:
            user.active = request.json.get('active', True)
            if user.save():
                return jsonify({'message': 'User active state changed.'}), 200

            return jsonify({'message': 'Failed to change user active state.'}), 400

        return jsonify({'message': 'User not found.'}), 404


@blp.route("/promote/<user_id>")
class PromoteUserById(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, MessageSchema)
    def post(self, user_id):
        """Promote user role by ID"""
        admin_role = RoleModel.objects(name='admin').first()
        user_role = RoleModel.objects(name='user').first()
        user = UserModel.objects(id=user_id).first()
        if user:
            state = request.json.get('promote', False)
            if state:
                if user_role in user.roles:
                    user.roles.remove(user_role)
                if admin_role not in user.roles:
                    user.roles.append(admin_role)
            else:
                if admin_role in user.roles:
                    user.roles.remove(admin_role)
                if user_role not in user.roles:
                    user.roles.append(user_role)

            if user.save():
                return jsonify({'message': 'User active state changed.'}), 200

            return jsonify({'message': 'Failed to change user active state.'}), 400

        return jsonify({'message': 'User not found.'}), 404
