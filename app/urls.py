from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('auth', views.auth, name='auth'),
    path('logout/', views.logout, name='logout'),
    path('', views.landing, name='landing'),
    path('index', views.index, name='index'),
    path('success/', views.success, name='success'),

    # path('success', success, name='success'),

]