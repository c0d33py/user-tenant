from urllib import request
from django_tenants.middleware.main import TenantMainMiddleware
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import Http404
from django.urls import set_urlconf, clear_url_caches
from django_tenants.urlresolvers import get_subfolder_urlconf
from django_tenants.utils import (
    get_public_schema_name,
    get_tenant_model,
    get_tenant_domain_model,
)
from django.utils.deprecation import MiddlewareMixin

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from django.contrib import auth


class TenantInactiveMiddleware(TenantMainMiddleware):
    def __init__(self, get_response):
        self.get_response = get_response

    # def __call__(self, request):
    #     response = self.get_response(request)
    #     UserModel = get_user_model()
    #     TenantModel = get_tenant_model()
    #     public_schema_name = get_public_schema_name()

    #     users = UserModel.objects.filter(tenants=request.user.id)
    #     # for i in users:
    #     #     print(f'{i}- {i.tenants.all()}')

    #     return response

    def get_tenant(self, domain_model, hostname):
        tenant = super().get_tenant(domain_model, hostname)
        if not tenant.on_trial:
            raise self.TENANT_NOT_FOUND_EXCEPTION("Tenant is inactive")
        return tenant

    def process_request(self, request):
        # connection.set_schema_to_public()
        hostname = self.hostname_from_request(request)
        domain_model = get_tenant_domain_model()
        UserModel = get_user_model()

        try:
            tenant = self.get_tenant(domain_model, hostname)
        except domain_model.DoesNotExist:
            self.no_tenant_found(request, hostname)
            return

        users = UserModel.objects.filter(tenants=tenant)
        print(request.user)
