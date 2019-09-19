from django.db import models

from triel.server.manager.models.master_model import TestBase, Language, Simulator, FileBase


class CocoTest(TestBase):
    name = models.CharField(max_length=255, unique=False, null=False)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, null=False)
    top_level = models.CharField(max_length=255, unique=False, null=False)
    simulator = models.ForeignKey(Simulator, on_delete=models.DO_NOTHING, null=False)
    module = models.CharField(max_length=255, null=False)


class CocoTestFiles(FileBase):
    test = models.ForeignKey(CocoTest, on_delete=models.CASCADE, related_name='files')


class CocoTestFilesTests(FileBase):
    test = models.ForeignKey(CocoTest, on_delete=models.CASCADE, related_name='tests')


class CocoOption(models.Model):
    test = models.ForeignKey(CocoTest, on_delete=models.CASCADE, related_name='options')
    type = models.CharField(max_length=255, unique=False)
    value = models.CharField(max_length=255, unique=False)