from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ModelViewSet

from triel.server.manager.models import Simulator, Suite, Language, CocoTest, EdalizeTest
from triel.server.manager.serializers import SimulatorSerializer, SuiteSerializer, LanguageSerializer, \
    CocoTestSerializer, EdalizeTestSerializer


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


class CocoTestViewSet(ModelViewSet):
    """
    API endpoint that allows Suites to be viewed.
    """
    queryset = CocoTest.objects.all()
    serializer_class = CocoTestSerializer


class EdalizeTestViewSet(ModelViewSet):
    """
    API endpoint that allows Suites to be viewed.
    """
    queryset = EdalizeTest.objects.all()
    serializer_class = EdalizeTestSerializer
