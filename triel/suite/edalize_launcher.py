import os
import shutil

import edalize
from triel.server.manager.models.edalize_model import EdalizeTest

from triel.simulator.validator import SimulatorNames


def validate_tool_options(simulator, simulator_args):
    return validate_argument_in_collection(
        simulator_args, 'group',
        valid_options={
            SimulatorNames.GHDL.value: ('analyze_options', 'run_options'),
            SimulatorNames.ICARUS.value: ('timescale', 'iverilog_options'),
        }.get(simulator)
    )


def validate_edalize_args(simulator, parameter):
    return validate_argument_in_collection(
        parameter, 'paramtype',
        valid_options={
            SimulatorNames.GHDL.value: edalize.ghdl.Ghdl.argtypes,
            SimulatorNames.ICARUS.value: edalize.icarus.Icarus.argtypes,
        }.get(simulator)
    )


def validate_argument_in_collection(args_attr, key, valid_options):
    input_args = []
    for arg in args_attr:
        if key in arg.keys():
            input_args.append(arg[key])
    input_args = set(input_args)

    for group in input_args:
        if group not in valid_options:
            return False
    return True


def group_arguments(arguments):
    result = {}
    for sarg in arguments:
        if sarg.group not in result.keys():
            result[sarg.group] = []
        text = sarg.argument
        if sarg.value:
            text += "=" + sarg.value
        result[sarg.group].append(text)
    return result


def launch_edalize_test(test: EdalizeTest):
    simulator = {
        SimulatorNames.GHDL.value: "ghdl",
        SimulatorNames.ICARUS.value: "icarus",
    }.get(test.simulator.name)

    work_root = os.path.join(test.working_dir, 'build')
    if os.path.isdir(work_root):
        shutil.rmtree(work_root)

    default_src_type = {
        SimulatorNames.GHDL.value: "vhdlSource-2008",
        SimulatorNames.ICARUS.value: "",
    }.get(test.simulator.name)

    sources = []
    for src in test.sources.all():
        sources.append({"name": src.path, "file_type": default_src_type})

    simulator_arg = group_arguments(test.simulator_args.all())
    edalize_args = group_arguments(test.edalize_args.all())

    backend = edalize.get_edatool(simulator)(
        edam={
            "files": sources,
            "name": test.name,
            "toplevel": test.top_level,
            "tool_options": {simulator: simulator_arg}
        }, work_root=work_root
    )
    os.makedirs(work_root)
    backend.configure(edalize_args.get('configure', ""))
    backend.build()
    backend.run(edalize_args.get('run', ""))
