from ._internal import RootCommand, SubCommand


class DjangoAdmin(RootCommand):
    """https://docs.djangoproject.com/zh-hans/4.0/ref/django-admin/"""
    globals = globals()
    __main__ = 'django.core.management.execute_from_command_line'


class StartProject(SubCommand):
    """https://docs.djangoproject.com/zh-hans/4.0/ref/django-admin/#startproject"""


__all__ = ["django_admin"]

django_admin = DjangoAdmin()