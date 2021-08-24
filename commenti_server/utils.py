from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied

def authenticated_users_only(fn):
    def wrapper(cls, root, info, **kwargs):
        if not info.context.user.is_authenticated:
            raise PermissionDenied(
                _('You must be logged in')
            )
        return fn(cls, root, info, **kwargs)

    return wrapper
