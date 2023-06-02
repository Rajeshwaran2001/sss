from django.contrib import admin
from .models import issue_list, status_list, service

# Register your models here.

admin.site.register(issue_list)
admin.site.register(status_list)
admin.site.register(service)
