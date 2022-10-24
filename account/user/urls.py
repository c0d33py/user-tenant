from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import path

from .api.views import *
from .views import *


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_func


urlpatterns = [
    path('profile/', profile, name='profile'),
    path('register/', unauthenticated_user(Register), name='signup'),
    path('login/', unauthenticated_user(LoginView.as_view(template_name='user/login.html')), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('change-password/', change_password, name='change-password'),
]
