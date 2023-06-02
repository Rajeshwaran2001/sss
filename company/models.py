from django.db import models
from user.models import branch_user
from utility.models import device_list


# Create your models here.
class issue_list(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class status_list(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class service(models.Model):
    user = models.ForeignKey(branch_user, on_delete=models.SET_NULL, blank=False, null=True)
    issue = models.ForeignKey(issue_list, on_delete=models.SET_NULL, blank=False, null=True)
    pc = models.ForeignKey(device_list, on_delete=models.SET_NULL, blank=False, null=True)
    status = models.BooleanField(default=False)
    resolution = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.issue)
