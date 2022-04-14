from django.conf import settings


def is_root(request, *args, **kwargs):
    return request.user.is_superuser and request.headers.get("x-root-token") == settings.ROOT_TOKEN


def can_hijack(hijacker, hijacked):
    return hijacker.is_superuser