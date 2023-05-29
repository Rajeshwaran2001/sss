from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('home', views.home, name='home'),
    path('change_password', views.change_password, name='change'),
    path('signup', views.Admin_signup_view, name='signup'),
]
