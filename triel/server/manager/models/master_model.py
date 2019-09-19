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
    result = models.TextField(blank=True)


class FileBase(models.Model):
    path = models.CharField(max_length=512, null=False)
