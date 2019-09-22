from django.db import models
from django.utils import timezone


class TestBase(models.Model):
    teros_project = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    result = models.TextField(blank=True)


class FileBase(models.Model):
    path = models.CharField(unique=True, max_length=512, null=False)


class SourceFile(FileBase):
    pass


class TestFile(FileBase):
    pass


class ArgumentBase(models.Model):
    group = models.CharField(max_length=255, null=True)
    argument = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = ('group', 'argument', 'value',)


class SimulatorArgument(ArgumentBase):
    pass


class SuiteArgument(ArgumentBase):
    pass
