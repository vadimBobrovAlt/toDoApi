from datetime import timedelta

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = 'SECRET_KEY'
JWT_AUTH_URL_RULE = '/api/v1/login'
JWT_EXPIRATION_DELTA = timedelta(18000)