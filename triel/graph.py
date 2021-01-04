"""

 Copyright 2021 Teros Technology

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
 along with Triel.  If not, see <https://www.gnu.org/licenses/>.

"""
import contextlib
import json
import os
from typing import Dict

from vunit.project import Project
from vunit.vhdl_standard import VHDL

from triel.broker import Broker
from triel.topic import GraphConsumer, TrielTopic


def get_direct_dependencies(project):
    dependency_graph = project.create_dependency_graph(True)

    files = project.get_source_files_in_order()

    dependencies = []
    for i in range(0, len(files)):
        dependency_local = []
        dependency = dependency_graph.get_direct_dependencies(files[i])
        for dep in dependency:
            dependency_local.append(str(dep.name))
        dependencies.append(dependency_local)

    return files, dependencies


class EdalizeGraphDependency(GraphConsumer):
    def on_graph_requested(self, tedam_json: Dict):
        project = Project()
        for file in tedam_json["files"]:
            with contextlib.suppress(ValueError):
                project.add_library(file["logical_name"], tedam_json["work_directory"])
            project.add_source_file(
                file["name"],
                file["logical_name"],
                file_type=file["file_type"],
                vhdl_standard=VHDL.STD_2008,
            )

        files, dependencies = get_direct_dependencies(project)

        nodes = []
        complete_nodes = []
        for i in range(0, len(files)):
            complete_nodes.append(files[i].name)
            name = os.path.basename(files[i].name)
            nodes.append(name)

        # Add nodes
        diagram = """
        digraph {
            node [color="#069302" fillcolor=lightgray fontname=helvetica shape=component splines=line style="filled,rounded"]
        """
        for i in range(0, len(nodes)):
            diagram += (
                    '    "' + str(complete_nodes[i]) + '" [label="' + str(nodes[i]) + '"]\n'
            )

        # Add edge node
        for i in range(0, len(dependencies)):
            for j in range(0, len(dependencies[i])):
                if str(complete_nodes[i]) != str(dependencies[i][j]):
                    diagram += (
                            '    "'
                            + str(complete_nodes[i])
                            + '" -> "'
                            + str(dependencies[i][j])
                            + '"\n'
                    )
        diagram += "}"
        Broker.produce(TrielTopic.GRAPH_RES, json.loads(diagram))
