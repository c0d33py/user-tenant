from django.db import models

from db.mixins import UserTrackTimeStampMixin


class Blog(UserTrackTimeStampMixin):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
