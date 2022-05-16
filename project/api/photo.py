import hashlib
import io

from PIL import Image
from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import Blueprint

from project.extension import awsS3
from project.models.comment import CommentModel
from project.models.photo import PhotoModel
from project.models.user import UserModel
from project.schemas.schemas import UserSchema, PhotoSchema, PhotoCreateSchema, LightPhotoSchema, MessageSchema

blp = Blueprint(
    'Photos',
    'Photos',
    url_prefix='/api/photos',
    description="Photos endpoint"
)


@blp.route("/list")
class PhotoView(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, LightPhotoSchema(many=True))
    def get(self):
        """List approved Photos"""
        return PhotoModel.objects(approved=True)


@blp.route("/pending")
class Photos(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, LightPhotoSchema(many=True))
    def get(self):
        """List Photos"""
        return PhotoModel.objects(banned=False)


@blp.route("/get/<photo_id>")
class PhotoGetById(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, PhotoSchema)
    def get(self, photo_id):
        """Toggle a Like on a photo"""
        photo = PhotoModel.objects(id=photo_id).first()
        if photo:
            return photo

        return jsonify({'message': 'Photo not found.'}), 404


@blp.route("/create")
class PhotoCreate(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.arguments(PhotoCreateSchema, location='files')
    @blp.response(200, MessageSchema)
    def post(self, args):
        """Create a new Photo"""
        file = request.files.get('image', None)
        user = UserModel.objects.get(email=get_jwt_identity())
        if file:
            s3_key = hashlib.sha3_256((user.email + file.filename).encode('utf-8')).hexdigest()

            image_bytes = io.BytesIO()
            image = Image.open(file.stream)
            if image.size[0] > 1920:
                image = image.resize((1920, int(image.size[1] * (1920 / image.size[0]))), Image.ANTIALIAS)
            image.save(image_bytes, format='WEBP', quality=75)
            image_bytes.seek(0)

            thumb_bytes = io.BytesIO()
            thumb_image = image.resize((400, int(image.size[1] * (400 / image.size[0]))), Image.ANTIALIAS)
            thumb_image.save(thumb_bytes, format='WEBP', quality=75)
            thumb_bytes.seek(0)

            # image.save('/home/dispew/anchor/golden-memories/image.webp', format='WEBP', quality=75)
            # thumb_image.save('/home/dispew/anchor/golden-memories/thumb_image.webp', format='WEBP', quality=75)

            if awsS3.upload_to_aws(image_bytes, f'{s3_key}.webp') and \
                    awsS3.upload_to_aws(thumb_bytes, f'thumb-{s3_key}.webp'):

                photo = PhotoModel(
                    s3_key=s3_key,
                    owner=user,
                    message=request.form.get('message', '')
                )

                if photo.save():
                    return jsonify({'message': 'Photo registered successfully!'}), 200

                return jsonify({'message': 'Photo register error.'}), 400

            return jsonify({'message': 'Photo persist error.'}), 400

        return jsonify({'message': 'Photo upload error.'}), 401


@blp.route("/like/<photo_id>")
class LikePhotoById(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, MessageSchema)
    def post(self, photo_id):
        """Toggle a Like on a photo"""
        photo = PhotoModel.objects(id=photo_id).first()
        if photo:
            user = UserModel.objects.get(email=get_jwt_identity())
            if user in photo.likes:
                photo.likes.remove(user)
            else:
                photo.likes.append(user)

            if photo.save():
                return jsonify({'message': 'Like updated.'}), 200

            return jsonify({'message': 'Like error.'}), 400

        return jsonify({'message': 'Photo not found.'}), 404


@blp.route("/comment/<photo_id>")
class CommentPhotoById(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, MessageSchema)
    def post(self, photo_id):
        """Comment on a photo"""
        photo = PhotoModel.objects(id=photo_id).first()
        if photo:
            comment = CommentModel(**request.json)
            comment.owner = UserModel.objects.get(email=get_jwt_identity())
            photo.comments.append(comment)
            if photo.save():
                return jsonify({'message': 'Commented successfully.'}), 200

            return jsonify({'message': 'Comment error.'}), 400

        return jsonify({'message': 'Photo not found.'}), 404


@blp.route("/approve/<photo_id>")
class ApprovePhotoById(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, MessageSchema)
    def post(self, photo_id):
        """Approve or ban a photo"""
        state = request.json.get('approve', None)
        ban = request.json.get('ban', None)
        photo = PhotoModel.objects(id=photo_id).first()
        if photo:
            photo.approved = state
            photo.banned = ban
            if photo.save():
                return jsonify({'message': 'Commented successfully.'}), 200

            return jsonify({'message': 'Comment error.'}), 400

        return jsonify({'message': 'Photo not found.'}), 404
