from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_tenants.models import DomainMixin
from PIL import Image

from account.user.models import TenantBase
from account.user.models.mixins import ContactInfoMixin, TimestampMixin

User = get_user_model()


class Organization(ContactInfoMixin, TimestampMixin):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    logo = models.ImageField(
        upload_to='organization/logo/',
        default='default/default-log.png',
    )

    class Meta:
        app_label = 'membership'
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Organization, self).save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.logo.path)


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


class ClientProfile(ContactInfoMixin):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    logo = models.ImageField(
        upload_to='client/logo/',
        default='default/default-log.png',
    )
    email = models.EmailField(blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    youtube = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    insta = models.CharField(max_length=255, blank=True)
    tiktok = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        app_label = 'membership'
        verbose_name = _('clients profile')
        verbose_name_plural = _('clients profiles')

    def __str__(self):
        return self.client.name

    def save(self, *args, **kwargs):
        super(ClientProfile, self).save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.logo.path)
