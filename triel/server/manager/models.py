from django.db import models
from django.utils import timezone


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Simulator(models.Model):
    name = models.CharField(max_length=255, unique=True)
    path = models.CharField(max_length=512, null=True)
    languages = models.ManyToManyField(Language, related_name="simulators", blank=False, editable=False)


class Suite(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)
    simulators = models.ManyToManyField(Simulator, related_name="suites", blank=False, editable=False)


class TestBase(models.Model):
    date = models.DateTimeField(default=timezone.now, blank=True)


class FileBase(models.Model):
    path = models.CharField(max_length=512, null=False)


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
