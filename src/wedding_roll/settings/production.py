# Development settings
from .common import *
import posixpath
from decouple import Config, RepositoryEnv
from .common import *

# Go up two directories from project base and then into config
env_path = os.path.join(BASE_DIR,'..','..','config','production.env')

env_config = Config(RepositoryEnv(env_path))
ALLOWED_HOSTS = env_config.get('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

SECRET_KEY=env_config.get('SECRET_KEY')
DEBUG = env_config.get('DEBUG',cast=bool)

AWS_STORAGE_BUCKET_NAME = env_config.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME =  env_config.get('AWS_S3_REGION_NAME') # e.g. us-east-2
AWS_ACCESS_KEY_ID = env_config.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env_config.get('AWS_SECRET_ACCESS_KEY')

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

STATIC_URL = '/static/'
MEDIA_URL ='/media/'
#STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))
#MEDIA_ROOT = os.path.join(BASE_DIR,'media')
STATIC_ROOT = AWS_S3_CUSTOM_DOMAIN + STATIC_URL
MEDIA_ROOT = AWS_S3_CUSTOM_DOMAIN + MEDIA_URL

DATABASES = {
    'default': {
        'ENGINE': env_config.get('DB_ENGINE'), 
        'NAME': env_config.get('DB_NAME'),
        'USER': env_config.get('DB_USER'),
        'HOST': env_config.get('DB_HOST'),
        'PORT': env_config.get('DB_PORT'),
    }
}

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'