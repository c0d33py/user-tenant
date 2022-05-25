
import json
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse


from account.user.tasks import provision_tenant
from membership.forms.organization import OrganizationForm, TenantForm, MembersForm
from membership.models.organization import Organization, Client
from membership.models.member_request import MemberRequest
from django.db.models import Q

User = get_user_model()


def fixtures_data_load(request):

    with open('fixtures/groups.json', encoding='utf-8') as data_file:
        # Convert json string to python object
        data = json.loads(data_file.read())

    # Create model instances for each item
    # items = []
    for item in data:
        pass
        # create model instances...
        # item = YourModel(*item)
        # YourModel.objects.bulk_create(items)

        return JsonResponse({'succes': True}, status=200)

    return JsonResponse({'succes': False, 'errors': []}, status=400)


@login_required
def settings(request, slug):
    obj = get_object_or_404(Client, slug=slug)

    # sent_request = list(
    #     MemberRequest.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
    #     .values_list('from_user_id', flat=True))

    # Global registered active users list
    # Exclude user if this tenant id alread exits in user model obj
    global_user = User.objects.filter(is_active=True).exclude(tenants=obj).exclude(id=obj.owner.id)  # .exclude(pk=)

    # exiting member invite request list
    active_requests = MemberRequest.objects.filter(client=obj).filter(is_active=True)

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
        'active_requests': active_requests,
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
            username = request.user.username
            tenant_name = form.cleaned_data.get('name')
            tenant_slug = tenant_name.lower()
            org = obj

            provision_tenant(tenant_name, tenant_slug, org, username, is_staff=False)
            return redirect('add_org')
    else:
        form = TenantForm()
    return render(request, 'org/_client_form.html', {'form': form})
