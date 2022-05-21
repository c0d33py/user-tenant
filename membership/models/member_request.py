from django.db import models
from .organization import Client
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .mixin import TimestampMixin
User = get_user_model()


class MemberRequest(TimestampMixin):
    """ Friend Request model """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=True, default=True)

    class Meta:
        app_label = 'membership'
        verbose_name = _('member request')
        verbose_name_plural = _('member requests')

    def __str__(self):
        return self.sender.email

    def accept(self):
        # update both sender and receiver friend list
        receiver_member_list = Client.objects.get(user=self.receiver)
        if receiver_member_list:
            receiver_member_list.add_member(self.sender)
            sender_member_list = Client.objects.get(user=self.sender)
            if sender_member_list:
                sender_member_list.add_member(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()
