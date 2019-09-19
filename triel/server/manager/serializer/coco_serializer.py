from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from triel.server.manager.models.coco_model import CocoTest
from triel.server.manager.serializer.test_serializer import SimulatorArgumentSerializer, FileSerializer


class CocoTestSerializer(serializers.ModelSerializer):
    simulator = PrimaryKeyRelatedField(many=False, read_only=True)
    modules = FileSerializer(many=True)
    sources = FileSerializer(many=True)
    simulator_args = SimulatorArgumentSerializer(many=True, required=False)

    class Meta:
        model = CocoTest
        fields = '__all__'

    def create(self, validated_data):
        return super(CocoTestSerializer, self).create(validated_data)

        #
        # options_data_list = validated_data.pop('options', ())
        # tests_data_list = validated_data.pop('tests', ())
        # files_data_list = validated_data.pop('files', ())
        #
        # test = CocoTest.objects.create(
        #     language=Language.objects.filter(id=self.context['request'].data['language'])[0],
        #     simulator=Simulator.objects.filter(id=self.context['request'].data['simulator'])[0],
        #     **validated_data
        # )
        #
        # for options_data in options_data_list:
        #     CocoOption.objects.create(test=test, **options_data)
        # for test_data in tests_data_list:
        #     CocoTestFilesTests.objects.create(test=test, **test_data)
        # for files_data in files_data_list:
        #     CocoTestFiles.objects.create(test=test, **files_data)
        #
        # test.result = launch_cocotb_test(test)
        # test.save()
        #
        # return test
