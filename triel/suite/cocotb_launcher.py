import os

from cocotb_test.run import run

from triel.server.manager.models.coco_model import CocoTest
from triel.simulator.validator import SimulatorNames


def generate_relative_imports(wd, filepath):
    if wd in filepath:
        extra_route = filepath.split(wd)[1].rsplit('.')[0]
        relative_import_path = ""
        for folder in extra_route.split(os.sep):
            relative_import_path += folder + "."
        return relative_import_path[:-1]


def launch_cocotb_test(test: CocoTest):
    os.environ["SIM"], language, source_arg = {
        SimulatorNames.GHDL.value: ("ghdl", "vhdl", "vhdl_sources"),
        SimulatorNames.ICARUS.value: ("icarus", "verilog", "verilog_sources"),
    }.get(test.simulator.name)

    modules = ""
    for module in test.modules.all():
        modules += generate_relative_imports(test.working_dir, module.path) + ','
    modules = modules[:-1]

    sources = [src.path for src in test.sources.all()]

    simulator_args = []
    for sarg in test.simulator_args.all():
        text = sarg.argument
        if sarg.value:
            text += "=" + sarg.value
        simulator_args.append(text)

    args = {
        source_arg: sources,
        "toplevel": test.top_level,
        "module": modules,
        "toplevel_lang": language,
        "run_dir": test.working_dir,
        "simulator_args": simulator_args
    }

    sim_result = run(**args)

    test.result = ""
    with open(sim_result) as file:
        for line in file:
            test.result += line
