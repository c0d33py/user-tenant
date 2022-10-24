from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from account.permissions.models import TenantPermissions

from .models.profile import Profile

User = get_user_model()


@admin.register(TenantPermissions)
class PermAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_staff', 'is_superuser']
    list_filter = ['is_superuser']
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
    )
    filter_horizontal = (
        'groups',
        'user_permissions',
    )


class PermAdmin(admin.TabularInline):
    model = TenantPermissions
    extra = 1
    fieldsets = (
        (_('Permissions'), {'fields': ('is_staff', 'groups',)}),
    )
    filter_horizontal = (
        'groups',
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_verified', 'is_staff', 'is_superuser']
    list_editable = ('is_active',)
    list_filter = ['is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email',)}),
        (_('Tenants & Permissions'), {'fields': ('is_verified', 'is_active', 'tenants',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-id']
    filter_horizontal = ('tenants',)
    inlines = [PermAdmin]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'phone', 'city']
    fieldsets = (
        (_('Profile'), {'fields': ('user', 'image',)}),
        (_('Contact address'),
         {'fields': ('gender', 'birth_date', 'phone', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'country')}),
        (_('Interest'),
         {'fields': ('user_services', 'user_interest', 'is_visitor', 'is_content_creator', 'is_expert',)}),
    )
    filter_horizontal = ('user_services', 'user_interest',)
    search_fields = ['user__username']
