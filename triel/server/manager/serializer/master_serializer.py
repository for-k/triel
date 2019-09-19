from rest_framework import serializers

from triel.server.manager.models.master_model import Language, Simulator, Suite
from triel.simulator.validator import validate_simulator


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class SimulatorSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)

    def validate_path(self, path):
        return validate_simulator(self.instance.name, path)

    class Meta:
        model = Simulator
        fields = '__all__'


class SimulatorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulator
        fields = ('id', 'name')


class SuiteSerializer(serializers.ModelSerializer):
    simulators = SimulatorNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Suite
        fields = '__all__'