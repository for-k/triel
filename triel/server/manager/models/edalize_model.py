from django.db import models

from triel.server.manager.models.master_model import Simulator, TestBase, FileBase


class EdalizeTest(TestBase):
    name = models.CharField(max_length=255, unique=False, null=False)
    top_level = models.CharField(max_length=255, unique=False, null=False)
    simulator = models.ForeignKey(Simulator, on_delete=models.DO_NOTHING, null=False)


class EdalizeTestFiles(FileBase):
    test = models.ForeignKey(EdalizeTest, on_delete=models.CASCADE, related_name='files')
    type = models.CharField(max_length=255, unique=False, null=False)


class EdalizeStep(models.Model):
    test = models.ForeignKey(EdalizeTest, on_delete=models.CASCADE, related_name='steps')
    type = models.CharField(max_length=255, unique=False)
    parameters = models.CharField(max_length=255, unique=False)
