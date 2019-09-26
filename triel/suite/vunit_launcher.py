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

    clean_build(os.path.join(test.working_dir, "vunit_out"))

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
