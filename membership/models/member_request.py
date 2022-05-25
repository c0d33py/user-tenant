from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .organization import Client
from .mixin import TimestampMixin

User = get_user_model()


class MemberRequest(TimestampMixin):
    """ Friend Request model """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client', null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField(_("Message"), blank=True)
    rejected = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True, default=True)

    class Meta:
        app_label = 'membership'
        verbose_name = _('member request')
        verbose_name_plural = _('member requests')

    def __str__(self):
        return self.sender.username

    def accept(self):
        # update both sender and receiver friend list
        client = Client.objects.get(slug=self.client.slug)
        if client:
            client.add_member(self.receiver)
            sender_tenant_list = User.objects.get(pk=self.receiver.pk)
            if sender_tenant_list:
                sender_tenant_list.tenants.add(self.client)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.rejected = timezone.now()
        self.save()
