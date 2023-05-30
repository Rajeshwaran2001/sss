from django.db import models
from barcode import generate
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
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

    def save(self, *args, **kwargs):
        if not self.id and not self.barcode:
            # Generate barcode image
            barcode_value = str(self.id)
            barcode_image = generate('code128', barcode_value, writer=ImageWriter())

            # Create a BytesIO object to store the image
            buffer = BytesIO()
            barcode_image.save(buffer, format='PNG')

            # Set the file name
            file_name = f'barcode_{self.id}.png'

            # Create a ContentFile from the buffer's value
            barcode_content = ContentFile(buffer.getvalue())

            # Assign the ContentFile to the self.barcode attribute
            self.barcode.save(file_name, barcode_content)

        super(device_list, self).save(*args, **kwargs)
