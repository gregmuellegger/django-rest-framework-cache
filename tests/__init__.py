from django.core.management import call_command
from django.test.utils import setup_test_environment


def configure():
    from django.conf import settings

    settings.configure(
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': ':memory:'}},
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',

            'rest_framework',
            'tests',
        ),
    )

    import django
    django.setup()

configure()
setup_test_environment()

call_command('migrate')