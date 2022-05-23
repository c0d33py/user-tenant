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
    path('friend_request_accept/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    path('friend_remove/', remove_friend, name='remove-friend'),
    path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
    path('load-data/', fixtures_data_load, name='load_data'),

]
