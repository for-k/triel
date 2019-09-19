from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from triel.server.manager.models.edalize_model import EdalizeStep, EdalizeTest, \
    EdalizeTestFiles
from triel.server.manager.models.master_model import Simulator


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
