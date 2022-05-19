from .models import Orgnization
from django.contrib import admin
from django.contrib.auth import get_user_model
from tenant_users.permissions.models import UserTenantPermissions
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django_tenants.admin import TenantAdminMixin
from .models import Client, Domain
from .forms import UserAdminCreationForm, UserAdminChangeForm
User = get_user_model()

admin.site.register(Orgnization)


@admin.register(UserTenantPermissions)
class PermAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Profile'), {'fields': ('profile',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
    )
    filter_horizontal = (
        'groups',
        'user_permissions',
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    list_editable = ('is_active',)
    list_filter = ['is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active',)}),
        (_('Tenants'), {'fields': ('tenants',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-id']
    filter_horizontal = ('tenants',)


class DomainInline(admin.TabularInline):
    model = Domain
    max_num = 3


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'paid_until')
    inlines = [DomainInline]
