from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('change_password', views.change_password, name='change'),
    path('signup', views.Admin_signup_view, name='signup'),
    path('asset/', views.asset, name='asset')
]
