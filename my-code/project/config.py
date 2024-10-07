# config.py
from corsheaders.defaults import default_headers


# Elasticsearch DSL configurations
# ----------------------------------------------------
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}

# MongoDB configurations
# ----------------------------------------------------
MONGO_CONFIG = {
    'URI': 'mongodb://localhost:27017/',
    'DB_NAME': 'mic_db',
    'COLLECTION_NAME': ['drugs_coll', 'ICDs'],
}

# CORS
# CORS settings
# ----------------------------------------------------
CORS_ALLOWED_ORIGINS = ["http://localhost:8080"]
CORS_ALLOW_HEADERS = list(default_headers) + ['lang']
ALLOWED_HOSTS = ['*']


# DB
# ----------------------------------------------------
ENGINE = 'djongo'
DJONGO_DB_NAME = MONGO_CONFIG['DB_NAME']
DJANGO_DB_HOST = 'localhost'
DJANGO_DB_PORT = 27017

# POSTGRESQL
POSTGRESQL_CONF = {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "CPT_PROCEDURES",
    "USER": "postgres",
    "PASSWORD": "0101011001",
    "HOST": "localhost",
    "PORT": "5432",
}

# -----------------------------------------

# Keys
# ----------------------------------------------------
SECRET_KEY = 'django-insecure-s5ympbnd23mzltx!0ve!vtuv1)h0f0l@l2e(em=audeyo9a@(%'
DEBUG = True
