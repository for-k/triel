from rest_framework import serializers

from triel.server.manager.models import Simulator, Suite
from triel.simulator.validator import validate_simulator


class SimulatorSerializer(serializers.ModelSerializer):
    def validate_path(self, path):
        return validate_simulator(self.instance.name, path)

    class Meta:
        model = Simulator
        fields = '__all__'


class SuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suite
        fields = '__all__'
