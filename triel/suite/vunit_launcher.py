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

import os
import shutil
import sys
from runpy import run_path

from triel.server.manager.models.master_enuml import SimulatorNames
from triel.server.manager.models.test_model import Test
from triel.suite.xml_parser import XmlParser


def launch_vunit_test(test: Test):
    os.environ["VUNIT_SIMULATOR"] = {
        SimulatorNames.GHDL.value: "ghdl",
    }.get(test.tool.name)

    # clean_build(os.path.join(test.working_dir, "vunit_out"))

    try:
        sys.argv = ['', "--xunit-xml-format", "jenkins", "-x", os.path.join("vunit_out", "out.xml"), "--gtkwave-fmt",
                    "vcd"]
        os.chdir(test.working_dir)
        run_path(test.files.all()[0].name, run_name="__main__")
    except SystemExit:
        pass
    finally:
        test.result = XmlParser().vunit_xml(os.path.join(test.working_dir, os.path.join("vunit_out", "out.xml")),
                                            test.tool.name,
                                            test.working_dir)


def clean_build(wd):
    if os.path.isdir(wd):
        shutil.rmtree(wd)
