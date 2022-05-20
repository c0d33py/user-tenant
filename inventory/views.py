from django.shortcuts import redirect, render
from django import forms
from .models import Location
from django.contrib.auth.decorators import login_required


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = '__all__'


@login_required
def add_location(request):
    queryset = Location.objects.all()

    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-inventory')
    else:
        form = LocationForm()

    return render(request, 'inven/_location.html', {'form': form, 'location': queryset})
