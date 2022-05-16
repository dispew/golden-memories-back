from datetime import datetime

import mongoengine as me

from project.extension import awsS3
from project.models.role import RoleModel


class UserModel(me.Document):
    meta = {'collection': 'users'}

    s3_key = me.StringField()

    name = me.StringField(required=True)
    email = me.EmailField(required=True)
    password = me.StringField(required=True, min_length=6)

    fs_uniquifier = me.StringField(required=True, unique=True)

    active = me.BooleanField(default=True)

    created = me.DateTimeField(default=datetime.now)
    modified = me.DateTimeField(default=datetime.now)

    roles = me.ListField(me.ReferenceField(RoleModel), default=[])

    @property
    def photo(self):
        if self.s3_key:
            return awsS3.gen_temp_url(f'profile-{self.s3_key}.webp')
        return None
