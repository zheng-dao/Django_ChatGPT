import os
import posixpath
from django.urls import reverse_lazy
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLCONFIGDIR'] = os.path.join(BASE_DIR, 'app/data/matplotlib')

ENV = 'prod'
ENV_OS = 'linux' #linux|osx|windows
ENV_LIVE = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

PIXEL_SCRIPT_URL = 'https://finalyticsprod.s3.us-east-2.amazonaws.com/finalytics.js'
S3_BASE_URL = 'https://finalyticsprod.s3.us-east-2.amazonaws.com/'
#S3_BASE_URL = 'https://finalyticsstg.s3.us-east-2.amazonaws.com/'

CLOUDFRONT_BASE_URL = 'https://dfy3oyzv6dw2d.cloudfront.net/'
#STG: https://d1v4vw9mwf7wyh.cloudfront.net/
#PROD: https://dfy3oyzv6dw2d.cloudfront.net/

ALGORITHMS_LIST = ['distance', 'funnel', 'ftv', 'org', 'products_default', 'products_owned', 'referrer', 'search', 'segment', 'transaction', 'url', 'zipcode']
LAST_ALGORITHMS = ['referrer', 'search', 'url']

MASTER_ACCOUNT_ID = 1

EXTERNAL_SITE_IP = 'https://www.finalyticsdemo.com'

SQL_DB_NAME = ""
SQL_DATA_PATH = '/secure_file_priv_dir'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3253f3f8-438e-41b8-aa21-9e8930d608c6'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
LOG_API_POSTS = False

ALLOWED_HOSTS = ['18.224.82.124','3.138.70.85','3.141.77.109', 'finalyticsdata.com', 'stgfinalyticsdata.com', 'devfinalyticsdata.com', '3.15.51.84', 'ec2-3-15-51-84.us-east-2.compute.amazonaws.com', 'extractable.com', 'www.devfinalyticsdata.com', 'www.finalyticsdata.com', 'www.stgfinalyticsdata.com', 'www.devfinalyticsdata.com', ]


#REST_USE_JWT = True
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.IsAuthenticated',
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        #'app.permissions.SafelistPermission',
    ],
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}
#JWT_AUTH = {
#    'JWT_RESPONSE_PAYLOAD_HANDLER': 'app.views.jwt_response_payload_handler',
#    'JWT_VERIFY_EXPIRATION': False
#}

SITE_ID = 1

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                    os.path.join(BASE_DIR, 'app', 'templates'),
                    os.path.join(BASE_DIR, 'app', 'templates/account'),
                    os.path.join(BASE_DIR, 'app', 'templates/account/email'),
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                #'django.template.context_processors.static',
                #'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.env',

            ],
            'libraries':{
                'tags': 'app.templatetags.tags',
            }
            #'loaders': [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader'
            #],
    },
    },
]

AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend',
    'app.views.MyAuthenticationBackend',
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    # Add your apps here to enable them
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'app',
    'django.contrib.admin',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_filters',
    #'modelclone',
    #'searchableselect',
    #'sslserver',
    #'corsheaders',
    #'sortedm2m',
    #'django_user_agents',
    #'django_admin_logs',
    #'session_security',
    #'phonenumber_field',
    #'django_otp',
    #'django_otp.plugins.otp_static',
    #'django_otp.plugins.otp_totp',
    #'two_factor',
    #'formtools',
    #'django_password_validators',
    #'django_password_validators.password_history',
    #'axes',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    #'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django_user_agents.middleware.UserAgentMiddleware',
    #'django_otp.middleware.OTPMiddleware',
    #'two_factor.middleware.threadlocals.ThreadLocals',
    #'session_security.middleware.SessionSecurityMiddleware',
    #'axes.middleware.AxesMiddleware',
    #'app.middleware.check_mfa_setup_middleware'
]


STAFF_DOMAINS = ['extractable.com', 'finalytics.ai']

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    #'http://localhost:8000',
    #'http://127.0.0.1:8000',
    #'http://localhost:8001',
    #'http://127.0.0.1:8001',
    'http://finalytics.ai',
    'https://finalytics.ai',
    'http://staging4.finalytics.ai',
    'https://staging4.finalytics.ai',
    'http://staging10.finalytics.ai',
    'https://staging10.finalytics.ai',
    'http://finalyticsdata.com',
    'https://finalyticsdata.com',
    'http://finalyticsdemo.com',
    'https://finalyticsdemo.com',
    #'http://finalyticsdemo.com:8000',
    #'https://finalyticsdemo.com:8000',
    'http://www.finalyticsdemo.com',
    'https://www.finalyticsdemo.com',
    'http://www.stgfinalyticsdemo.com',
    'https://www.stgfinalyticsdemo.com',
    'http://stgfinalyticsdemo.com',
    'https://stgfinalyticsdemo.com',
    'http://www.devfinalyticsdemo.com',
    'https://www.devfinalyticsdemo.com',
    'http://devfinalyticsdemo.com',
    'https://devfinalyticsdemo.com',
    'http://www.finalyticsdemo.com:8000',
    'https://www.finalyticsdemo.com:8000',
    'http://35.208.161.20',
    'https://35.208.161.20',
    'http://3.138.53.243',
    'https://3.138.53.243',
    'http://3.134.132.30',
    'https://3.134.132.30',
    'https://www.blackstone.studio',
    'https://finalytics.blackstone.studio',
    'http://www.blackstone.studio',
    'http://finalytics.blackstone.studio',
    'https://finalyticsdemo624196.loca.lt',
    'https://as-react-vcuweb-dev01-eu-vy-slot1.azurewebsites.net',
    'https://staging.visionsfcu.org',
    'https://www.visionsfcu.org',
    'https://visionsfcu.org',
    'http://www.dev.millennialwebdevelopment.com',
    'https://cscutx.com',
    'https://www.cscutx.com',
    'http://cscuprod.wpengine.com',
    'https://cscuprod.wpengine.com',
    'http://cscustg.wpengine.com',
    'https://cscustg.wpengine.com',
    'https://api.contentful.com',
    'https://www.uccu.com',
    'https://dev.uccu.com',
    'https://staging.uccu.com',
    'https://devfinalyticsdata.com',
    'https://www.devfinalyticsdemo.com',
    'https://finalyticsdemo624197.loca.lt',
    'https://finalyticsdemo624198.loca.lt',
    'http://18.218.80.217:8080',
    'https://sffiredev.wpengine.com',
    'https://www-stg.sffirecu.org',
    'https://sffirecu.org',
    'https://www.lfcu.org',
    'https://www.georgiasown.org',
]

REST_SAFE_LIST_IPS = list(CORS_ORIGIN_WHITELIST) + [
    '108.233.250.186', #Scott's IP
    '35.208.161.20', #fin.ai stg and prod
    '3.138.53.243', #findemo stg
    '3.134.132.30', #findemo prod
    '38.95.108.163', #Blackstone
    ]

ROOT_URLCONF = 'ga.urls'


WSGI_APPLICATION = 'ga.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
#STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))
STATICFILES_DIRS = [
    os.path.join('app', 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

IMG_STORE_BASE_URL = 'https://finalyticsdata.com'

DEFAULT_FROM_EMAIL = 'hello@finalytics.ai'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

##AUTHENTITATION/VERIFICATION SETTINGS: http://django-allauth.readthedocs.io/en/latest/configuration.html
LOGIN_URL = 'two_factor:login'
#LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_URL
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
#ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'https://www.finalytics.ai/redirect/'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = PASSWORD_RESET_TIMEOUT = 3*24*60*60
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
#ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = reverse_lazy('account_confirm_complete')
#ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = reverse_lazy('account_confirm_complete')

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 900

#django-session-security settings
SESSION_SECURITY_INSECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SECURITY_WARN_AFTER = 14*60
SESSION_SECURITY_EXPIRE_AFTER = 15*60
SESSION_SECURITY_PASSIVE_URL_NAMES = ['ignore']
SESSION_COOKIE_DOMAIN = ''
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=15)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'secure_tools.DigitLowerUpperValidator',
    },
    {
        'NAME': 'django_password_validators.password_history.password_validation.UniquePasswordsValidator',
        'OPTIONS': {
             # How many recently entered passwords matter.
             # Passwords out of range are deleted.
             # Default: 0 - All passwords entered by the user. All password hashes are stored.
            'last_passwords': 5 # Only the last 5 passwords entered by the user
        }
    },
]



BENCHMARK_SERIES = ['Average', 'quarterly growth', 'year over year', 'quarter over quarter']

DEFAULT_COLORS = ["#209af1", "#84c586", "#00429b", "#7793db", '#a8cfe5', '#7497aa', '#c58484', '#dba377', '#aa8674', '#f16920']
DEFAULT_COLORS += DEFAULT_COLORS*5
DEFAULT_GRADIENT_COLORS = ["#209af1", "#84c586", "#00429b", "#7793db", "#a8cfe5", "#7497aa", '#c58484', '#dba377', '#aa8674', '#f16920']
DEFAULT_GRADIENT_COLORS += DEFAULT_GRADIENT_COLORS*5
DEFAULT_STYLE_COLORS = {'blue':["#209af1", "#a8cfe5"]}

#Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

STATE_ABBREV_TO_STATE = {'AL': 'Alabama',
 'AK': 'Alaska',
 'AS': 'American Samoa',
 'AZ': 'Arizona',
 'AR': 'Arkansas',
 'CA': 'California',
 'CO': 'Colorado',
 'CT': 'Connecticut',
 'DE': 'Delaware',
 'DC': 'District of Columbia',
 'FL': 'Florida',
 'GA': 'Georgia',
 'GU': 'Guam',
 'HI': 'Hawaii',
 'ID': 'Idaho',
 'IL': 'Illinois',
 'IN': 'Indiana',
 'IA': 'Iowa',
 'KS': 'Kansas',
 'KY': 'Kentucky',
 'LA': 'Louisiana',
 'ME': 'Maine',
 'MD': 'Maryland',
 'MA': 'Massachusetts',
 'MI': 'Michigan',
 'MN': 'Minnesota',
 'MS': 'Mississippi',
 'MO': 'Missouri',
 'MT': 'Montana',
 'NE': 'Nebraska',
 'NV': 'Nevada',
 'NH': 'New Hampshire',
 'NJ': 'New Jersey',
 'NM': 'New Mexico',
 'NY': 'New York',
 'NC': 'North Carolina',
 'ND': 'North Dakota',
 'MP': 'Northern Mariana Islands',
 'OH': 'Ohio',
 'OK': 'Oklahoma',
 'OR': 'Oregon',
 'PA': 'Pennsylvania',
 'PR': 'Puerto Rico',
 'RI': 'Rhode Island',
 'SC': 'South Carolina',
 'SD': 'South Dakota',
 'TN': 'Tennessee',
 'TX': 'Texas',
 'UT': 'Utah',
 'VT': 'Vermont',
 'VI': 'Virgin Islands',
 'VA': 'Virginia',
 'WA': 'Washington',
 'WV': 'West Virginia',
 'WI': 'Wisconsin',
 'WY': 'Wyoming'}

STATE_TO_ABBREV = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

NOTIFICATIONS = {}
NOTIFICATIONS['admins'] = ['sbarnard@extractable.com']
NOTIFICATIONS['new_lead'] = ['sbarnard@extractable.com']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': ['console']
        },
        #'two_factor': {
        #    'handlers': ['console'],
        #    'level': 'ERROR',
        #}
    }
}

try:
    LOCAL_SETTINGS
except NameError:
    try:
        from ga.settings_local import *
    except ImportError:
        LOCAL_SETTINGS = False
        pass
