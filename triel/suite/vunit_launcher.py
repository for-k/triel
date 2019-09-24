import os
import sys
from runpy import run_path

from triel.server.manager.models.master_enuml import SimulatorNames
from triel.server.manager.models.test_model import Test
from triel.suite.xml_parser import XmlParser


def launch_vunit_test(test: Test):
    os.environ["VUNIT_SIMULATOR"] = {
        SimulatorNames.GHDL.value: "ghdl",
    }.get(test.tool.name)

    try:
        sys.argv = ['', "--xunit-xml-format", "jenkins", "-x", "out.xml", "--gtkwave-fmt", "vcd"]
        os.chdir(test.working_dir)
        run_path(test.files.all()[0].name, run_name="__main__")
    except SystemExit as err:
        if err.code == 0:
            test.result = XmlParser().vunit_xml(os.path.join(test.working_dir, 'out.xml'), test.tool.name, test.working_dir)
