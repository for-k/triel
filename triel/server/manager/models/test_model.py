from django.db import models
from django.utils import timezone


class TestBase(models.Model):
    date = models.DateTimeField(default=timezone.now, blank=True)
    result = models.TextField(blank=True)


class FileBase(models.Model):
    path = models.CharField(unique=True, max_length=512, null=False)


class SourceFile(FileBase):
    pass


class TestFile(FileBase):
    pass


class ArgumentBase(models.Model):
    argument = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('argument', 'value',)


class SimulatorArgument(ArgumentBase):
    pass


class SuiteArgument(ArgumentBase):
    pass
