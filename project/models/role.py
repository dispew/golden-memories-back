
from flask_security import RoleMixin
import mongoengine as me


class RoleModel(me.Document, RoleMixin):
    meta = {'collection': 'roles'}

    name = me.StringField(required=True, unique=True)
    description = me.StringField()
