from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, null=False, blank=False)
    is_Active = models.BooleanField(default=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Admin"
