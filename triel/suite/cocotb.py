import os

from cocotb_test.run import run

from triel.server.manager.models import CocoTest
from triel.simulator.validator import SimulatorNames, LanguageNames


def launch_cocotb_test(test: CocoTest):
    os.environ["SIM"] = {
        SimulatorNames.GHDL.value: "ghdl",
        SimulatorNames.ICARUS.value: "icarus"
    }.get(test.simulator.name)

    language = {
        LanguageNames.VHDL.value: "vhdl",
        LanguageNames.VERILOG.value: "verilog"
    }.get(test.language.name)

    files = [file.path for file in test.files.all()]

    folder, filename = os.path.split(test.module)
    module = os.path.splitext(filename)[0]

    sim_result = run(
        verilog_sources=files,
        toplevel=test.top_level,
        module=module,
        toplevel_lang=language,
        run_dir=folder
    )

    result = ""
    with open(sim_result) as file:
        for line in file:
            result += line

    return result
