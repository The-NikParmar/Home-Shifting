"""
URL configuration for home_shifting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.partner_index, name='partner_index'),
    path('profile', views.profile, name='profile'),
    path('Mywalllet', views.Mywallet, name='Mywalllet'),
    path('dcontact', views.dcontact, name='dcontact'),
    path('withdrawal_funds', views.withdrawal_funds, name='withdrawal_funds'),
    path('update', views.update, name='update'),
    path('plogin', views.plogin, name='plogin'),
   
    
]