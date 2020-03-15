"""

 Copyright 2020 Teros Technology

 Ismael Perez Rojo
 Carlos Alberto Ruiz Naranjo
 Alfredo Saez

 This file is part of Triel.

 Triel is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Triel is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Colibri.  If not, see <https://www.gnu.org/licenses/>.

"""

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