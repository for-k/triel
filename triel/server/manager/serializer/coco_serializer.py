import os

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from triel.server.manager.models.coco_model import CocoTest
from triel.server.manager.models.master_model import Simulator
from triel.server.manager.models.test_model import TestFile, SourceFile, SimulatorArgument
from triel.server.manager.serializer.test_serializer import SimulatorArgumentSerializer, TestFileSerializer, \
    SourceFileSerializer, search_before_create
from triel.suite.cocotb_launcher import launch_cocotb_test


class CocoTestSerializer(serializers.ModelSerializer):
    simulator = SlugRelatedField(many=False, queryset=Simulator.objects.all(), slug_field='name')
    modules = TestFileSerializer(many=True)
    sources = SourceFileSerializer(many=True)
    simulator_args = SimulatorArgumentSerializer(many=True, required=False)

    class Meta:
        model = CocoTest
        fields = '__all__'

    def validate_working_dir(self, wd):
        if os.path.exists(wd):
            return wd
        else:
            raise ValidationError("Invalid path")

    def create(self, validated_data):

        modules_list = validated_data.pop('modules', ())
        sources_list = validated_data.pop('sources', ())
        simulator_args_list = validated_data.pop('simulator_args', ())

        if not validated_data['working_dir'].endswith(os.sep):
            validated_data['working_dir'] += os.sep

        test = CocoTest.objects.create(**validated_data)
        test.modules.set([search_before_create(TestFile, module) for module in modules_list])
        test.sources.set([search_before_create(SourceFile, source) for source in sources_list])
        test.simulator_args.set([search_before_create(SimulatorArgument, simulator_arg) for simulator_arg in
                                 simulator_args_list])

        launch_cocotb_test(test)

        test.save()

        return test
