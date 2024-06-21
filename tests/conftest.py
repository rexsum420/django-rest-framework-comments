import os

import django
from django.core import management


def pytest_addoption(parser):
    parser.addoption('--staticfiles', action='store_true', default=False,
                     help='Run tests with static files collection, using manifest '
                          'staticfiles storage. Used for testing the distribution.')


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            },
            'secondary': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    "debug": True,  # We want template errors to raise
                }
            },
        ],
        MIDDLEWARE=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
<<<<<<< HEAD
            'drf_comments',
            'drf_comments.authtoken',
=======
            'rest_framework',
            'rest_framework.authtoken',
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
            'tests.authentication',
            'tests.generic_relations',
            'tests.importable',
            'tests',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
    )

    # guardian is optional
    try:
        import guardian  # NOQA
    except ImportError:
        pass
    else:
        settings.ANONYMOUS_USER_ID = -1
        settings.AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'guardian.backends.ObjectPermissionBackend',
        )
        settings.INSTALLED_APPS += (
            'guardian',
        )

    # Manifest storage will raise an exception if static files are not present (ie, a packaging failure).
    if config.getoption('--staticfiles'):
<<<<<<< HEAD
        import drf_comments
        settings.STATIC_ROOT = os.path.join(os.path.dirname(drf_comments.__file__), 'static-root')
=======
        import rest_framework
        settings.STATIC_ROOT = os.path.join(os.path.dirname(rest_framework.__file__), 'static-root')
>>>>>>> e13688f0c0d32672d31ef3b9474c2a9f9dd12ae9
        backend = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
        settings.STORAGES['staticfiles']['BACKEND'] = backend

    django.setup()

    if config.getoption('--staticfiles'):
        management.call_command('collectstatic', verbosity=0, interactive=False)
