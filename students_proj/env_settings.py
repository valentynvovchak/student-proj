import os
from django.core.exceptions import ImproperlyConfigured


msg = "Set the %s environment variable"


def get_env_var(var_name):
    try:
        return os.environ.get(var_name)
    except KeyError:
        error_msg = msg % var_name
        raise ImproperlyConfigured(error_msg)


# local.py

# FB_API_KEY = get_env_var("FB_API_KEY")
# os.environ["Secret Key"]


SECRET_KEY_ST = get_env_var("SECRET_KEY_STUDENTS")
DB_NAME = get_env_var("DB_NAME_STUDENTS")
DB_USER = get_env_var("DB_USER_STUDENTS")
DB_PASSWORD = get_env_var("DB_PASSWORD_STUDENTS")
FACEBOOK_CLIENT_ID = get_env_var("FACEBOOK_CLIENT_ID_STUDENTS")
FACEBOOK_SECRET = get_env_var("FACEBOOK_SECRET_STUDENTS")
GITHUB_CLIENT_ID = get_env_var("GITHUB_CLIENT_ID_STUDENTS")
GITHUB_SECRET = get_env_var("GITHUB_SECRET_STUDENTS")


# email settings
# please, set here you smtp server details and your admin email

ADMIN_EMAIL_ST = get_env_var("ADMIN_EMAIL_STUDENTS")
EMAIL_HOST_ST = 'smtp.sendgrid.net'
EMAIL_HOST_USER_ST = 'apikey'
EMAIL_HOST_PASSWORD_ST = get_env_var("EMAIL_HOST_PASSWORD_STUDENTS")
EMAIL_PORT_ST = 587
EMAIL_USE_TLS_ST = True
EMAIL_USE_SSL_ST = False
