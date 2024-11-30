from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
