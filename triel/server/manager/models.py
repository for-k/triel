from django.db import models


# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=255)


class Simulator(models.Model):
    name = models.CharField(max_length=255)
    path = models.FileField()


class SimulatorLanguage(models.Model):
    simulator = models.OneToOneField(Simulator, on_delete=models.DO_NOTHING)
    language = models.OneToOneField(Language, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=255)

    class Meta:
        unique_together = (('simulator', 'language'),)


class Suite(models.Model):
    name = models.CharField(max_length=255)


class SuiteSimulator(models.Model):
    suite = models.OneToOneField(Suite, on_delete=models.DO_NOTHING)
    simulator = models.OneToOneField(Simulator, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=255)

    class Meta:
        unique_together = (('suite', 'simulator'),)
