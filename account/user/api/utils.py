from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

''' user model '''
User = get_user_model()


def get_host(request):
    ''' get domain host with schema '''
    return request.scheme + '://' + request.META['HTTP_HOST']


def decode_uidb64(uidb64):
    ''' function to decode uidb64 and token '''
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return user


def get_user_by_token(token):
    ''' function to get user by token '''
    try:
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        user = None
    return user


def get_user_by_email(email):
    ''' function to get user by email '''
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None
    return user


def get_user_by_username(username):
    ''' function to get user by username '''
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user


def get_user_by_id(id):
    ''' function to get user by id '''
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        user = None
    return user
