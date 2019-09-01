from rest_framework import viewsets

# Create your views here.
from triel.server.manager.models import Simulator
from triel.server.manager.serializers import SimulatorSerializer


class SimulatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer
