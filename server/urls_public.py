from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='home_page'),
    path('account/', include('account.user.urls')),
    path('member/', include('membership.urls')),
    path('admin/', admin.site.urls),
]
