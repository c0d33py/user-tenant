
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from membership.forms.organization import OrganizationForm, TenantForm
from membership.models.organization import Organization
from membership.tasks import provision_tenant


@login_required
def settings(request):
    return render(request, 'member/settings.html')


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
