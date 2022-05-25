from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TreeMixin(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserTrackMixin(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created_by', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_updated_by', null=True, blank=True)

    class Meta:
        abstract = True
