from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import datetime
from PIL import Image

from .path import file_path
from .mixins import ContactInfoMixIn


User = get_user_model()


class Profile(ContactInfoMixIn):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    image = models.ImageField(
        _('profile image'),
        default='profile/default-profile.jpg',
        upload_to=file_path,
        help_text=_(
            'If user is not set the profile image. '
            'The system automatically add default image for user.'
        ),
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_age(self):
        age = datetime.date.today() - self.birth_date
        return int((age).days / 365.25)
