# coding: utf-8

from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from beagent.decorators import login_required, anonymous_required
from beagent.forms import SignInForm, SignUpForm
from beagent.models import User
from beagent.utils import render, render_json