import os

from cocotb_test.run import run

from triel.server.manager.models.coco_model import CocoTest
from triel.simulator.validator import SimulatorNames, LanguageNames


def launch_cocotb_test(test: CocoTest):
    os.environ["SIM"] = {
        SimulatorNames.GHDL.value: "ghdl",
        SimulatorNames.ICARUS.value: "icarus"
    }.get(test.simulator.name)

    language, source_args = {
        LanguageNames.VHDL.value: ("vhdl", "vhdl_sources"),
        LanguageNames.VERILOG.value: ("verilog", "verilog_sources"),
    }.get(test.language.name)

    files = [file.path for file in test.files.all()]

    folder, filename = os.path.split(test.module)
    module = os.path.splitext(filename)[0]

    simulator_args = [option.type + "=" + option.value for option in test.options.all()]

    args = {
        source_args: files,
        "toplevel": test.top_level,
        "module": module,
        "toplevel_lang": language,
        "run_dir": folder,
        "simulator_args": simulator_args
    }

    sim_result = run(**args)

    result = ""
    with open(sim_result) as file:
        for line in file:
            result += line

    return result
