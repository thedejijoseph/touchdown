
from wsgiref import validate
from django.utils import timezone

from rest_framework.serializers import ModelSerializer

from devices.models import Device

class DeviceInfoSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'device_id',
            'brand',
            'brand_version',
            'architecture',
            'model',
            'platform',
            'platform_version',
            'is_mobile',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['account']

    def create(self, validated_data):
        return Device.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.brand = validated_data.get('brand', instance.brand)
        instance.brand_version = validated_data.get('brand_version', instance.brand_version)
        instance.architecture = validated_data.get('architecture', instance.architecture)
        instance.model = validated_data.get('model', instance.model)
        instance.platform = validated_data.get('platform', instance.platform)
        instance.platform_version = validated_data.get('platform_version', instance.platform_version)
        instance.is_mobile = validated_data.get('is_mobile', instance.is_mobile)
        instance.updated_at = timezone.now()
        instance.save()
        return instance