from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ModelViewSet

from triel.server.manager.models.master_model import Language, Simulator, Suite
from triel.server.manager.models.test_model import Test
from triel.server.manager.serializer.master_serializer import LanguageSerializer, SimulatorSerializer, SuiteSerializer
from triel.server.manager.serializer.test_serializer import TestSerializer


class OnlyUpdateViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    pass


class LanguageViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows Suites to be viewed.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class SimulatorViewSet(OnlyUpdateViewSet):
    """
    API endpoint that allows Simulators to be viewed or edited.
    """
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer


class SuiteViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows Suites to be viewed.
    """
    queryset = Suite.objects.all()
    serializer_class = SuiteSerializer


class TestViewSet(ModelViewSet):
    """
    API endpoint that allows Tests to be viewed.
    """
    queryset = Test.objects.all()
    serializer_class = TestSerializer
