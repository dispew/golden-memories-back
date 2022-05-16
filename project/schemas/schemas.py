import marshmallow as ma
from marshmallow.validate import Length


class LoginQueryArgsSchema(ma.Schema):
    class Meta:
        unknown = ma.EXCLUDE
        ordered = True

    username = ma.fields.Str(required=True, validate=Length(min=2, max=40))
    password = ma.fields.Str(required=True, validate=Length(min=2, max=40))


class JWTSchema(ma.Schema):
    class Meta:
        unknown = ma.EXCLUDE
        ordered = True

    access_token = ma.fields.Str()
    token_type = ma.fields.Str()
    expires = ma.fields.Str()


class UserCreateSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'password', 'image')
    image = ma.fields.Raw(metadata={'type': 'string', 'format': 'binary'})


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('name', 'description')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'photo', 'active', 'created', 'roles')
    roles = ma.fields.List(ma.fields.Nested(RoleSchema))


class LightUserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'photo')
    roles = ma.fields.List(ma.fields.Nested(RoleSchema))


class CommentCreateSchema(ma.Schema):
    class Meta:
        fields = ('message',)


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('owner', 'message')
    owner = ma.fields.Nested(UserSchema)


class PhotoCreateSchema(ma.Schema):
    class Meta:
        fields = ('image', 'message')
    image = ma.fields.Raw(metadata={'type': 'string', 'format': 'binary'})


class PhotoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'photo', 'owner', 'message', 'likes', 'comments', 'created')
    owner = ma.fields.Nested(LightUserSchema)
    likes = ma.fields.List(ma.fields.Nested(LightUserSchema))
    comments = ma.fields.List(ma.fields.Nested(CommentSchema))


class LightPhotoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'thumb', 'photo', 'owner', 'approved', 'banned', 'message', 'like_count', 'comment_count', 'created')
    owner = ma.fields.Nested(LightUserSchema)
    like_count = ma.fields.Int()
    comment_count = ma.fields.Int()


class MessageSchema(ma.Schema):
    message = ma.fields.Str()

