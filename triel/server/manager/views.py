from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from triel.server.manager.models import Simulator, Suite, Language
from triel.server.manager.serializers import SimulatorSerializer, SuiteSerializer, LanguageSerializer


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
