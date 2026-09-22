from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(role):

    def decorator(view_func):

        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):

            if request.user.role != role:
                return redirect('home')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator