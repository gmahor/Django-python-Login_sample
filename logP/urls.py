from django.urls import path

from . import views

# Password Change
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name='homepage'),
    path('signup', views.handleSignup, name='handleSignup'),
    path('login', views.handleLogin, name='handleLogin'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('change_pass/', views.change_pass, name='change_pass'),

]
