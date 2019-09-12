from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)


class Simulator(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)
    path = models.CharField(max_length=255, null=True)


class SimulatorLanguage(models.Model):
    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = (('simulator', 'language'),)


class Suite(models.Model):
    name = models.CharField(max_length=255, unique=True, editable=False)


class SuiteSimulator(models.Model):
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = (('suite', 'simulator'),)
