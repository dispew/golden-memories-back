from datetime import datetime

import mongoengine as me

from project.extension import awsS3
from project.models.user import UserModel
from project.models.comment import CommentModel


class PhotoModel(me.Document):
    meta = {'collection': 'photos'}

    s3_key = me.StringField(required=True)
    owner = me.ReferenceField(UserModel)
    message = me.StringField()

    approved = me.BooleanField(default=False)
    banned = me.BooleanField(default=False)
    likes = me.ListField(me.ReferenceField(UserModel), default=[])
    comments = me.EmbeddedDocumentListField(CommentModel, default=[])

    created = me.DateTimeField(default=datetime.now)
    modified = me.DateTimeField(default=datetime.now)

    @property
    def photo(self):
        return awsS3.gen_temp_url(f'{self.s3_key}.webp')

    @property
    def thumb(self):
        return awsS3.gen_temp_url(f'thumb-{self.s3_key}.webp')

    @property
    def like_count(self):
        return len(self.likes)

    @property
    def comment_count(self):
        return len(self.comments)
