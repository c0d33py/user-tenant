from pyexpat import model
from django import forms
from django.utils.translation import gettext_lazy as _
from membership.models.organization import Organization, Client


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['name']


class TenantForm(forms.Form):
    name = forms.CharField(max_length=100, help_text=_('Put your client name here.'),)

    class Meta:
        fields = ['name']


class MembersForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, help_text=_('Put your client name here.'),)

    class Meta:
        model = Client
        fields = [
            'name',
            'owner',
            'manager',
            'members',
            'paid_until',
            'on_trial',
        ]
