from functools import wraps
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    """
    Restrict a view to specific roles.
    Usage: @role_required("ADMIN", "LECTURER")
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    return role_required("ADMIN")(view_func)


def lecturer_required(view_func):
    return role_required("LECTURER")(view_func)


def student_required(view_func):
    return role_required("STUDENT")(view_func)