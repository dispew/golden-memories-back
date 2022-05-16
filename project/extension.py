from flask import Flask
from flask_mongoengine import MongoEngine
from flask_smorest import Api

from flask_jwt_extended import JWTManager

from flask_cors import CORS

from project.services.aws import AWSS3
from project.util import CustomJSONEncoder

app = Flask(__name__)
app.config.from_object('project.config.BaseConfig')

db = MongoEngine(app)

specs = {
    'security': [{"bearerAuth": []}],
    'components': {
        "securitySchemes":
            {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
    }
}

api = Api(app, spec_kwargs=specs)

jwt = JWTManager(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.json_encoder = CustomJSONEncoder

awsS3 = AWSS3(app, bucket='anchor-golden-memories')

