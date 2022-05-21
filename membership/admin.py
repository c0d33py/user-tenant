from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from membership.models.organization import Organization, Client, Domain
from membership.models.member_request import MemberRequest


admin.site.register(Organization)
admin.site.register(MemberRequest)


class DomainInline(admin.TabularInline):
    model = Domain
    max_num = 3


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'paid_until')
    inlines = [DomainInline]
