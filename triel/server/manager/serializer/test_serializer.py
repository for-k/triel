import os

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from triel.server.manager.models.test_model import SimulatorArgument, FileBase, TestFile, SourceFile, SuiteArgument


def search_before_create(model, validated_data):
    db_data = model.objects.filter(**validated_data)
    if db_data:
        return db_data[0]
    else:
        return model.objects.create(**validated_data)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileBase
        fields = ('path',)
        extra_kwargs = {
            'path': {'validators': []},
        }

    def validate(self, attrs):
        if os.path.exists(attrs['path']):
            return attrs
        else:
            raise ValidationError("Invalid path")


class TestFileSerializer(FileSerializer):
    class Meta(FileSerializer.Meta):
        model = TestFile


class SourceFileSerializer(FileSerializer):
    class Meta(FileSerializer.Meta):
        model = SourceFile


class SimulatorArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorArgument
        fields = '__all__'
        validators = []


class SuiteArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiteArgument
        fields = '__all__'
        validators = []
