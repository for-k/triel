from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet, ModelViewSet

from triel.server.manager.models.edalize_model import EdalizeTest
from triel.server.manager.models.coco_model import CocoTest
from triel.server.manager.models.master_model import Language, Simulator, Suite
from triel.server.manager.serializer.edalize_serializer import EdalizeTestSerializer
from triel.server.manager.serializer.coco_serializer import CocoTestSerializer
from triel.server.manager.serializer.master_serializer import LanguageSerializer, SimulatorSerializer, SuiteSerializer


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
