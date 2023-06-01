from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import uuid
import random
import string


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
    asset_id = models.CharField(max_length=50, null=True, blank=True)
    barcode = models.ImageField(upload_to='barcodes/', null=True, blank=True)
    barcode_id = models.CharField(max_length=500, blank=True, null=True)
    warranty = models.ForeignKey(warranty, on_delete=models.SET_NULL, blank=False, null=True)
    branch = models.ForeignKey(branch, on_delete=models.SET_NULL, blank=False, null=True)
    user = models.CharField(max_length=120, blank=True, null=True)
    sys_name = models.CharField(max_length=120, blank=True, null=True)
    system_purchased_from = models.CharField(max_length=120, blank=True, null=True)
    bill_no = models.CharField(max_length=100, blank=True, null=True)
    system_purchased_year = models.DateField(null=True, blank=True)
    manufacture = models.ForeignKey(manufacture, on_delete=models.SET_NULL, blank=False, null=True)
    processor = models.CharField(max_length=120, blank=True, null=True)
    ram = models.CharField(max_length=5, blank=True, null=True)
    hard_disk_type = models.ForeignKey(hard_disk_type, on_delete=models.SET_NULL, blank=False, null=True)
    hard_disk_size = models.CharField(max_length=120, blank=True, null=True)
    monitor = models.CharField(max_length=120, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    printer = models.ForeignKey(printer, on_delete=models.SET_NULL, blank=True, null=True)
    printer_purchased_from = models.CharField(max_length=120, blank=True, null=True)
    printer_year = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        if not self.asset_id:
            branch_initial = self.branch.name[0] if self.branch and self.branch.name else ''
            random_number = self.generate_random_number()
            self.asset_id = f"{branch_initial}{random_number}"

        super().save(*args, **kwargs)
        if self.branch and self.system_purchased_year and self.sys_name:
            self.barcode_id = f"{self.branch} {self.system_purchased_year.year} {self.sys_name} {self.asset_id}"
            if any(char.isalpha() for char in self.barcode_id):
                self.barcode_id = self.barcode_id.upper()

        if self.branch and self.system_purchased_year and self.sys_name:
            barcode_data = f"{self.barcode_id}"
            EAN = barcode.get_barcode_class('code39')
            ean = EAN(barcode_data, writer=ImageWriter(),add_checksum=False)
            buffer = BytesIO()
            ean.write(buffer)
            barcode_filename = f'{self.barcode_id}.png'

            # Check if barcode image already exists
            if not self.barcode or self.barcode.name != barcode_filename:
                self.barcode.save(barcode_filename, File(buffer), save=False)

        return super().save(*args, **kwargs)

    def generate_random_number(self):
        while True:
            random_number = ''.join(random.choices(string.digits, k=4))
            if not device_list.objects.filter(asset_id=random_number).exists():
                return random_number
