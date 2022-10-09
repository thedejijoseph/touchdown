
from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from devices.models import Device

class PositionPing(models.Model):
    account = models.ForeignKey(
        to=CustomUser,
        on_delete=models.PROTECT,
    )
    device = models.ForeignKey(
        to=Device,
        on_delete=models.PROTECT,
    )
    latitude = models.DecimalField(
        null=False,
        max_digits=12,
        decimal_places=8,
    )
    longitude = models.DecimalField(
        null=False,
        max_digits=12,
        decimal_places=8,
    )
    altitude = models.DecimalField(
        null=True,
        max_digits=12,
        decimal_places=4,
    )
    accuracy = models.FloatField(
        null=True,
    )
    altitude_accuracy = models.FloatField(
        null=True,
    )
    heading = models.FloatField(
        null=True,
    )
    speed = models.FloatField(
        null=True,
    )
    timestamp = models.BigIntegerField(
        null=True,
    )
    logged_at = models.DateTimeField(
        null=False,
    )
    created_at = models.DateTimeField(
        null=False,
        default=timezone.now,
    )
