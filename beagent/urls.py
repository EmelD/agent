# coding: utf-8

from django.conf.urls import patterns, url
from beagent_project.settings import LOCAL, MEDIA_ROOT
from beagent.views import admin, common, agent

urlpatterns = patterns('',
    url(r'^$', common.index, name='index'),
    url(r'^cabinet/profile/type/switch', common.switch_profile_type),
    url(r'^cabinet/signup', common.signup),
    url(r'^cabinet/signin', common.signin),
    url(r'^cabinet/signout', common.signout),
    url(r'^cabinet/profile/edit', common.edit_profile),
    url(r'^cabinet/profile/change_password$', common.change_password),
    url(r'^cabinet/profile/black_list$', common.edit_profile_blackLists),
    url(r'^cabinet/profile/white_list$', common.edit_profile_whiteLists),
    url(r'^cabinet/profile$', common.profile),
    url(r'^delete/from_list/(?P<pk>\d+)$', common.delete_from_list),
    url(r'^advertiser', agent.view_advertiser),

    url(r'^cabinet/balance$', common.profile_balance),
    url(r'^cabinet/balance/input$', common.profile_balance_input),
    url(r'^cabinet/balance/output$', common.profile_balance_output),

    url(r'^platforms', agent.view_agent_platforms),
    url(r'^platform', agent.show_agent_platform),
    url(r'^redaction_platform', agent.redaction_agent_platform),
    url(r'^change_status_platform', agent.agent_platform_change_status),
    url(r'^tasks', common.profile_view_tasks),
    url(r'^view_tasks', common.profile_view_task),
    url(r'^invitations', agent.view_agent_invitations),
    url(r'^invitation', agent.profile_view_company),
    url(r'^reject_invitation', agent.reject_invitation),
    url(r'^approve_invitation', agent.approve_invitation),
    url(r'^pay_task', common.reject_task),
    url(r'^reject_task', common.pay_task),
    url(r'^messages', common.profile_messages),
    url(r'^admin_message', common.profile_view_admin_message),
    url(r'^msg_review', common.add_msg_review),
    url(r'^message', common.profile_view_message),
    url(r'^ask', common.profile_ask_question),
    url(r'^purses', common.purses_list),
    url(r'^activate_platform', agent.agent_activate_platform),

    url(r'^admin',admin.admin),
    url(r'^admin',admin.admin_platforms_list),
    url(r'^admin',admin.admin_view_platform),
    url(r'^admin',admin.admin_users_list),
    url(r'^admin',admin.admin_view_user),
    url(r'^admin',admin.admin_tasks_list),
    url(r'^admin',admin.admin_view_task),
    url(r'^admin',admin.admin_new_tickets),
    url(r'^admin',admin.admin_support_tickets_list),
    url(r'^admin',admin.admin_complaints_list),
    url(r'^admin',admin.admin_disputes_list),
    url(r'^admin',admin.admin_view_dispute),
    url(r'^admin',admin.admin_view_ticket),
    url(r'^admin',admin.admin_view_complaint),
    url(r'^admin',admin.admin_companies_list),
    url(r'^admin',admin.admin_platforms_list),
    url(r'^admin',admin.admin_edit_platform),
    url(r'^admin',admin.admin_arrival_money_list),
    url(r'^admin',admin.admin_outflow_money_list),
    url(r'^admin',admin.admin_history_financial_transactions),
    url(r'^admin',admin.admin_view_process_money_output),
    url(r'^admin',admin.admin_management_reasons_fail),
    url(r'^admin',admin.admin_requests_output_list),
    )
if LOCAL:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT
        })
    )

"""
    url(r'^cabinet/profile', views.edit_profile_bwlists),
    url(r'^cabinet/profile', views.profile_balance),
    url(r'^cabinet/profile', views.profile_balance_output),
    url(r'^cabinet/profile', views.profile_balance_input),
    url(r'^cabinet/profile', views.profile_messages),
    url(r'^cabinet/profile', views.profile_asq_question),
    url(r'^cabinet/profile', views.profile_view_message),
    url(r'^cabinet/profile', views.profile_view_admin_message),
    url(r'^cabinet/profile', views.profile_view_tasks),
    url(r'^cabinet/profile', views.profile_view_task),
    url(r'^cabinet/profile', views.profile_companies_list),
    url(r'^cabinet/profile', views.profile_add_company),
    url(r'^cabinet/profile', views.profile_platforms_list),
    url(r'^cabinet/profile', views.profile_add_platform),
    url(r'^cabinet/profile', views.profile_activate_platform1),
    url(r'^cabinet/profile', views.profile_activate_platform2),
    url(r'^cabinet/profile', views.profile_activate_platform3),
    url(r'^cabinet/profile', views.profile_platform_options),
    url(r'^cabinet/profile', views.profile_paid_platforms),
    url(r'^cabinet/profile', views.profile_form_search_company),
    url(r'^cabinet/profile', views.profile_view_company),
    url(r'^cabinet/profile', views.profile_invites_list),
    url(r'^cabinet/profile', views.profile_favourites_list_agentplatform),
    url(r'^cabinet/profile', views.profile_form_search_platform),
    """