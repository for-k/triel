from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from triel.server.manager.models import Simulator, Suite, Language, CocoTest, CocoOption, EdalizeStep, EdalizeTest, \
    CocoTestFilesTests, CocoTestFiles, EdalizeTestFiles
from triel.simulator.validator import validate_simulator
from triel.suite.cocotb import launch_cocotb_test


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


class CocoTestFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocoTestFiles
        fields = ('path',)


class CocoTestFilesTestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocoTestFilesTests
        fields = ('path',)


class CocoTestSerializer(serializers.ModelSerializer):
    simulator = PrimaryKeyRelatedField(many=False, read_only=True)
    language = PrimaryKeyRelatedField(many=False, read_only=True)
    options = CocoOptionSerializer(many=True, required=False)
    files = CocoTestFilesSerializer(many=True, required=False)
    tests = CocoTestFilesTestsSerializer(many=True, required=False)

    class Meta:
        model = CocoTest
        fields = ('id', 'name', 'language', 'top_level', 'simulator', 'module', 'tests', 'options', 'files', 'result')

    def create(self, validated_data):
        options_data_list = validated_data.pop('options', ())
        tests_data_list = validated_data.pop('tests', ())
        files_data_list = validated_data.pop('files', ())

        test = CocoTest.objects.create(
            language=Language.objects.filter(id=self.context['request'].data['language'])[0],
            simulator=Simulator.objects.filter(id=self.context['request'].data['simulator'])[0],
            **validated_data
        )

        for options_data in options_data_list:
            CocoOption.objects.create(test=test, **options_data)
        for test_data in tests_data_list:
            CocoTestFilesTests.objects.create(test=test, **test_data)
        for files_data in files_data_list:
            CocoTestFiles.objects.create(test=test, **files_data)

        test.result = launch_cocotb_test(test)
        test.save()

        return test


class EdalizeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdalizeStep
        fields = ('type', 'parameters')


class EdalizeTestSerializer(serializers.ModelSerializer):
    simulator = PrimaryKeyRelatedField(many=False, read_only=True)
    steps = EdalizeStepSerializer(many=True)

    class Meta:
        model = EdalizeTest
        fields = ('id', 'name', 'top_level', 'simulator', 'steps', 'files', 'result')

    def create(self, validated_data):
        steps_data_list = validated_data.pop('steps')
        files_data_list = validated_data.pop('files')

        test = EdalizeTest.objects.create(
            simulator=Simulator.objects.filter(id=self.context['request'].data['simulator'])[0],
            **validated_data
        )

        for steps_data in steps_data_list:
            EdalizeStep.objects.create(test=test, **steps_data)
        for files_data in files_data_list:
            EdalizeTestFiles.objects.create(test=test, **files_data)

        return test
