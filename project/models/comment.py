from datetime import datetime

import mongoengine as me

from project.models.user import UserModel


class CommentModel(me.EmbeddedDocument):
    owner = me.ReferenceField(UserModel)
    message = me.StringField()

    created = me.DateTimeField(default=datetime.now)
    modified = me.DateTimeField(default=datetime.now)
