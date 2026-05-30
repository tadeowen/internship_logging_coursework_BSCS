from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def role_required(*allowed_roles):
    """
    Decorator for views that checks that the user has the required role.
    Redirects to dashboard with error message if not authorized.
    """
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
        return _wrapped_view
    return decorator