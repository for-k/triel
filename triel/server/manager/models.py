from django.db import models


# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Simulator(models.Model):
    name = models.CharField(max_length=255, unique=True)
    path = models.FileField(null=True)


class SimulatorLanguage(models.Model):
    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = (('simulator', 'language'),)


class Suite(models.Model):
    name = models.CharField(max_length=255, unique=True)


class SuiteSimulator(models.Model):
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = (('suite', 'simulator'),)
