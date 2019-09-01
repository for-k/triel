from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from triel.server.manager.models import Simulator
from triel.server.manager.serializers import SimulatorSerializer


class OnlyUpdateViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    pass


class SimulatorViewSet(OnlyUpdateViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer
