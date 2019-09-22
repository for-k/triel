from django.db import models

from triel.server.manager.models.master_model import Simulator
from triel.server.manager.models.test_model import TestBase, SuiteArgument, SourceFile, SimulatorArgument


class EdalizeTest(TestBase):
    working_dir = models.CharField(max_length=512, unique=False, null=False)
    sources = models.ManyToManyField(SourceFile)
    top_level = models.CharField(max_length=128, unique=False, null=False)
    simulator = models.ForeignKey(Simulator, on_delete=models.DO_NOTHING, null=False)
    simulator_args = models.ManyToManyField(SimulatorArgument)
    edalize_args = models.ManyToManyField(SuiteArgument)