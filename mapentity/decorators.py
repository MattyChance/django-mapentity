from functools import wraps

from django.utils.decorators import available_attrs, method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

from . import app_settings
from .helpers import user_has_perm


def view_permission_required(login_url=None, raise_exception=True):
    def check_perms(user, perm):
        # Check both authenticated and anonymous
        if user_has_perm(user, perm):
            return True
        if not user.is_anonymous() and raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False

    def decorator(view_func):
        def _wrapped_view(self, request, *args, **kwargs):
            perm = self.get_view_perm()
            has_perm_decorator = user_passes_test(lambda u: check_perms(u, perm),
                                                  login_url=login_url)
            cbv_user_has_perm = method_decorator(has_perm_decorator)

            @cbv_user_has_perm
            def decorated(self, request, *args, **kwargs):
                return view_func(self, request, *args, **kwargs)

            return decorated(self, request, *args, **kwargs)

        return _wrapped_view
    return decorator


def save_history():
    """
    A decorator for class-based views, which save navigation history in
    session.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(self, request, *args, **kwargs):
            result = view_func(self, request, *args, **kwargs)

            # Stack list of request paths
            history = request.session.get('history', [])
            # Remove previous visits of this page
            history = [h for h in history if h['path'] != request.path]
            # Add this one and remove extras
            model = self.model or self.queryset.model
            history.insert(0, dict(title=unicode(self.get_title()),
                                   path=request.path,
                                   modelname=unicode(model._meta.object_name.lower())))
            if len(history) > app_settings['HISTORY_ITEMS_MAX']:
                history.pop()
            request.session['history'] = history

            return result
        return _wrapped_view
    return decorator
