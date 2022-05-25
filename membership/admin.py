from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django.utils.translation import gettext_lazy as _

from membership.models.organization import Organization, Client, ClientProfile, Domain
from membership.models.member_request import MemberRequest


@admin.register(Organization)
class OrgAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'logo', 'phone', 'city']
    fieldsets = (
        (_('Organization'), {'fields': ('created_by', 'name', 'logo',)}),
        (_('Address'), {'fields': (
            'phone',
            'address_1',
            'address_2',
            'state',
            'zip_code',
            'city',
            'country',
            'website',
        )}),
    )


@admin.register(MemberRequest)
class MemberRequestAdmin(admin.ModelAdmin):
    list_display = ['client', 'sender', 'receiver', 'is_active', 'rejected']
    list_filter = ['is_active']
    fieldsets = (
        (_('Request'), {'fields': ('client', 'sender', 'receiver', 'message',)}),
        (_('Status'), {'fields': ('is_active', 'rejected',)}),
    )


class DomainInline(admin.TabularInline):
    model = Domain
    max_num = 3


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'owner', 'organization', 'paid_until', 'on_trial', 'created')
    list_filter = ['name', 'owner', 'organization']
    fieldsets = (
        (_('Client'), {'fields': ('organization', 'schema_name', 'name',  'slug',)}),
        (_('Members'), {'fields': ('owner', 'manager', 'members',)}),
        (_('Status'), {'fields': ('paid_until', 'on_trial', 'created', 'modified',)}),
    )
    filter_horizontal = (
        'members',
    )
    inlines = [DomainInline]


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['client', 'logo', 'phone', 'email', 'phone', 'city']
    fieldsets = (
        (_('Client'), {'fields': ('client', 'logo',)}),
        (_('Social'), {'fields': (
            'email',
            'facebook',
            'youtube',
            'twitter',
            'insta',
            'tiktok',
            'description',
        )}),
        (_('Address'), {'fields': (
            'phone',
            'address_1',
            'address_2',
            'state',
            'zip_code',
            'city',
            'country',
            'website',
        )}),
    )
