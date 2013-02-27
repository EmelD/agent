# coding: utf-8

from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from beagent.decorators import login_required, anonymous_required
from beagent.forms import SignInForm, SignUpForm
from beagent.models import User
from beagent.utils import render, render_json


@login_required
def admin(request):
    pass

@login_required
def admin_platforms_list(request):
    pass

@login_required
def admin_view_platform(request):
    pass

@login_required
def admin_users_list(request):
    pass

@login_required
def admin_view_user(request):
    pass

@login_required
def admin_tasks_list(request):
    pass

@login_required
def admin_view_task(request):
    pass

@login_required
def admin_new_tickets(request):
    pass

@login_required
def admin_support_tickets_list(request):
    pass

@login_required
def admin_complaints_list(request):
    pass

@login_required
def admin_disputes_list(request):
    pass

@login_required
def admin_view_dispute(request):
    pass

@login_required
def admin_view_ticket(request):
    pass

@login_required
def admin_view_complaint(request):
    pass

@login_required
def admin_companies_list(request):
    pass

@login_required
def admin_platforms_list(request):
    pass

@login_required
def admin_edit_platform(request):
    pass

@login_required
def admin_arrival_money_list(request):
    pass

@login_required
def admin_outflow_money_list(request):
    pass

@login_required
def admin_history_financial_transactions(request):
    pass

@login_required
def admin_view_process_money_output(request):
    pass

@login_required
def admin_management_reasons_fail(request):
    pass

@login_required
def admin_requests_output_list(request):
    pass
