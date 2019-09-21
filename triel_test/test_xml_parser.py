import sys
from os.path import dirname
sys.path.append('../triel/suite')
import xml_parser

vunitParser= xml_parser.xml_parser("./xml/out.xml","ghdl")
cocoParser= xml_parser.xml_parser("./xml/results_fail.xml","ghdl")
print(vunitParser.vunit_xml())
print(cocoParser.coco_xml())
