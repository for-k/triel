from django.db import models
from django.utils import timezone


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Simulator(models.Model):
    name = models.CharField(max_length=255, unique=True)
    path = models.CharField(max_length=255, null=True)
    languages = models.ManyToManyField(Language, related_name="simulators", blank=False, editable=False)


class Suite(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)
    simulators = models.ManyToManyField(Simulator, related_name="suites", blank=False, editable=False)


class TestBase(models.Model):
    date = models.DateTimeField(default=timezone.now, blank=True)


class CocoTest(TestBase):
    name = models.CharField(max_length=255, unique=False, null=False)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING, null=False)
    top_level = models.CharField(max_length=255, unique=False, null=False)
    simulator = models.ForeignKey(Simulator, on_delete=models.DO_NOTHING, null=False)
    module = models.CharField(max_length=255, null=False)
    _tests = models.CharField(max_length=255, unique=False, db_column="tests")
    _files = models.CharField(max_length=255, unique=False, db_column="files")

    @property
    def tests(self):
        return eval(self._tests) if self._tests else ''

    @tests.setter
    def tests(self, tests):
        self._tests = str(tests)

    @property
    def files(self):
        return eval(self._files) if self._files else ''

    @files.setter
    def files(self, files):
        self._files = str(files)


class CocoOption(models.Model):
    test = models.ForeignKey(CocoTest, on_delete=models.CASCADE, related_name='options')
    type = models.CharField(max_length=255, unique=False)
    value = models.CharField(max_length=255, unique=False)
