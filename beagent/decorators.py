# coding: utf-8

from functools import wraps
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

def login_required(view):
    @wraps(view)
    def check(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view(request, *args, **kwargs)
        else:
            return redirect(reverse('beagent.views.common.signin'))
    return check

def anonymous_required(view):
    @wraps(view)
    def check(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return view(request, *args, **kwargs)
        else:
            return redirect(reverse('beagent.views.common.signin'))
    return check
