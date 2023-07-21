from django.contrib import admin
from .models import branch, warranty, manufacture, hard_disk_type, printer,device_list, hdd_size, ram
# Register your models here.

admin.site.register(branch)
admin.site.register(warranty)
admin.site.register(manufacture)
admin.site.register(hard_disk_type)
admin.site.register(printer)
admin.site.register(device_list)
admin.site.register(ram)
admin.site.register(hdd_size)
