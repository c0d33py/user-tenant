from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .views import *
from django.urls import path


urlpatterns = [
    path('', home_page, name='home_page'),
    # path('change-password/', change_password, name='change-password'),
    path('register/', Register, name='signup'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('org/', add_orgniztion, name='add_org'),
    path('client/<int:org_id>/', client_register, name='client_register'),

]
