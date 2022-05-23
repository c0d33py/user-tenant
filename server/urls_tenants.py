from django.urls import path, include
from django.contrib.auth import views as auth_views
from membership.views.organization import settings

urlpatterns = [
    path('', include('blog.urls')),
    path('settings/<slug:slug>/', settings, name='settings'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
]
