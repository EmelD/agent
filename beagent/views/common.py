# -*- coding: utf-8 -*-

from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from beagent.decorators import login_required, anonymous_required
from beagent.forms import SignInForm, SignUpForm, EditProfileForm, DateForm, PurseForm, PaymentsForm, NonCashPaymentsForm, MessageReviewForm
from beagent.models import User, Town, Country, UserList, Review, AgentTask, Invitation, AdvertisingPlatform, RequestForCompany, Balance, AgentPurse, MoneyTransfer, NonCashPayment, Message, MessageReview, PaymentSystem
from beagent.utils import render, render_json, paging_list, createPaginationBlock
import datetime
from django.template.loader import render_to_string
from datetime import date
from django.db.models import Q
from beagent_project.settings import SITE_URL
from django.utils.timezone import utc

def index(request):
    return render(request, 'beagent/index.html')

@anonymous_required
def signup(request):
    if request.is_ajax():
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User(email=data['email'], type=data['type'])
            user.set_password(data['password'])
            user.save()
            user = authenticate(email=data['email'], password=data['password'])
            login(request, user)
            return render_json({'redirect': reverse('beagent.views.common.index'), 'status': True})
        else:
            return render_json({'errors': form.errors, 'status': False})
    else:
        return render(request, 'beagent/signup.html')

@anonymous_required
def signin(request):
    if request.is_ajax():
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user:
                login(request, user)
                return render_json({'redirect': reverse('beagent.views.common.profile'), 'status': True})
            else:
                return render_json({'messages': [u'Неверное сочетание E-mail \ Пароль.'], 'status': False})
        else:
            return render_json({'errors': form.errors, 'status': False})
    else:
        return render(request, 'beagent/signin.html')

@login_required
def signout(request):
    logout(request)
    return redirect(reverse('beagent.views.common.index'))

@login_required
def switch_profile_type(request):
    request.user.type = 'advertiser' if request.user.type == 'agent' else 'agent'
    request.user.save()
    return redirect(reverse('beagent.views.common.profile'))

@login_required
def edit_profile(request):
    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        request.POST['name'], request.POST['surname'] = request.POST['userName'].split(' ')
        request.POST['town'] = Town.objects.get(name=request.POST['town']).pk
        request.POST['country'] = Country.objects.get(name=request.POST['country']).pk
        form = EditProfileForm(request.POST, request.FILES, initial={'user':request.user.pk} )
        if form.is_valid():
            for field in form.cleaned_data:
                setattr(request.user, field, form.cleaned_data[field])
            request.user.save()
            return render_json(u'Successful!')
        else:
            return render_json(form.errors)
    else:
        return render(request, 'beagent/ba-agent-profile-edit.html', {'user':request.user,
                                                                               'days':[x+1 for x in range(31)],
                                                                               'months':[x+1 for x in range(12)],
                                                                               'years':[x+1 for x in range(date.today().year-40, date.today().year)] })

@login_required
def change_password(request):
    if request.is_ajax():
        if request.POST['confirm_password'] != request.POST['new_password']:
            return render_json(u'Введенные пароли не совпадают')
        user = User.objects.get(pk=request.user.pk)
        #old_passw = user.password
        user.set_password(request.POST['new_password'])
        #if old_passw != user.password:
        #    return render_json(u'Старый пароль введен не верно!!!!')
        user.save()
        return render_json(u'Successful!')
    else:
        return render_json(u'Error')

@login_required
def profile(request):
    user = User.objects.get(pk=request.user.pk)
    tasks_agent = AgentTask.objects.filter(user=user.pk).exclude(status='completed')
    unverified_tasks = AgentTask.objects.filter(customer=user.pk,status='unverified')
    platforms = AdvertisingPlatform.objects.filter(user=user.pk)
    company_requests = RequestForCompany.objects.filter(user=user.pk,status='stat1')
    invitations = Invitation.objects.filter(platform__in=platforms,status='new')
    review = {'positive':Review.objects.filter(user=request.user.pk,type=1).count(),
              'negative':Review.objects.filter(user=request.user.pk,type=0).count(),
              'reviews':Review.objects.filter(user=request.user.pk)}

    day = date.today() - user.date_added
    days = datetime.date.fromordinal(day.days)

    for i in company_requests:
        print i.user

    if request.user.type == 'advertiser':
        return render(request, 'beagent/ba-reklamodatel.html', {'user': user,'reviews': review,'on_project':{'d':days.day,'m':days.month,'y':days.year-1},
                                                                'tasks':unverified_tasks, 'company_requests': company_requests})
    else:
        return render(request, 'beagent/ba-agent.html', {'user': user,'reviews': review,'on_project':{'d':days.day,'m':days.month,'y':days.year-1},
                                                         'tasks':tasks_agent,'platforms':platforms, 'invitations':invitations})

@login_required
def edit_profile_blackLists(request):
    page = int(request.GET.get('page',1))
    per_page = int(request.GET.get('per_page',10))
    if request.GET.get('search'):
        search = request.GET.get('search','').split(' ')
        if not search or (type(search) == 'list' and len(search) > 2):
            return render_json(u'Error in search word')
        else:
            if len(search) == 2:
                list_users = User.objects.filter((Q(name=search[0]) & Q(surname=search[1]) | Q(name=search[1]) & Q(surname=search[0]))).values_list('pk', flat=True)
            else:
                list_users = User.objects.filter((Q(name=search[0]) | Q(surname=search[0]))).values_list('pk', flat=True)

            list = UserList.objects.filter(object__in=list_users, user=request.user.pk)
            pagination = createPaginationBlock(page, per_page, list)

            return render(request, 'beagent/ba-agent-profile-blacklist.html', {'request':request, 'count_list':list.count(),'list':list[pagination['offset']:pagination['offset'] + pagination['per_page']],'pag':pagination})

    else:
        list = UserList.objects.filter(user=request.user.pk, type='black')
        pagination = createPaginationBlock(page, per_page, list)
        return render(request, 'beagent/ba-agent-profile-blacklist.html', {'request':request, 'count_list':list.count(),'list':list[pagination['offset']:pagination['offset'] + pagination['per_page']],'pag':pagination})

@login_required
def edit_profile_whiteLists(request):
    page = int(request.GET.get('page',1))
    per_page = int(request.GET.get('per_page',10))
    if request.GET.get('search'):
        search = request.GET.get('search','').split(' ')
        if not search or (type(search) == 'list' and len(search) > 2):
            return render_json(u'Error in search word')
        else:
            if len(search) == 2:
                list_users = User.objects.filter((Q(name=search[0]) & Q(surname=search[1]) | Q(name=search[1]) & Q(surname=search[0]))).values_list('pk', flat=True)
            else:
                list_users = User.objects.filter((Q(name=search[0]) | Q(surname=search[0]))).values_list('pk', flat=True)

            list = UserList.objects.filter(object__in=list_users, user=request.user.pk)
            pagination = createPaginationBlock(page, per_page, list)

        return render(request, 'beagent/ba-reklamodatel-profile-whitelist.html', {'request':request, 'count_list':list.count(),'list':list[pagination['offset']:pagination['offset'] + pagination['per_page']],'pag':pagination})

    if request.user.type == 'advertiser':
        list = UserList.objects.filter(user=request.user.pk, type='white')
        pagination = createPaginationBlock(page, per_page, list)
        return render(request, 'beagent/ba-reklamodatel-profile-whitelist.html', {'request':request, 'count_list':list.count(),'list':list[pagination['offset']:pagination['offset'] + pagination['per_page']],'pag':pagination})

    elif request.user.type == 'agent':
        return redirect(SITE_URL+'cabinet/profile/black_list')

@login_required
def delete_from_list(request,pk):
    list = UserList.objects.filter(pk = pk,user = request.user.pk)
    list.delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def profile_balance(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        val = {}
        for i in request.POST:
            if request.POST[i] == '':
                val[i] = str(datetime.date.today())
            else:
                val[i] = request.POST[i]
        form = DateForm(val)
        if form.is_valid():
            balance = Balance.objects.filter(user=user.pk, date__range=(form.cleaned_data['date_from'], form.cleaned_data['date_to']))
        else:
            print form.errors
    else:
        balance = Balance.objects.filter(user=user.pk)
        print balance
    return render(request, 'beagent/ba-agent-denigi.html', {'user':user, 'balance': balance})

@login_required
def profile_balance_output(request):
    user = User.objects.get(pk=request.user.pk)
    balance = Balance.objects.filter(user=user.pk)
    purses = AgentPurse.objects.filter(user=user.pk,system=1)
    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        post_values = request.POST.copy()
        if request.POST['form'] == 'beznal':
            #безнал
            form = NonCashPaymentsForm(request.POST)
            if form.is_valid():
                post_values['noncash'] = form.save()
                post_values['purse'] = None
                post_values['system'] = PaymentSystem.objects.get(name=request.POST['system'])
            else:
                return render_json({'errors': form.errors, 'status': False})
        else:
            if request.POST['new_purse']:
                post_values['name'] = request.POST['new_purse']
                form = PurseForm(post_values)
                if form.is_valid():
                    post_values['purse'] = AgentPurse.objects.get(name=form.data['name'])
                    post_values['noncash'] = None
                    system = PaymentSystem.objects.get(name=request.POST['system'])
                    post_values['system'] = system
                    if not post_values['purse']:
                        purse = AgentPurse(name=form.data['name'], user=user, system=system)
                        post_values['purse'] = purse.save()
            else:
                post_values['purse'] = AgentPurse.objects.get(pk=int(request.POST['name']))
                post_values['noncash'] = None
                post_values['system'] = PaymentSystem.objects.get(name=request.POST['system'])

        total_sum = float(post_values['sum']) - (float(post_values['sum']) * float(post_values['percent']) / 100)
        transfer = MoneyTransfer(user=user,type='out',total_sum=total_sum,status='unverified')
        form = PaymentsForm(post_values)
        if form.is_valid():
            for field in form.data:
                setattr(transfer, field, form.data[field])
            transfer.save()
        else:
            return render_json({'errors': form.errors, 'status': False})
    return render(request, 'beagent/ba-agent-denigi-vivod.html', {'user':user, 'balance': balance, 'purses':purses})

@login_required
def purses_list(request):
    if request.is_ajax():
        system = PaymentSystem.objects.get(name=request.POST['system'])
        a = render_to_string('beagent/purses_template.html', {'purses':AgentPurse.objects.filter(user=request.user.pk,system=system)})
        return render_json({'result':a,'callback':{'name':'add_html','params':'#purses'}})
    else:
        return None

@login_required
def profile_balance_input(request):
    user = User.objects.get(pk=request.user.pk)
    balance = Balance.objects.filter(user=user.pk)
    purses = AgentPurse.objects.filter(user=user.pk,system=1)

    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        post_values = request.POST.copy()
        if request.POST['form'] == 'beznal':
            #безнал
            form = NonCashPaymentsForm(request.POST)
            if form.is_valid():
                post_values['noncash'] = form.save()
                post_values['purse'] = None
                post_values['system'] = PaymentSystem.objects.get(name=request.POST['system'])
            else:
                return render_json({'errors': form.errors, 'status': False})
        else:
            if request.POST['new_purse']:
                post_values['name'] = request.POST['new_purse']
                form = PurseForm(post_values)
                if form.is_valid():
                    post_values['purse'] = AgentPurse.objects.get(name=form.data['name'])
                    post_values['noncash'] = None
                    system = PaymentSystem.objects.get(name=request.POST['system'])
                    post_values['system'] = system
                    if not post_values['purse']:
                        purse = AgentPurse(name=form.data['name'], user=user, system=system)
                        post_values['purse'] = purse.save()
            else:
                post_values['purse'] = AgentPurse.objects.get(pk=int(request.POST['name']))
                post_values['noncash'] = None
                post_values['system'] = PaymentSystem.objects.get(name=request.POST['system'])

        total_sum = float(post_values['sum']) - (float(post_values['sum']) * float(post_values['percent']) / 100)
        transfer = MoneyTransfer(user=user,type='in',total_sum=total_sum,status='unverified')
        form = PaymentsForm(post_values)
        if form.is_valid():
            for field in form.data:
                setattr(transfer, field, form.data[field])
            transfer.save()
        else:
            return render_json({'errors': form.errors, 'status': False})

    return render(request, 'beagent/ba-reklamodatel-denigi-popolnit.html', {'user':user, 'balance': balance, 'purses':purses})

@login_required
def profile_messages(request):
    page = int(request.GET.get('page',1))
    per_page = int(request.GET.get('per_page',10))
    list = Message.objects.filter(receiver=request.user.pk).order_by('-last_answer')
    pagination = createPaginationBlock(page, per_page, list)

    return render(request, 'beagent/ba-agent-soobshenia.html', {'request':request, 'count_list':list.count(),'list':list[pagination['offset']:pagination['offset'] + pagination['per_page']],'pag':pagination})

@login_required
def profile_view_message(request):
    Message.objects.filter(pk=request.GET['id'],receiver=request.user.pk).update(watched=1)
    return render(request, 'beagent/ba-agent-soobshenia-prosmotr_tiketa.html', {'request':request, 'msg':Message.objects.get(pk=request.GET['id']), 'review':MessageReview.objects.filter(message=request.GET['id'])})

@login_required
def add_msg_review(request):
    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        form = MessageReviewForm(request.POST)
        if form.is_valid():
            msg_review = MessageReview()
            for field in form.cleaned_data:
                setattr(msg_review, field, form.cleaned_data[field])
            msg_review.save()
            Message.objects.filter(pk=form.cleaned_data['message'].pk).update(watched=0)
            return render_json({'redirect': request.META['HTTP_REFERER'], 'status': True})
        else:
            print form.errors
            return render_json({'errors': form.errors, 'status': False})

@login_required
def profile_ask_question(request):

    return render(request, 'beagent/ba-agent-soobshenia-sendform.html', {'request':request})

@login_required
def profile_view_admin_message(request):
    Message.objects.filter(pk=request.GET['id'],receiver=request.user.pk).update(watched=1,last_answer=datetime.datetime.now())
    return render(request, 'beagent/ba-agent-soobshenia-soobshenia_ot_admina.html', {'request':request, 'msg':Message.objects.get(pk=request.GET['id']), 'review':MessageReview.objects.filter(message=request.GET['id'])})

@login_required
def profile_view_tasks(request):
    date_range = None

    page = int(request.GET.get('page',1))
    per_page = int(request.GET.get('per_page',10))
    status = request.GET.get('status','')

    if request.method == 'POST':
        val = {}
        for i in request.POST:
            if request.POST[i] == '':
                val[i] = str(datetime.date.today())
            else:
                val[i] = request.POST[i]
        form = DateForm(val)
        if form.is_valid():
            date_range=(form.cleaned_data['date_from'], form.cleaned_data['date_to'])

    if request.user.type == 'agent':
        if not status:
            if not date_range:
                list = AgentTask.objects.filter(user=request.user.pk).extra(where=["status='performed' OR status='checkout'"])
            else:
                list = AgentTask.objects.filter(user=request.user.pk,date_start__range=date_range).extra(where=["status='performed' OR status='checkout'"])
        else:
            if not date_range:
                list = AgentTask.objects.filter(user=request.user.pk,status=status)
            else:
                list = AgentTask.objects.filter(user=request.user.pk,status=status,date_start__range=date_range)
        pagination = createPaginationBlock(page, per_page, list)

        return render(request, 'beagent/ba-agent-moi_zadachi.html', {'request':request, 'count_list':list.count(),'list':list[pagination['offset']:pagination['offset'] + pagination['per_page']],'pag':pagination})
    else:
        if not status:
            if not date_range:
                list = AgentTask.objects.filter(customer=request.user.pk).extra(where=["status='performed' OR status='payable'"])
            else:
                list = AgentTask.objects.filter(customer=request.user.pk,date_start__range=date_range).extra(where=["status='performed' OR status='payable'"])
        else:
            if not date_range:
                list = AgentTask.objects.filter(customer=request.user.pk,status=status)
            else:
                list = AgentTask.objects.filter(customer=request.user.pk,status=status,date_start__range=date_range)
        pagination = createPaginationBlock(page, per_page, list)
        res = []
        for i in list[pagination['offset']:pagination['offset'] + pagination['per_page']]:
            total_hours = i.date_finish - i.date_start
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            elapsed_hours = i.date_finish - now if i.date_finish > now else i.date_finish - i.date_finish
            res.append({
                'pk':i.pk,
                'campaign_name':i.task.campaign.name,
                'work_type':i.task.work_type,
                'status':i.get_status_display,
                'date_start':i.date_start,
                'last_event':i.last_event,
                'total_hours':total_hours.days*24 + total_hours.seconds/3600,
                'elapsed_hours':elapsed_hours.days*24 + elapsed_hours.seconds/3600,
                'name':i.customer.name,
                'surname':i.customer.surname,
                'rating':i.customer.rating,
                })


        return render(request, 'beagent/ba-reklamodatel-moi_zadachi.html', {'request':request, 'count_list':list.count(),'list':res,'pag':pagination})

@login_required
def pay_task(request):
    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        AgentTask.objects.filter(customer=request.user.pk,id__in=request.POST.getlist('task')).update(status='payable')
        return render_json({'redirect': request.META['HTTP_REFERER'], 'status': True})
    else:
        return render_json({'errors': 'not ajax request', 'status': False})

@login_required
def reject_task(request):
    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        AgentTask.objects.filter(customer=request.user.pk,id__in=request.POST.getlist('task')).update(status='reject')
        return render_json({'redirect': request.META['HTTP_REFERER'], 'status': True})
    else:
        return render_json({'errors': 'not ajax request', 'status': False})

@login_required
def profile_view_task(request):
    return render(request, 'beagent/ba-agent-moi_zadachi-odna_zadacha.html', {'request':request})

@login_required
def profile_companies_list(request):
    pass

@login_required
def profile_add_company(request):
    pass

@login_required
def profile_platforms_list(request):
    pass

@login_required
def profile_add_platform(request):
    pass

@login_required
def profile_activate_platform1(request):
    pass

@login_required
def profile_activate_platform2(request):
    pass

@login_required
def profile_activate_platform3(request):
    pass

@login_required
def profile_platform_options(request):
    pass

@login_required
def profile_paid_platforms(request):
    pass

@login_required
def profile_form_search_company(request):
    pass

@login_required
def profile_view_company(request):
    pass

@login_required
def profile_invites_list(request):
    pass

@login_required
def profile_favourites_list_agentplatform(request):
    pass

@login_required
def profile_form_search_platform(request):
    pass