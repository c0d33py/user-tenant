from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.permissions.functional import tenant_cached_property


class PermissionsMixinFacade(object):
    """
    This class is designed to shim the PermissionMixin class functions and
    delegate them down to the correct linked (based on the current schema)
    tenant permissions since we don't handle them in the user like stock
    django does. This is designed to be inherited from by the AUTH_USER_MODEL
    """

    class Meta(object):
        abstract = True

    # This will throw a DoesNotExist exception if there is no tenant
    # permissions matching the current schema, which means that this
    # user has no authorization, so we catch this exception and return
    # the appropriate False or empty set
    @tenant_cached_property
    def tenant_perms(self):
        return TenantPermissions.objects.get(
            user_id=self.id,
        )

    def has_tenant_permissions(self):
        try:
            self.tenant_perms
            return True
        except TenantPermissions.DoesNotExist:
            return False

    @tenant_cached_property
    def is_staff(self):
        try:
            return self.tenant_perms.is_staff
        except TenantPermissions.DoesNotExist:
            return False

    @tenant_cached_property
    def is_superuser(self):
        try:
            return self.tenant_perms.is_superuser
        except TenantPermissions.DoesNotExist:
            return False

    def get_group_permissions(self, obj=None):
        try:
            return self.tenant_perms.get_group_permissions(obj)
        except TenantPermissions.DoesNotExist:
            return set()

    def get_all_permissions(self, obj=None):
        try:
            return self.tenant_perms.get_all_permissions(obj)
        except TenantPermissions.DoesNotExist:
            return set()

    def has_perm(self, perm, obj=None):
        try:
            return self.tenant_perms.has_perm(perm, obj)
        except TenantPermissions.DoesNotExist:
            return False

    def has_perms(self, perm_list, obj=None):
        try:
            return self.tenant_perms.has_perms(perm_list, obj)
        except TenantPermissions.DoesNotExist:
            return False

    def has_module_perms(self, app_label):
        try:
            return self.tenant_perms.has_module_perms(app_label)
        except TenantPermissions.DoesNotExist:
            return False


class AbstractBaseUserFacade(object):
    """
    This class is designed to shim functions on the authorization model
    that are actually part of the authentication model. Auth backends
    expect the models to be combined, but we separate them so we can
    have single authentication across the system, but have per
    tenant permissions
    """

    class Meta(object):
        abstract = True

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def is_anonymous(self):
        return False


class TenantPermissions(PermissionsMixin, AbstractBaseUserFacade):
    """This class serves as the authorization model (permissions) per-tenant.

    We keep all of the global user user information in the public tenant
    schema including authentication aspects. See Useruser model.
    """

    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID',
    )

    # The user stores all of the common information between
    # tenants for a user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this tenants admin site.',
        ),
    )

    def __str__(self):
        """Return string representation."""
        return str(self.user)