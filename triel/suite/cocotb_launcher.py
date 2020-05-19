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
import importlib
import os
import shutil

import cocotb
from cocotb_test.run import run

from triel.server.manager.models.master_enuml import SimulatorNames
from triel.server.manager.models.test_enum import FileTypeChoices
from triel.server.manager.models.test_model import Case, Test
from triel.suite.xml_parser import XmlParser

BUILD = "sim_build"
RESULT_EXT = ".xml"
WAVE_EXT = ".vcd"


def generate_relative_imports(wd, filepath):
    if wd in filepath:
        extra_route = filepath.split(wd)[1].rsplit('.')[0]
        relative_import_path = ""
        for folder in extra_route.split(os.sep):
            relative_import_path += folder + "."
        return relative_import_path[:-1]


def separate_src_and_modules(files):
    src_list = []
    module_list = []

    for file in files:
        if file.file_type in (FileTypeChoices.vhdl08.value, FileTypeChoices.vlog05.value):
            src_list.append(file.name)
        elif file.file_type == FileTypeChoices.py.value:
            module_list.append(file.name)

    return src_list, module_list


def list_cocotb_test(case: Case):
    file_path = os.path.join(case.working_dir, case.file)
    spec = importlib.util.spec_from_file_location(os.path.splitext(file_path)[0].split('/')[-1], file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    case.result = []
    for test in dir(mod):
        if isinstance(getattr(mod, test), cocotb.coroutine):
            with open(file_path) as fd:
                offset = 0
                line_number = getattr(mod, test)._func.__code__.co_firstlineno - 1
                for line in fd:
                    line_number -= 1
                    offset += len(line)
                    if line_number == 0:
                        break

            case.result.append({
                "attributes": {},
                "location": {'file_name': file_path, 'length': len(test), "offset": offset},
                "name": test
            })


def launch_cocotb_test(test: Test):
    build_dir = os.path.join(os.getcwd(), BUILD)
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)

    os.environ["SIM"], language, source_arg = {
        SimulatorNames.GHDL.value: ("ghdl", "vhdl", "vhdl_sources"),
        SimulatorNames.ICARUS.value: ("icarus", "verilog", "verilog_sources"),
    }.get(test.tool.name)

    src_list, module_list = separate_src_and_modules(test.files.all())
    module_list.append(os.path.join(test.case.working_dir, test.case.file))
    module_list = list(set(module_list))

    modules = ""
    for module in module_list:
        modules += generate_relative_imports(test.case.working_dir, module) + ','
    modules = modules[:-1]

    simulator_args = []
    for sarg in test.tool_options.all():
        text = sarg.group
        if sarg.argument:
            text += "=" + sarg.argument
        simulator_args.append(text)

    args = {
        source_arg: src_list,
        "toplevel": test.top_level,
        "module": modules,
        "toplevel_lang": language,
        "run_dir": test.case.working_dir,
        "simulation_args": simulator_args,
        "testcase": test.name,
    }

    try:
        sim_result = run(**args)
    except Exception:
        sim_result = search_for_file_by_ext(build_dir, RESULT_EXT)

    test.result = XmlParser().coco_xml(sim_result, search_for_file_by_ext(build_dir, WAVE_EXT))


def search_for_file_by_ext(folder: str, ext: str):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                return os.path.join(folder, file)
        for dir in dirs:
            search_for_file_by_ext(os.path.join(folder, dir), ext)
    return ""
