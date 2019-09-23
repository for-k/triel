import os

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from triel.server.manager.models.master_model import Simulator
from triel.server.manager.models.test_model import SimulatorArgument, File, ParameterDataTypeChoices, Test


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
