from django import forms
from django.utils.translation import gettext_lazy as _
from membership.models.organization import Organization


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['name']


class TenantForm(forms.Form):
    name = forms.CharField(max_length=100, help_text=_('Put your client name here.'),)

    class Meta:
        fields = ['name']
