import sys
from os.path import dirname
sys.path.append('../triel/suite')
import xml_parser

xmlParser= xml_parser.xml_parser()
print("\n ====  Vunit ok  ====  sim-> ghdl\n")
print(xmlParser.vunit_xml("./xml/out.xml","ghdl",""))
print("\n ==== Vunit fail ====  sim-> ghdl\n")
print(xmlParser.vunit_xml("./xml/out_fail.xml","ghdl",""))
print("\n ====  Vunit ok  ====  sim-> modelsim\n")
print(xmlParser.vunit_xml("./xml/out.xml","modelsim",""))
print("\n ==== Vunit fail ====  sim-> modelsim\n")
print(xmlParser.vunit_xml("./xml/out_fail.xml","modelsim",""))
print("\n ====  coco ok   ====\n")
print(xmlParser.coco_xml("./xml/results.xml","./func.vcd"))
print("\n ==== coco fail  ====\n")
print(xmlParser.coco_xml("./xml/results_fail.xml","./func.vcd"))
