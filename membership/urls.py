from django.urls import path
from membership.views.organization import *
from membership.views.members import *


urlpatterns = [
    # Organization
    path('org/', add_orgniztion, name='add_org'),
    path('client/<int:org_id>/', client_register, name='client_register'),
]
