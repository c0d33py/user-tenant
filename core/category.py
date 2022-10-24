from django.contrib.auth import get_user_model
from django.db import models

from .mixins import UserTrackTimeStampMixin

User = get_user_model()


class Category(UserTrackTimeStampMixin):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class City(UserTrackTimeStampMixin):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Tags(UserTrackTimeStampMixin):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
