import uuid
from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, decode_token, jwt_required
from flask_security import utils
from flask_smorest import Blueprint, abort

from project.models.photo import PhotoModel
from project.models.role import RoleModel
from project.models.user import UserModel
from project.schemas.schemas import LoginQueryArgsSchema, JWTSchema, UserCreateSchema


blp = Blueprint(
    'Auth',
    'Auth',
    url_prefix='/api/auth',
    description="Auth for token JWT"
)


@blp.route('/signin')
class Auth(MethodView):

    @blp.arguments(LoginQueryArgsSchema, location='json')
    @blp.response(200, JWTSchema)
    def post(self, args):
        """Auth Signin for JWT Token"""
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = UserModel.objects(email=username).first()

        if user and utils.verify_password(password, user.password):
            if user.active:
                access_token = create_access_token(identity=user.email)
                pure_decoded = decode_token(access_token)
                return jsonify(
                    access_token=access_token,
                    user={
                        'name': user.name,
                        'email': user.email,
                        'photo': user.photo,
                        'created': user.created,
                        'post_count': PhotoModel.objects(owner=user).count(),
                        'like_count':  sum([p.like_count for p in PhotoModel.objects(owner=user)]),
                        'roles': [role.name for role in user.roles]},
                    token_type='Bearer',
                    expires=datetime.fromtimestamp(pure_decoded["exp"]).strftime('%Y-%m-%d %H:%M:%S'))

            return jsonify({'message': 'User access revoked.', 'authenticated': False}), 401

        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401
