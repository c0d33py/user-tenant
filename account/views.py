from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistration


def Register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} Account has been created!')
            return redirect('login')
    else:
        form = UserRegistration()
    return render(request, 'user/register.html', {'form': form})
