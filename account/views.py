import imp
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistration, OrgnizationForm, TenantForm
from .models import Orgnization
from .models import Client, Domain
from .tasks import provision_tenant


@login_required
def home_page(request):
    org_query = Orgnization.objects.filter(created_by=request.user).first()

    return render(request, 'user/_index.html', {'org_query': org_query})


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


@login_required
def add_orgniztion(request):
    org = Orgnization.objects.filter(created_by=request.user).first()
    if request.method == 'POST':
        form = OrgnizationForm(request.POST)
        if form.is_valid():
            orgnization = form.save(commit=False)
            orgnization.created_by = request.user
            orgnization.save()
            return redirect('/')
    else:
        form = OrgnizationForm()
        context = {'form': form, 'org': org}

    return render(request, 'user/_orginzation.html', context)


@login_required
def client_register(request, org_id):
    obj = get_object_or_404(Orgnization, id=org_id)

    if request.method == 'POST':
        form = TenantForm(request.POST)

        if form.is_valid():
            user_email = request.user.email
            tenant_name = form.cleaned_data.get('name')
            tenant_slug = tenant_name.lower()
            org = obj

            provision_tenant(tenant_name, tenant_slug, org, user_email, is_staff=False)
            return redirect('/')
    else:
        form = TenantForm()
    return render(request, 'user/_client_registeration.html', {'form': form})
