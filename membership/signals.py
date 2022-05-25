from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models.organization import Client, ClientProfile

User = get_user_model()


@receiver(post_save, sender=Client)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ClientProfile.objects.create(client=instance)


@receiver(post_save, sender=Client)
def save_profile(sender, instance, **kwargs):
    instance.clientprofile.save()
