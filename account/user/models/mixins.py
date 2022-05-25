from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampMixin(models.Model):
    '''Timestamp Mixin'''

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CommonMixin(models.Model):
    '''User Commen'''

    name = models.CharField(_('Name'), max_length=100)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this attr should be treated as active. '
            'Unselect this instead of deleting object.'
        ),
    )

    class Meta:
        abstract = True


class ContactInfoMixIn(models.Model):
    '''Contact.'''

    address_1 = models.CharField(max_length=70, blank=True, verbose_name=_('Address Line 1'))
    address_2 = models.CharField(max_length=70, blank=True, verbose_name=_('Address Line 2'))
    city = models.CharField(max_length=70, blank=True, verbose_name=_('City'))
    state = models.CharField(max_length=70, blank=True, verbose_name=_('State/Province'))
    zip_code = models.CharField(max_length=20, blank=True, verbose_name=_('Zip Code'))
    country = models.CharField(max_length=70, blank=True, verbose_name=_('Country'))
    website = models.URLField(blank=True, verbose_name=_('Website'))
    phone = models.CharField(max_length=30, blank=True,  verbose_name=_('Phone Number'))

    class Meta:
        abstract = True

    def get_cszc(self):
        if all([
            self.city,
            self.state,
            self.zip_code,
            self.country,
        ]):
            return f'{self.city}, {self.state}. {self.zip_code}. {self.country}'
