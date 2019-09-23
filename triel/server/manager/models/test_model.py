from enum import Enum

from django.db import models
from django.utils import timezone

from triel.server.manager.models.master_model import Simulator, Suite


class ChoiseModel(Enum):
    @classmethod
    def choices(cls):
        return ((item.value, item.name) for item in cls)


class FileTypeChoices(ChoiseModel):
    qip = "QIP"
    ucf = "UCF"
    vlog05 = "verilogSource-2005"
    vhdl08 = "vhdlSource-2008"
    xci = "xci"
    xdc = "xdc"
    py = "py"


class ParameterTypeChoices(ChoiseModel):
    cmdlinearg = "cmdlinearg"
    generic = "generic"
    plusarg = "plusarg"
    vlogdefine = "vlogdefine"
    vlogparam = "vlogparam"


class ParameterDataTypeChoices(ChoiseModel):
    bool = "bool"
    file = "file"
    int = "int"
    str = "str"


class File(models.Model):
    name = models.CharField(unique=True, max_length=512)
    file_type = models.CharField(max_length=8, blank=True, choices=FileTypeChoices.choices())
    is_include_file = models.BooleanField(default=False, blank=True, null=True)
    logical_name = models.CharField(max_length=255, null=True, blank=True)


class Parameter(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, null=True, blank=True)
    datatype = models.CharField(max_length=16, choices=ParameterDataTypeChoices.choices())
    paramtype = models.CharField(max_length=16, choices=ParameterTypeChoices.choices())

    class Meta:
        unique_together = ('name', 'datatype', 'paramtype')


class ParameterValue(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING, null=False)
    default = models.CharField(max_length=256, null=True, blank=True)
    configure = models.CharField(max_length=256, null=True, blank=True)
    run = models.CharField(max_length=256, null=True, blank=True)


class SimulatorArgument(models.Model):
    group = models.CharField(max_length=255, null=True)
    argument = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('group', 'argument')


class Test(models.Model):
    suite = models.ForeignKey(Suite, on_delete=models.DO_NOTHING, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True)

    working_dir = models.CharField(max_length=512, null=False)
    files = models.ManyToManyField(File)
    parameters = models.ManyToManyField(ParameterValue)
    top_level = models.CharField(max_length=128, unique=False, null=False)
    tool = models.ForeignKey(Simulator, on_delete=models.DO_NOTHING, null=True, blank=True)
    tool_options = models.ManyToManyField(SimulatorArgument)

    result = models.TextField(blank=True)
