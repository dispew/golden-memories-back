import os


class BaseConfig:
    SECRET_KEY = 'bulbasaur_squirtle_charmander'

    SESSION_TYPE = 'filesystem'
    SECURITY_URL_PREFIX = "/admin"
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = "mewtwo_mew"
    SECURITY_PASSWORD_SINGLE_HASH = "pbkdf2_sha512"
    SECURITY_POST_LOGIN_VIEW = '/admin/'
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}

    MONGODB_SETTINGS = {
        'db': 'golden',
        'host': '127.0.0.1',
        'port': 27017
    }

    # Api
    API_TITLE = "GoldenApi"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = '/api'
    OPENAPI_RAPIDOC_PATH = '/doc'
    OPENAPI_RAPIDOC_URL = 'https://unpkg.com/rapidoc/dist/rapidoc-min.js'
    API_SPEC_OPTIONS = {'x-internal-id': '2'}

    JWT_SECRET_KEY = 'articuno_zapdos_moltres'

    DEBUG = True
    USE_RELOADER = True

    S3_ACCESS_KEY = ''
    S3_SECRET_KEY = ''
