from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('inventory.urls')),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
]
