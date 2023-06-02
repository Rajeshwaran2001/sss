from django.db import models


# Create your models here.

class branch_user(models.Model):
    user = models.CharField(max_length=50, null=True, blank=True)
    branch = models.ForeignKey('utility.branch', on_delete=models.SET_NULL, blank=False, null=True)
    pc = models.ForeignKey('utility.device_list', on_delete=models.SET_NULL, blank=False, null=True)
