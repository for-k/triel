from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from triel.server.manager.models import Simulator, Suite, Language, CocoTest, CocoOption
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


class CocoOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocoOption
        fields = ('type', 'value')


class CocoTestSerializer(serializers.ModelSerializer):
    simulator = PrimaryKeyRelatedField(many=False, read_only=True)
    language = PrimaryKeyRelatedField(many=False, read_only=True)
    options = CocoOptionSerializer(many=True)

    class Meta:
        model = CocoTest
        fields = ('id', 'name', 'language', 'top_level', 'simulator', 'module', 'tests', 'options', 'files')

    def create(self, validated_data):
        options_data_list = validated_data.pop('options')
        test = CocoTest.objects.create(
            language=Language.objects.filter(id=self.context['request'].data['language'])[0],
            simulator=Simulator.objects.filter(id=self.context['request'].data['simulator'])[0],
            files=self.context['request'].data['files'],
            tests=self.context['request'].data['tests'],
            **validated_data
        )
        for options_data in options_data_list:
            CocoOption.objects.create(test=test, **options_data)
        return test
