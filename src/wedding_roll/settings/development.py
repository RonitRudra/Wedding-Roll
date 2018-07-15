# Development settings
from .common import *
import posixpath

STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))
MEDIA_URL ='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

