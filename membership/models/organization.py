from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_tenants.models import DomainMixin

from account.user.models import TenantBase

User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'membership'
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    def __str__(self):
        return self.name


class Client(TenantBase):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    members = models.ManyToManyField(User, blank=True, related_name='members')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='manager')

    auto_create_schema = True
    auto_drop_schema = True

    class Meta:
        app_label = 'membership'
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    # has admin
    def has_admin(self):
        return self.owner

    # has manager
    def has_manager(self):
        return self.manager

    # member Count
    def member_count(self):
        return self.members.all().count()

    # add member
    def add_member(self, account):
        if not account in self.members.all():
            self.members.add(account)
            self.save()

    # remove member
    def remove_member(self, account):
        if account in self.members.all():
            self.members.remove(account)
            self.save()

    # is mutual member
    def is_mutual_member(self, member):
        if member in self.members.all():
            return True
        return False

    # TODO member role list


class Domain(DomainMixin):

    class Meta:
        app_label = 'membership'
        verbose_name = _('domain')
        verbose_name_plural = _('domains')
