from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('home', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('', views.login_user, name='login'),
    path('change_password', views.change_password, name='change'),
    path('logout', views.logout, name='logout')
]
