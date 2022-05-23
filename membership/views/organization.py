
from multiprocessing import context, managers
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from membership.forms.organization import OrganizationForm, TenantForm, MembersForm
from membership.models.organization import Organization, Client
from membership.models.member_request import MemberRequest
from membership.tasks import provision_tenant
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def settings(request, slug):
    current_user = request.user
    obj = get_object_or_404(Client, slug=slug)
    # Global registered active users list
    global_user = User.objects.filter(is_active=True).exclude(id=obj.owner.id)
    # exiting member invite request list
    account = User.objects.get(pk=current_user.id)
    if account == current_user:
        active_requests = MemberRequest.objects.filter(receiver=obj.owner).filter(receiver=obj.manager).filter(is_active=True)

    # Tenant update Form TODO
    if request.method == 'POST':
        form = MembersForm(request.POST, instance=obj)
        if form.is_valid():
            pass
    else:
        form = MembersForm(instance=obj)
    context = {
        'object': obj,
        'form': form,
        'global_user': global_user,
        'active_requests': active_requests
    }

    return render(request, 'member/settings.html', context)


@login_required
def add_orgniztion(request):
    org = Organization.objects.filter(created_by=request.user).first()
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_by = request.user
            organization.save()
            return redirect('add_org')
    else:
        form = OrganizationForm()
        context = {'form': form, 'org_query': org}

    return render(request, 'org/_orginzation.html', context)


@login_required
def client_register(request, org_id):
    obj = get_object_or_404(Organization, id=org_id)

    if request.method == 'POST':
        form = TenantForm(request.POST)

        if form.is_valid():
            user_email = request.user.email
            tenant_name = form.cleaned_data.get('name')
            tenant_slug = tenant_name.lower()
            org = obj

            provision_tenant(tenant_name, tenant_slug, org, user_email, is_staff=False)
            return redirect('add_org')
    else:
        form = TenantForm()
    return render(request, 'org/_client_form.html', {'form': form})
