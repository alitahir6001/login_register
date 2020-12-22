from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('process', views.process), # aka the registration process
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout)
]
