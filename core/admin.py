from django.contrib import admin
from tenant_users.permissions.models import UserTenantPermissions

# Register your models here.
admin.site.register(UserTenantPermissions)
