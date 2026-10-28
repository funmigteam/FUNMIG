import os
import sys


from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-development-only')


DEBUG = True


ALLOWED_HOSTS = [


    'funmig.com',


    'www.funmig.com',


    'prof.funmig.com',
    'social.funmig.com',
    'ai.funmig.com',


    '94.183.51.150',


    'localhost',


    '127.0.0.1',


]


INSTALLED_APPS = [


    'django.contrib.admin',


    'django.contrib.auth',


    'django.contrib.contenttypes',


    'django.contrib.sessions',


    'django.contrib.messages',


    'django.contrib.staticfiles',


    'channels',


    'core',


    'chat',


]


ASGI_APPLICATION = 'myproject.asgi.application'


CHANNEL_LAYERS = {


    'default': {


        'BACKEND': 'channels.layers.InMemoryChannelLayer',


    },


}


WEBRTC_ICE_SERVERS = [
    {
        'urls': [
            url.strip()
            for url in os.getenv(
                'WEBRTC_STUN_URLS',
                'stun:stun.l.google.com:19302,stun:stun.cloudflare.com:3478',
            ).split(',')
            if url.strip()
        ],
    },
]


SITE_URL = os.getenv('SITE_URL', 'https://social.funmig.com')
FUNMIG_AI_URL = os.getenv('FUNMIG_AI_URL', 'https://ai.funmig.com').rstrip('/')


if os.getenv('WEBRTC_TURN_URLS'):

    WEBRTC_ICE_SERVERS.append({
        'urls': [
            url.strip()
            for url in os.getenv('WEBRTC_TURN_URLS', '').split(',')
            if url.strip()
        ],
        'username': os.getenv('WEBRTC_TURN_USERNAME', ''),
        'credential': os.getenv('WEBRTC_TURN_CREDENTIAL', ''),
    })


MIDDLEWARE = [


    'django.middleware.security.SecurityMiddleware',
    'myproject.security.LoginRateLimitMiddleware',


    'django.contrib.sessions.middleware.SessionMiddleware',


    'core.middleware.UserTimezoneMiddleware',


    'django.middleware.common.CommonMiddleware',


    'django.middleware.csrf.CsrfViewMiddleware',


    'django.contrib.auth.middleware.AuthenticationMiddleware',


    'django.contrib.messages.middleware.MessageMiddleware',


    'django.middleware.clickjacking.XFrameOptionsMiddleware',


]


ROOT_URLCONF = 'myproject.urls'


TEMPLATES = [


    {


        'BACKEND': 'django.template.backends.django.DjangoTemplates',


        'DIRS': [],


        'APP_DIRS': True,


        'OPTIONS': {


            'context_processors': [


                'django.template.context_processors.request',


                'django.contrib.auth.context_processors.auth',


                'django.contrib.messages.context_processors.messages',


            ],


        },


    },


]


WSGI_APPLICATION = 'myproject.wsgi.application'


DATABASES = {


    'default': {


        'ENGINE': 'django.db.backends.sqlite3',


        'NAME': BASE_DIR / 'db.sqlite3',


    }


}


AUTH_PASSWORD_VALIDATORS = [


    {


        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',


    },


    {


        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',


    },


    {


        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',


    },


    {


        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',


    },


]


LANGUAGE_CODE = 'fa-ir'


TIME_ZONE = 'Asia/Tehran'


USE_I18N = True


USE_TZ = True


STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_DIRS = [


    os.path.join(BASE_DIR, 'static'),


]


MEDIA_URL = '/media/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


DATA_UPLOAD_MAX_MEMORY_SIZE = 10737418240         


FILE_UPLOAD_MAX_MEMORY_SIZE = 10737418240         


FILE_UPLOAD_HANDLERS = [


    'django.core.files.uploadhandler.MemoryFileUploadHandler',


    'django.core.files.uploadhandler.TemporaryFileUploadHandler',


]


LOGIN_URL = 'login'


LOGIN_REDIRECT_URL = 'home'


LOGOUT_REDIRECT_URL = 'home'


CSRF_FAILURE_VIEW = 'core.views.csrf_failure_redirect'


JIBIT_API_KEY = os.environ.get('JIBIT_API_KEY', '')


JIBIT_SECRET_KEY = os.environ.get('JIBIT_SECRET_KEY', '')


CSRF_TRUSTED_ORIGINS = [


    'https://funmig.com',


    'https://www.funmig.com',


    'https://prof.funmig.com',
    'https://social.funmig.com',
    'https://ai.funmig.com',


    'https://94.183.51.150',


    'http://94.183.51.150',


    'http://localhost:8000',


    'http://127.0.0.1:8000',


]


SECURE_SSL_REDIRECT = False


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CSRF_COOKIE_SECURE = False


SESSION_COOKIE_SECURE = False

SESSION_COOKIE_NAME = os.getenv('DJANGO_SESSION_COOKIE_NAME', 'funmig_social_sessionid')


SESSION_COOKIE_DOMAIN = os.getenv('DJANGO_SESSION_COOKIE_DOMAIN') or None


CSRF_COOKIE_DOMAIN = os.getenv('DJANGO_CSRF_COOKIE_DOMAIN') or None

CSRF_COOKIE_NAME = os.getenv('DJANGO_CSRF_COOKIE_NAME', 'funmig_social_csrftoken')


CSRF_COOKIE_SAMESITE = 'Lax'  


SESSION_COOKIE_SAMESITE = 'Lax'


SECURE_BROWSER_XSS_FILTER = True


X_FRAME_OPTIONS = 'DENY'


SECURE_CONTENT_SECURITY_POLICY = {


    'default-src': ("'self'",),


    'script-src': ("'self'", "'unsafe-inline'", "'unsafe-eval'"),


    'style-src': ("'self'", "'unsafe-inline'"),


    'img-src': ("'self'", 'data:', 'https:'),


    'font-src': ("'self'",),


    'media-src': ("'self'",),


    'frame-src': ("'self'",),


}


VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', '')


VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', '')


VAPID_SUBJECT = 'mailto:admin@funmig.com'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)
JIBIT_API_KEY = os.environ.get('JIBIT_API_KEY', JIBIT_API_KEY)
JIBIT_SECRET_KEY = os.environ.get('JIBIT_SECRET_KEY', JIBIT_SECRET_KEY)
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', VAPID_PUBLIC_KEY)
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', VAPID_PRIVATE_KEY)
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 28800
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
DATA_UPLOAD_MAX_MEMORY_SIZE = 512 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000

for _validator in AUTH_PASSWORD_VALIDATORS:
    if _validator['NAME'].endswith('MinimumLengthValidator'):
        _validator['OPTIONS'] = {'min_length': 12}
if 'test' in sys.argv:
    SECURE_SSL_REDIRECT = SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = False
