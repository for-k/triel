import os
import shutil

import edalize

from triel.server.manager.models.master_enuml import SimulatorNames
from triel.server.manager.models.test_model import Test


def validate_tool_options(tool, tool_options):
    return validate_argument_in_collection(
        tool_options, 'group',
        valid_options={
            SimulatorNames.GHDL.value: ('analyze_options', 'run_options'),
            SimulatorNames.ICARUS.value: ('timescale', 'iverilog_options'),
        }.get(tool)
    )


def validate_edalize_args(tool, parameter):
    return validate_argument_in_collection(
        parameter, 'paramtype',
        valid_options={
            SimulatorNames.GHDL.value: edalize.ghdl.Ghdl.argtypes,
            SimulatorNames.ICARUS.value: edalize.icarus.Icarus.argtypes,
        }.get(tool)
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


def parse_parameter_values(parameter_values):
    parameters = {}
    configure_args = []
    run_args = []

    for pv in parameter_values:
        parameters[pv.parameter.name] = {'datatype': pv.parameter.datatype, 'paramtype': pv.parameter.paramtype}
        if pv.parameter.description:
            parameters[pv.parameter.name]['description'] = pv.parameter.description
        if pv.default:
            parameters[pv.parameter.name]['default'] = pv.default

        if pv.configure:
            configure_args.append(f"--{parameters[pv.parameter.name]}={pv.configure}")
        if pv.run:
            configure_args.append(f"--{parameters[pv.parameter.name]}={pv.run}")

    return parameters, configure_args, run_args


TOOL_OPTION_GROUP_STRING_TYPE = ('timescale',)


def parse_tool_options(tool_options):
    tool_options_dict = {}
    for sarg in tool_options:
        if sarg.group not in tool_options_dict.keys():
            tool_options_dict[sarg.group] = []
        tool_options_dict[sarg.group].append(sarg.argument)

    for group in TOOL_OPTION_GROUP_STRING_TYPE:
        if group in tool_options_dict.keys():
            tool_options_dict[group] = tool_options_dict[group][0]

    return tool_options_dict


def launch_edalize_test(test: Test):
    tool = {
        SimulatorNames.GHDL.value: "ghdl",
        SimulatorNames.ICARUS.value: "icarus",
    }.get(test.tool.name)

    work_root = os.path.join(test.working_dir, 'build')
    clean_build(work_root)

    files = []
    for src in test.files.all():
        files.append({"name": src.name, "file_type": src.file_type})

    parameters, configure_args, run_args = parse_parameter_values(test.parameters.all())
    tool_options = parse_tool_options(test.tool_options.all())

    backend = edalize.get_edatool(tool)(
        edam={
            "files": files,
            "name": test.name,
            "toplevel": test.top_level,
            'parameters': parameters,
            "tool_options": {tool: tool_options}
        }, work_root=work_root
    )
    os.makedirs(work_root)
    backend.configure(configure_args)
    backend.build()
    backend.run(run_args)


def clean_build(build_dir):
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
