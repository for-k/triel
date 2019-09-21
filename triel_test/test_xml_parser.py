import sys
from os.path import dirname
sys.path.append('../triel/suite')
import xml_parser

xmlParser= xml_parser.xml_parser()
print(xmlParser.vunit_xml("./xml/out.xml","ghdl"))
print(xmlParser.coco_xml("./xml/results_fail.xml","./func.vcd"))
