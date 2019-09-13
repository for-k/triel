from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)


class Simulator(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)
    path = models.CharField(max_length=255, null=True)
    languages = models.ManyToManyField(Language, related_name="simulators", blank=False, editable=False)


class Suite(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)
    simulators = models.ManyToManyField(Simulator, related_name="suites", blank=False, editable=False)
