import os

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from triel.server.manager.models.master_model import Simulator
from triel.server.manager.models.test_model import SimulatorArgument, File, ParameterDataTypeChoices, Test, \
    SuiteChoices, ParameterValue
from triel.suite.cocotb_launcher import launch_cocotb_test
from triel.suite.edalize_launcher import validate_tool_options, validate_edalize_args, launch_edalize_test


def search_before_create(model, validated_data):
    db_data = model.objects.filter(**validated_data)
    if db_data:
        return db_data[0]
    else:
        return model.objects.create(**validated_data)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        extra_kwargs = {
            'path': {'validators': []},
        }

    def validate(self, attrs):
        if os.path.exists(attrs['path']):
            return attrs
        else:
            raise ValidationError("Invalid path")


class ParameterValueSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        try:
            datatype = attrs['parameter'].datatype
            if 'default' in attrs.keys():
                attrs['default'] = self.validate_by_datatype(datatype, attrs['default'])
            if 'configure' in attrs.keys():
                attrs['configure'] = self.validate_by_datatype(datatype, attrs['configure'])
            if 'run' in attrs.keys():
                attrs['run'] = self.validate_by_datatype(datatype, attrs['run'])

        except Exception:
            raise ValidationError("Invalid value for this datatype")

    @staticmethod
    def validate_by_datatype(datatype, value):
        if datatype == ParameterDataTypeChoices.bool:
            return bool(value)
        elif datatype == ParameterDataTypeChoices.int:
            return int(value)
        elif datatype in (ParameterDataTypeChoices.str, ParameterDataTypeChoices.file):
            return str(value)


class SimulatorArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorArgument
        fields = '__all__'
        validators = []


class TestSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)
    parameters = ParameterValueSerializer(many=True, required=False)
    tool = SlugRelatedField(many=False, queryset=Simulator.objects.all(), slug_field='name')
    tool_options = SimulatorArgumentSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = '__all__'

    def validate_working_dir(self, wd):
        if os.path.exists(wd):
            return wd
        else:
            raise ValidationError("Invalid path")

    def validate(self, attrs):
        if 'suite' not in attrs.keys():
            attrs['suite'] = SuiteChoices.edalize.value

        if attrs['tool'] == SuiteChoices.edalize.value:
            if 'name' not in attrs.keys():
                raise ValidationError("Field name required for Edalize")
            if 'simulator_args' in attrs.keys() and \
                    not validate_tool_options(attrs['simulator'].name, attrs['simulator_args']):
                raise ValidationError(f"Invalid tool options group for simulator {attrs['simulator']}")
            if 'parameters' in attrs.keys() and \
                    not validate_edalize_args(attrs['simulator'].name, attrs['parameters'].parameter):
                raise ValidationError(f"Invalid parameter type for simulator {attrs['simulator']}")

        return super(TestSerializer, self).validate(attrs)

    def create(self, validated_data):

        if not validated_data['working_dir'].endswith(os.sep):
            validated_data['working_dir'] += os.sep

        file_list = validated_data.pop('files', ())
        tool_options_list = validated_data.pop('tool_options', ())
        parameters = validated_data.pop('parameters', ())

        test = Test.objects.create(**validated_data)
        test.files.set([search_before_create(File, file) for file in file_list])
        test.tool_options.set([search_before_create(SimulatorArgument, tool_opt) for tool_opt in
                               tool_options_list])
        test.parameters.set([search_before_create(ParameterValue, parameter) for parameter in
                             parameters])

        {
            SuiteChoices.edalize.value: launch_edalize_test,
            SuiteChoices.cocotb.value: launch_cocotb_test,
        }.get(validated_data['suite'])(test)

        test.save()

        return test
