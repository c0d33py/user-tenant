from django.urls import path
from membership.views.organization import *
from membership.views.members import *


urlpatterns = [
    # Organization
    path('org/', add_orgniztion, name='add_org'),
    path('client/<int:org_id>/', client_register, name='client_register'),
    path('settings/<slug:slug>/', settings, name='settings'),
    path('list/', member_list_view, name='member_list_view'),

    # request for member (AJAX)
    path('mrq/', send_friend_request, name='send_friend_request'),

]
