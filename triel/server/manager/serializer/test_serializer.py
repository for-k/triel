import os

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from triel.server.manager.models.test_model import SimulatorArgument, FileBase


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileBase
        fields = ('path',)

    def validate(self, attrs):
        if os.path.exists(attrs['path']):
            return super(FileSerializer, self).validate(attrs)
        else:
            raise ValidationError("Invalid path")


class SimulatorArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorArgument
        fields = ('argument', 'value')
