from enum import Enum


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