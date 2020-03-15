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

from triel.suite.xml_parser import XmlParser
from triel_test.resources_test import resource_test_path

if __name__ == '__main__':
    xmlParser = XmlParser()
    print("\n ====  Vunit ok  ====  sim-> ghdl\n")
    print(xmlParser.vunit_xml(resource_test_path("xml/out.xml"), "ghdl", resource_test_path("")))
    print("\n ==== Vunit fail ====  sim-> ghdl\n")
    print(xmlParser.vunit_xml(resource_test_path("xml/out_fail.xml"), "ghdl", resource_test_path("")))
    print("\n ====  Vunit ok  ====  sim-> modelsim\n")
    print(xmlParser.vunit_xml(resource_test_path("xml/out.xml"), "modelsim", resource_test_path("")))
    print("\n ==== Vunit fail ====  sim-> modelsim\n")
    print(xmlParser.vunit_xml(resource_test_path("xml/out_fail.xml"), "modelsim", resource_test_path("")))
    print("\n ====  coco ok   ====\n")
    print(xmlParser.coco_xml(resource_test_path("xml/results.xml"), resource_test_path("xml/func.vcd")))
    print("\n ==== coco fail  ====\n")
    print(xmlParser.coco_xml(resource_test_path("xml/results_fail.xml"), resource_test_path("xml/func.vcd")))
