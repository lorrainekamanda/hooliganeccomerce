import os
import cloudinary
import django_heroku
import dj_database_url
from decouple import config,Csv


ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = []




INSTALLED_APPS = [
   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'django_countries',
    'stripe',
    'social_django',
    'cloudinary',
    'rest_framework',
    'bootstrap_datepicker_plus',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'demo.urls'





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'social_django.context_processors.backends',  
                'social_django.context_processors.login_redirect', 
                'django.template.context_processors.media',
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


MODE=config("MODE", default="dev")
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
# development
if config('MODE')=="dev":
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'NAME': config('DB_NAME'),
           'USER': config('DB_USER'),
           'PASSWORD': config('DB_PASSWORD'),
           'HOST': config('DB_HOST'),
           'PORT': '',
       }
       
   }
# production
else:
   DATABASES = {
       'default': dj_database_url.config(
           default=config('DATABASE_URL')
       )
   }

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


AUTHENTICATION_BACKENDS = (
   
   
    'django.contrib.auth.backends.ModelBackend',

   
    'allauth.account.auth_backends.AuthenticationBackend',

    'social_core.backends.facebook.FacebookOAuth2',
    
)

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



CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_FACEBOOK_KEY  = '326790765061673'
SOCIAL_AUTH_FACEBOOK_SECRET  = 'd240a5a03c150413ff4e7176db9535de'
SOCIAL_AUTH_FACEBOOK_API_VERSION = 'v8.0'
STRIPE_SECRET_KEY = "sk_test_51I8OnPE4J5N0ITOGgEB1M6Qku1f75lsuD6Fw2Bo5S1zmOcfj8vPzaUC6FgFklF0m6jZ10O6LallYY2DVsgHgBZQj006Hb51SS6"

id = '989850233242-8ggt05kq646pokp9bqotdhndm4hd903r.apps.googleusercontent.com'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
secret = 'yCXALy4tzPszcYALJ4D1rrak'


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' 


# EMAIL_HOST = "localhost"
EMAIL_PORT = 587
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "lorrainekamanda@gmail.com"
EMAIL_HOST_PASSWORD = "leilanjeri123"
EMAIL_USE_TLS = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_FILE_PATH = "sent_emails"


ACCOUNT_FORMS = {
'signup': 'core.forms.CustomSignupForm',
'login': 'core.forms.YourLoginForm'
}


django_heroku.settings(locals())


cloudinary.config( 
  cloud_name = "dqj36cjxw", 
  api_key = "916162855945684", 
  api_secret = "8D2h4MB2jmA6_Twft8yemnYN2dY" 
)

BOOTSTRAP4 = {
    'include_jquery': True,
}






