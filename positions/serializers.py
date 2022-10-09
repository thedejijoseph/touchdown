
from rest_framework.serializers import ModelSerializer

from positions.models import PositionPing

class PositionPingSerializer(ModelSerializer):
    class Meta:
        model = PositionPing
        fields = [
            'latitude', 'longitude', 'altitude', 
            'accuracy', 'altitude_accuracy', 'heading', 
            'speed', 'timestamp', 'logged_at'
        ]
