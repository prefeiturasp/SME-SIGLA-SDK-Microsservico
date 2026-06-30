import django
from django.conf import settings


def pytest_configure():
    if not settings.configured:
        settings.configure(
            SECRET_KEY="test",
            INSTALLED_APPS=["rest_framework"],
            USE_TZ=True,
        )
        django.setup()
