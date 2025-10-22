from config.settings import *

SECRET_KEY = 'test-secret-key-for-ci-only'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_myapp",
        "USER": "postgres",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

DEBUG = False

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
