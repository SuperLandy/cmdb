from django.db import models
from uuid import uuid4
import django.utils.timezone as timezone
# Create your models here.


class Administrator(models.Model):

    id = models.UUIDField(max_length=36, null=False, default=uuid4, primary_key=True)
    name = models.CharField(max_length=128, null=False)
    password = models.CharField(max_length=256, null=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(max_length=256, null=True)


class Asset(models.Model):

    id = models.UUIDField(max_length=36, default=uuid4, primary_key=True)
    ip = models.GenericIPAddressField(max_length=128, unique=True)
    hostname = models.CharField(max_length=128)
    public_ip = models.GenericIPAddressField(max_length=128, null=True)
    protocol = models.CharField(max_length=10)
    port = models.CharField(max_length=5)
    is_active = models.BooleanField(null=False, default=True)
    assets_user = models.ForeignKey(Administrator, blank=True, null=True, on_delete=models.SET_NULL)
    vendor = models.CharField(max_length=128, null=True)
    model = models.CharField(max_length=128, null=True)
    cpu_cores = models.CharField(max_length=128, null=True)
    disk_info = models.CharField(max_length=1024, null=True)
    os = models.CharField(max_length=1024, null=True)
    sn = models.CharField(max_length=128, null=True)
    number = models.CharField(max_length=32, null=True)
    remarks = models.CharField(max_length=1024, null=True)
    cpu_model = models.CharField(max_length=128, null=True)
    memory = models.CharField(max_length=128, null=True)
    disk_total = models.CharField(max_length=1024, null=True)
    platform = models.CharField(max_length=1024, null=True)
    os_version = models.CharField(max_length=128, null=True)
    os_arch = models.CharField(max_length=128, null=True)
    hostname_raw = models.CharField(max_length=128, null=True)
    date_crated = models.DateTimeField(default=timezone.now)
