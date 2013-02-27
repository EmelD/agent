# -*- coding: utf-8 -*-

from beagent.decorators import login_required
from django.shortcuts import redirect
from beagent.models import User, Invitation, AdvertisingPlatform, RequestForCompany, AgentTask
from beagent.utils import render, render_json, createPaginationBlock
from beagent.forms import LinkForm
from django.core.urlresolvers import reverse

@login_required
def view_agent_platforms(request):
    if request.user.type == 'agent':
        page = int(request.GET.get('page',1))
        per_page = int(request.GET.get('per_page',10))
        status = request.GET.get('status','')

        res = []
        if status:
            list = AdvertisingPlatform.objects.filter(user=request.user.pk,status=status)
        else:
            list = AdvertisingPlatform.objects.filter(user=request.user.pk)
        pagination = createPaginationBlock(page, per_page, list)

        for i in list[pagination['offset']:pagination['offset'] + pagination['per_page']]:
            count = Invitation.objects.filter(status='new',platform=i.id).count()
            res.append({
                    'id':i.id,
                    'inventation':count,
                    'address':i.address,
                    'type':i.type,
                    'status':i.status,
                })

        return render(request, 'beagent/ba-agent-moi_ploshadki.html', {'request':request, 'count_list':list.count(),'result':res,'pag':pagination})
    else:
        return render(request, 'beagent/404.html')

@login_required
def show_agent_platform(request):
    platform = request.GET.get('id','')
    if request.user.type == 'agent' or platform == '' :
        return render(request, 'beagent/ba-agent-moi_ploshadki-prosmotr.html', {'request':request})
    else:
        return render(request, 'beagent/404.html')

@login_required
def redaction_agent_platform(request):
    platform = request.GET.get('id','')
    if request.user.type == 'agent' or platform == '' :
        return render(request, 'beagent/ba-agent-moi_ploshadki-dobavlenie.html', {'request':request})
    else:
        return render(request, 'beagent/404.html')

@login_required
def agent_platform_change_status(request):
    platform = request.GET['platform']
    status = request.GET['status']
    AdvertisingPlatform.objects.filter(user=request.user.pk,pk=platform).exclude(status='activation').update(status=status)
    return redirect(request.META['HTTP_REFERER'])

@login_required
def view_agent_invitations(request):
    if request.user.type == 'agent':
        page = int(request.GET.get('page',1))
        per_page = int(request.GET.get('per_page',10))

        res = []
        balance = 0

        platforms = AdvertisingPlatform.objects.filter(user=request.user.pk)
        list = Invitation.objects.filter(platform__in=platforms,status='new')
        pagination = createPaginationBlock(page, per_page, list)

        for i in list:
            balance += i.task.sum

        for i in list[pagination['offset']:pagination['offset'] + pagination['per_page']]:
            res.append({
                'id':i.pk,
                'campaign':i.campaign.name,
                'balance':i.task.sum,
                'platform':i.platform.address,
                'platform_type':i.platform.type,
                'sender_name':i.campaign.user.name,
                'sender_surname':i.campaign.user.surname,
                'sender_rating':i.campaign.user.rating,
                'task':i.task.work_type,
            })
        return render(request, 'beagent/ba-agent-priglashenia.html', {'request':request, 'count_list':list.count(),'result':res,'pag':pagination,'balance':balance})
    else:
        return render(request, 'beagent/404.html')

@login_required
def approve_invitation(request):
    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        platforms = AdvertisingPlatform.objects.filter(user=request.user.pk)
        Invitation.objects.filter(platform__in=platforms,id__in=request.POST.getlist('campaign')).update(status='approve')
        return render_json({'redirect': request.META['HTTP_REFERER'], 'status': True})
    else:
        return render_json({'errors': 'not ajax request', 'status': False})

@login_required
def reject_invitation(request):
    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        platforms = AdvertisingPlatform.objects.filter(user=request.user.pk)
        Invitation.objects.filter(platform__in=platforms,id__in=request.POST.getlist('campaign')).update(status='reject')
        return render_json({'redirect': request.META['HTTP_REFERER'], 'status': True})
    else:
        return render_json({'errors': 'not ajax request', 'status': False})

@login_required
def profile_view_company(request):
    pass

@login_required
def agent_activate_platform(request):
    if request.is_ajax() or ('meta' in request.POST and request.POST['meta'] == 'ajax'):
        form = LinkForm(request.POST['link'])
        if form.is_valid():
            AdvertisingPlatform.objects.filter(user=request.user.pk, pk=request.GET['platform']).update(activated_link=form.data['link'])
            return render_json({'redirect': reverse('beagent.views.agent.platforms'), 'status': True})
        else:
            return render_json({'errors': form.errors, 'status': False})
    return render(request, 'beagent/ba-agent-moi_ploshadki-aktivacia.html', {'request':request, 'platform':request.GET['platform']})

@login_required
def view_advertiser(request):
    if request.user.type == 'agent':
        return render(request, '404.html')
    else:
        return render(request, '404.html')