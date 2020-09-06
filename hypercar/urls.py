"""hypercar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView
from tickets.views import GetTicket, user_menu, Processing, welcome, NextTicket

urlpatterns = [
    path('welcome/', welcome),
    path('menu/', user_menu),
    path('processing', Processing.as_view()),
    path('next', NextTicket.as_view()),
    path('get_ticket/<service>/', GetTicket.as_view()),
    path('', RedirectView.as_view(url='menu/')),
    path('processing/', RedirectView.as_view(url='/processing')),
    path('next/', RedirectView.as_view(url='/next')),
]
