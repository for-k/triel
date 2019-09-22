from builtins import super

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from triel.server.manager.models.edalize_model import EdalizeTest
from triel.server.manager.models.master_model import Simulator
from triel.server.manager.models.test_model import SourceFile, SimulatorArgument, SuiteArgument
from triel.server.manager.serializer.test_serializer import SimulatorArgumentSerializer, SourceFileSerializer, \
    SuiteArgumentSerializer, search_before_create
from triel.suite.edalize_launcher import validate_simulator_args, validate_edalize_args, launch_edalize_test


class EdalizeTestSerializer(serializers.ModelSerializer):
    simulator = SlugRelatedField(many=False, queryset=Simulator.objects.all(), slug_field='name')
    sources = SourceFileSerializer(many=True)
    simulator_args = SimulatorArgumentSerializer(many=True, required=False)
    edalize_args = SuiteArgumentSerializer(many=True, required=False)

    class Meta:
        model = EdalizeTest
        fields = '__all__'

    def validate(self, attrs):
        if 'name' not in attrs.keys():
            raise ValidationError("Field name required for Edalize")
        if 'simulator_args' in attrs.keys() and \
                not validate_simulator_args(attrs['simulator'].name, attrs['simulator_args']):
            raise ValidationError(f"Invalid simulator arg group for simulator {attrs['simulator']}")
        if 'edalize_args' in attrs.keys() and \
                not validate_edalize_args(attrs['simulator'].name, attrs['edalize_args']):
            raise ValidationError(f"Invalid edalize arg group for simulator {attrs['simulator']}")

        return super(EdalizeTestSerializer, self).validate(attrs)

    def create(self, validated_data):

        sources_list = validated_data.pop('sources', ())
        simulator_args_list = validated_data.pop('simulator_args', ())
        edalize_args_list = validated_data.pop('edalize_args', ())

        test = EdalizeTest.objects.create(**validated_data)
        test.sources.set([search_before_create(SourceFile, source) for source in sources_list])
        test.simulator_args.set([search_before_create(SimulatorArgument, simulator_arg) for simulator_arg in
                                 simulator_args_list])
        test.edalize_args.set([search_before_create(SuiteArgument, edalize_arg) for edalize_arg in
                               edalize_args_list])

        launch_edalize_test(test)

        test.save()

        return test
