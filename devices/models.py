
from uuid import uuid4

from django.db import models
from django.utils import timezone

from accounts.models import CustomUser

class Device(models.Model):
    account = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
        null=False,
    )
    device_id = models.UUIDField(
        default=uuid4,
        null=False,
    )
    brand = models.CharField(
        max_length=64,
        null=True,
    )
    brand_version = models.CharField(
        max_length=16,
        null=True,
    )
    architecture = models.CharField(
        max_length=4,
        null=True,
    )
    model = models.CharField(
        max_length=32,
        null=True,
    )
    platform = models.CharField(
        max_length=32,
        null=True,
    )
    platform_version = models.CharField(
        max_length=16,
        null=True,
    )
    is_mobile = models.BooleanField(
        null=True,
    )
    created_at = models.DateTimeField(
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        default=timezone.now,
    )
