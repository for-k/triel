from rest_framework import serializers

from triel.server.manager.models import Simulator


class SimulatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulator
        fields = '__all__'
