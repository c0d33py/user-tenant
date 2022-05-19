from importlib.resources import path
from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('', add_location, name='add-inventory'),
    # path('rster/', add_location, name='signup'),
]
