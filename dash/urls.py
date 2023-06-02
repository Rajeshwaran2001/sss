from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('update/<int:pk>', views.edit_service, name="edit_service"),
    path('change_password', views.change_password, name='change'),
    path('signup', views.Admin_signup_view, name='signup'),
    path('asset/', views.asset, name='asset'),
    path('edit/<int:pk>', views.edit_asset, name="edit_asset"),
    path('delete/<int:pk>', views.delete_asset, name="delete_asset"),
]
