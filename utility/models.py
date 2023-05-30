from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File


# Create your models here.
class branch(models.Model):
    name = models.CharField(max_length=120, null=True, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class warranty(models.Model):
    name = models.CharField(max_length=120, null=True, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class manufacture(models.Model):
    name = models.CharField(max_length=120, null=True, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class hard_disk_type(models.Model):
    name = models.CharField(max_length=120, null=True, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class printer(models.Model):
    name = models.CharField(max_length=120, null=True, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class device_list(models.Model):
    barcode = models.ImageField(upload_to='barcodes/', null=True, blank=True)
    barcode_id = models.CharField(max_length=500, blank=True, null=True)
    branch = models.ForeignKey(branch, on_delete=models.SET_NULL, blank=False, null=True)
    user = models.CharField(max_length=120, blank=True, null=True)
    sys_name = models.CharField(max_length=120, blank=True, null=True)
    system_purchased_from = models.CharField(max_length=120, blank=True, null=True)
    system_purchased_year = models.DateField(null=True, blank=True)
    manufacture = models.ForeignKey(manufacture, on_delete=models.SET_NULL, blank=False, null=True)
    processor = models.CharField(max_length=120, blank=True, null=True)
    ram = models.CharField(max_length=5, blank=True, null=True)
    hard_disk_type = models.ForeignKey(hard_disk_type, on_delete=models.SET_NULL, blank=False, null=True)
    hard_disk_size = models.CharField(max_length=120, blank=True, null=True)
    monitor = models.CharField(max_length=120, blank=True, null=True)
    year = models.CharField(max_length=5, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    printer = models.ForeignKey(printer, on_delete=models.SET_NULL, blank=True, null=True)
    printer_purchased_from = models.CharField(max_length=120, blank=True, null=True)
    printer_year = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        if self.branch and self.system_purchased_year and self.sys_name:
            self.barcode_id = f"{self.branch}{self.system_purchased_year.year}{self.sys_name}"
        super().save(*args, **kwargs)
        EAN = barcode.get_barcode_class('code39')
        ean = EAN(self.barcode_id, writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save(f'{self.barcode_id}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)
