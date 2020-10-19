import sys
import logging

from economy.settings import *

class DisableMigrations:

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

DATABASES['default']['HOST'] = 'localhost'


TESTS_IN_PROGRESS = False
if 'test' in sys.argv[1:] or 'jenkins' in sys.argv[1:]:
    logging.disable(logging.CRITICAL)
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )
    DEBUG = False
    TEMPLATE_DEBUG = False
    TESTS_IN_PROGRESS = True
    MIGRATION_MODULES = DisableMigrations()
