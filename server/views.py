from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from membership.models.member_request import MemberRequest


@login_required
def index(request):
    request_list = MemberRequest.objects.filter(receiver=request.user).filter(is_active=True)

    context = {
        'request_list': request_list,
    }
    return render(request, '_index.html', context)


''
