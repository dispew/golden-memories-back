from bson import ObjectId
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """Add support for serializing ObjectId"""

    def default(self, o):
        if type(o) == ObjectId:
            return str(o)
        else:
            return super().default(o)
