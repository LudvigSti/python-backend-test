from os import environ

class Config:
    DEBUG = environ.get('DEBUG', False)
    TESTING = environ.get('TESTING', False)
    SECRET_KEY = environ.get('SECRET_KEY', 'your_secret_key_here')
    JSON_SORT_KEYS = False
    # Add any other configuration variables as needed