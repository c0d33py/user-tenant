from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .mixins import CommonMixin, ContactInfoMixin, TimestampMixin
from .path import file_path

User = get_user_model()


class UserInterest(CommonMixin, TimestampMixin):
    '''User Interest'''

    class Meta:
        app_label = 'account'

    def __str__(self):
        return self.name


class UserServices(CommonMixin, TimestampMixin):
    '''User Services'''

    class Meta:
        app_label = 'account'

    def __str__(self):
        return self.name


class Profile(ContactInfoMixin):
    '''User Profile'''

    GENDER_CHOICES = (
        ('male', 'Male',),
        ('female', 'Female',),
        ('others', 'others',),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=100, blank=True)
    user_services = models.ManyToManyField(UserServices, related_name='services', blank=True)
    user_interest = models.ManyToManyField(UserInterest, related_name='interest', blank=True)
    is_visitor = models.BooleanField(default=True)
    is_content_creator = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)

    image = models.ImageField(
        _('profile image'),
        default='default/default-profile.jpg',
        upload_to=file_path,
        help_text=_(
            'If user is not set the profile image. '
            'The system automatically add default image for user.'
        ),
    )

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'account'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserExperience(TimestampMixin):
    '''User Experience'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=100, verbose_name=_('Job Title'))
    orgnization = models.CharField(max_length=100, verbose_name=_('Organization'))
    join_date = models.DateField(auto_now=False, verbose_name=_('Join Date'))
    end_date = models.DateField(auto_now=False, verbose_name=_('End Date'))
    currently_working = models.BooleanField(
        default=False,
        help_text=_('If user is currently working in this organization.')
    )

    class Meta:
        app_label = 'account'
        verbose_name = _('user experience')
        verbose_name_plural = _('user experiences')

    def __str__(self):
        return self.user.username


class UserEducation(TimestampMixin):
    '''User Education'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100, verbose_name=_('Degree'))
    institute = models.CharField(max_length=100, verbose_name=_('Institute'))
    start_from = models.DateField(auto_now=False, verbose_name=_('Join Date'))
    end_at = models.DateField(auto_now=False, verbose_name=_('End Date'))
    currently_studying = models.BooleanField(
        default=False,
        help_text=_('If user is currently studying in this institute.')
    )

    class Meta:
        app_label = 'account'
        verbose_name = _('user education')
        verbose_name_plural = _('user educations')

    def __str__(self):
        return self.user.username


class UserSkill(TimestampMixin):
    '''User Skill'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill')
    skill = models.CharField(max_length=100, verbose_name=_('Skill'))

    class Meta:
        app_label = 'account'
        verbose_name = _('user skill')
        verbose_name_plural = _('user skills')

    def __str__(self):
        return self.user.username


class UserSocialMedia(TimestampMixin):
    '''User Social Media'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_media')
    facebook = models.URLField(max_length=100, verbose_name=_('Facebook'), blank=True)
    twitter = models.URLField(max_length=100, verbose_name=_('Twitter'), blank=True)
    linkedin = models.URLField(max_length=100, verbose_name=_('Linkedin'), blank=True)
    instagram = models.URLField(max_length=100, verbose_name=_('instagram'), blank=True)
    youtube = models.URLField(max_length=100, verbose_name=_('Youtube'), blank=True)
    website = models.URLField(blank=True, verbose_name=_('Website'))

    class Meta:
        app_label = 'account'
        verbose_name = _('user social media')
        verbose_name_plural = _('user social medias')

    def __str__(self):
        return self.user.username
